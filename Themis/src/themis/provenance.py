from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import re

import yaml

REQUIRED_METADATA = ["author", "date", "version", "source_type", "regulatory_domain"]


def parse_yaml_front_matter(text: str) -> Tuple[Dict[str, str], str]:
    if not text.strip().startswith("---"):
        raise ValueError("No metadata header found")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Malformed metadata header")
    header_text = parts[1].strip()
    metadata_raw = yaml.safe_load(header_text)
    if not isinstance(metadata_raw, dict):
        raise ValueError("Malformed metadata header")
    metadata = {str(k): str(v) for k, v in metadata_raw.items() if v is not None}
    body = parts[2].strip()
    return metadata, body


def get_lineage(file_path: str) -> Dict[str, str]:
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(file_path)
    text = p.read_text(encoding="utf-8")
    metadata, _ = parse_yaml_front_matter(text)
    return metadata


def parse_date(value: str) -> datetime:
    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y"]:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {value}")


def extract_claims(text: str) -> Dict[str, str]:
    claims: Dict[str, str] = {}
    body = text.lower()

    approved = re.search(r"approved\s+(\d{4})", body)
    if approved:
        claims["approval_year"] = approved.group(1)

    retention = re.search(r"retain(?:ed)?\s+data(?:\s+for)?\s+(\d+)\s+years?", body)
    if retention:
        claims["retention_years"] = retention.group(1)

    if "gdpr" in body:
        claims.setdefault("regulatory_domain_hint", "GDPR")
    if "data retention" in body:
        claims.setdefault("regulatory_domain_hint", "data retention")
    if "ip law" in body or "intellectual property" in body:
        claims.setdefault("regulatory_domain_hint", "IP law")

    return claims


def normalize_version(version: str) -> int:
    match = re.search(r"(\d+)", version)
    return int(match.group(1)) if match else 0


@dataclass
class SourceDocument:
    id: str
    cluster: str
    version: str
    author: str
    date: str
    source_type: str
    regulatory_domain: str
    content: str
    parent_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(init=False)
    claims: Dict[str, str] = field(init=False)

    def __post_init__(self) -> None:
        self.metadata = {
            "id": self.id,
            "cluster": self.cluster,
            "version": self.version,
            "author": self.author,
            "date": self.date,
            "source_type": self.source_type,
            "regulatory_domain": self.regulatory_domain,
        }
        self.validate_metadata()
        self.claims = extract_claims(self.body_text())

    def body_text(self) -> str:
        if self.content.strip().startswith("---"):
            try:
                _, body = parse_yaml_front_matter(self.content)
                return body
            except ValueError:
                return self.content
        return self.content

    def validate_metadata(self) -> None:
        missing = [key for key in REQUIRED_METADATA if not self.metadata.get(key)]
        if missing:
            raise ValueError(f"Missing required metadata fields: {missing}")

    def parsed_date(self) -> datetime:
        return parse_date(self.date)

    def normalized_version(self) -> int:
        return normalize_version(self.version)


@dataclass
class LineageGraph:
    nodes: Dict[str, SourceDocument]
    edges: Dict[str, List[str]]
    parents: Dict[str, List[str]]

    @property
    def root_ids(self) -> List[str]:
        return [node_id for node_id in self.nodes if node_id not in self.parents]

    def ancestors(self, source_id: str) -> List[str]:
        result: List[str] = []
        for parent_id in self.parents.get(source_id, []):
            result.extend(self.ancestors(parent_id))
            result.append(parent_id)
        return result

    def descendants(self, source_id: str) -> List[str]:
        result: List[str] = []
        for child_id in self.edges.get(source_id, []):
            result.append(child_id)
            result.extend(self.descendants(child_id))
        return result

    def chains(self) -> List[List[SourceDocument]]:
        results: List[List[SourceDocument]] = []

        def dfs(node_id: str, path: List[SourceDocument]) -> None:
            children = self.edges.get(node_id, [])
            if not children:
                results.append(path.copy())
                return
            for child_id in children:
                child = self.nodes[child_id]
                path.append(child)
                dfs(child_id, path)
                path.pop()

        for root_id in self.root_ids:
            dfs(root_id, [self.nodes[root_id]])

        return results


def load_source_document(file_path: str) -> SourceDocument:
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(file_path)
    text = p.read_text(encoding="utf-8")
    metadata, _ = parse_yaml_front_matter(text)
    source_id = metadata.get("id", p.stem)
    cluster = metadata.get("cluster", p.parent.name)
    version = metadata.get("version", p.stem)
    return SourceDocument(
        id=source_id,
        cluster=cluster,
        version=version,
        author=metadata.get("author", ""),
        date=metadata.get("date", ""),
        source_type=metadata.get("source_type", ""),
        regulatory_domain=metadata.get("regulatory_domain", ""),
        content=text,
        parent_ids=metadata.get("parent_ids", []),
    )


def parse_source_document(document: Dict[str, str]) -> SourceDocument:
    return SourceDocument(
        id=document["id"],
        cluster=document["cluster"],
        version=document["version"],
        author=document["author"],
        date=document["date"],
        source_type=document["source_type"],
        regulatory_domain=document["regulatory_domain"],
        content=document["content"],
        parent_ids=document.get("parent_ids", []),
    )


def build_lineage_graph(documents: Iterable[SourceDocument]) -> LineageGraph:
    nodes = {doc.id: doc for doc in documents}
    edges: Dict[str, List[str]] = {}
    parents: Dict[str, List[str]] = {}

    clusters: Dict[str, List[SourceDocument]] = {}
    for doc in nodes.values():
        clusters.setdefault(doc.cluster, []).append(doc)
        if doc.parent_ids:
            for parent_id in doc.parent_ids:
                edges.setdefault(parent_id, []).append(doc.id)
                parents.setdefault(doc.id, []).append(parent_id)

    for cluster_docs in clusters.values():
        ordered = sorted(cluster_docs, key=lambda doc: (doc.normalized_version(), doc.parsed_date()))
        for previous, current in zip(ordered, ordered[1:]):
            if current.id in parents:
                continue
            edges.setdefault(previous.id, []).append(current.id)
            parents.setdefault(current.id, []).append(previous.id)

    return LineageGraph(nodes=nodes, edges=edges, parents=parents)

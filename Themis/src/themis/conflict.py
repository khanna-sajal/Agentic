from __future__ import annotations

from dataclasses import dataclass, field, asdict
from itertools import combinations
from typing import Any, Dict, Iterable, List, Optional, Union
import re

from .provenance import SourceDocument, build_lineage_graph, get_lineage, load_source_document


@dataclass
class Conflict:
    doc_a: str
    doc_b: str
    conflicting_claim: str
    claim_a: str
    claim_b: str
    conflict_type: str
    evidence: List[str] = field(default_factory=list)
    rule_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        return result


def _conflict_type_for_claim(claim_key: str, value_a: str, value_b: str) -> str:
    if re.search(r"year|date|approved", claim_key, re.I) or (
        re.fullmatch(r"\d{4}", value_a) and re.fullmatch(r"\d{4}", value_b)
    ):
        return "DATE_CONFLICT"
    return "VERSION_MISMATCH"


def _get_source_document(value: Union[str, SourceDocument]) -> SourceDocument:
    if isinstance(value, SourceDocument):
        return value
    return load_source_document(value)


def detect_conflict(a_path: Union[str, SourceDocument], b_path: Union[str, SourceDocument], key: str = "date") -> Dict[str, str]:
    if isinstance(a_path, SourceDocument):
        a_doc = a_path
    else:
        a_doc = _get_source_document(a_path)
    if isinstance(b_path, SourceDocument):
        b_doc = b_path
    else:
        b_doc = _get_source_document(b_path)

    a_meta = a_doc.metadata
    b_meta = b_doc.metadata
    if key in a_meta and key in b_meta and a_meta[key] != b_meta[key]:
        return {
            "conflict_key": key,
            "a_value": a_meta[key],
            "b_value": b_meta[key],
            "reason": f"metadata '{key}' differs",
        }
    return {}


def extract_conflicts(sources: Iterable[SourceDocument]) -> List[Conflict]:
    conflicts: List[Conflict] = []
    for a, b in combinations(sources, 2):
        shared_keys = set(a.claims) & set(b.claims)
        for claim_key in shared_keys:
            value_a = a.claims[claim_key]
            value_b = b.claims[claim_key]
            if value_a != value_b:
                conflict_type = _conflict_type_for_claim(claim_key, value_a, value_b)
                evidence = [
                    f"{claim_key} differs: {a.id}='{value_a}' vs {b.id}='{value_b}'"
                ]
                conflicts.append(
                    Conflict(
                        doc_a=a.id,
                        doc_b=b.id,
                        conflicting_claim=claim_key,
                        claim_a=value_a,
                        claim_b=value_b,
                        conflict_type=conflict_type,
                        evidence=evidence,
                    )
                )
    return conflicts

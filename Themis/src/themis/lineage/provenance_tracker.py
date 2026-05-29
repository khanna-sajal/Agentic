from __future__ import annotations

from typing import Any, Dict, List, Optional

from .version_graph import VersionGraph


class ProvenanceTracker:
    def __init__(self) -> None:
        self.graph = VersionGraph()
        self.chunk_provenance: Dict[str, Dict[str, Any]] = {}

    def register_version(
        self,
        document_id: str,
        version: str,
        author: str,
        timestamp: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        return self.graph.add_version(
            document_id=document_id,
            version=version,
            author=author,
            timestamp=timestamp,
            metadata=metadata,
        )

    def link_versions(
        self,
        parent_document_id: str,
        parent_version: str,
        child_document_id: str,
        child_version: str,
        relationship: str = "update",
    ) -> None:
        self.graph.add_edge(
            parent_document_id=parent_document_id,
            parent_version=parent_version,
            child_document_id=child_document_id,
            child_version=child_version,
            relationship=relationship,
        )

    def tag_chunk(
        self,
        chunk_id: str,
        document_id: str,
        version: str,
        offset: int,
        length: int,
        content_hash: str,
    ) -> None:
        if chunk_id in self.chunk_provenance:
            raise ValueError(f"Chunk provenance already exists for {chunk_id}")
        self.chunk_provenance[chunk_id] = {
            "chunk_id": chunk_id,
            "document_id": document_id,
            "version": version,
            "offset": offset,
            "length": length,
            "content_hash": content_hash,
        }

    def get_chunk_provenance(self, chunk_id: str) -> Dict[str, Any]:
        if chunk_id not in self.chunk_provenance:
            raise KeyError(f"Chunk provenance not found: {chunk_id}")
        return self.chunk_provenance[chunk_id].copy()

    def get_version_lineage(self, document_id: str, version: str) -> List[List[Dict[str, Any]]]:
        paths = self.graph.get_ancestry_paths(document_id, version)
        return [self._expand_path(path) for path in paths]

    def get_descendant_lineage(self, document_id: str, version: str) -> List[List[Dict[str, Any]]]:
        paths = self.graph.get_descendant_paths(document_id, version)
        return [self._expand_path(path) for path in paths]

    def compare_versions(
        self,
        document_id_a: str,
        version_a: str,
        document_id_b: str,
        version_b: str,
    ) -> Dict[str, Any]:
        return self.graph.compare_versions(document_id_a, version_a, document_id_b, version_b)

    def _expand_path(self, path: List[str]) -> List[Dict[str, Any]]:
        return [self.graph.graph.nodes[node_key].copy() for node_key in path]

    def serialize(self) -> Dict[str, Any]:
        return {
            "graph": self.graph.serialize(),
            "chunk_provenance": self.chunk_provenance.copy(),
        }

    def load(self, data: Dict[str, Any]) -> None:
        self.graph.load(data["graph"])
        self.chunk_provenance = data.get("chunk_provenance", {}).copy()

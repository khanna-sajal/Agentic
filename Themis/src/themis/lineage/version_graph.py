from __future__ import annotations

from typing import Any, Dict, List, Optional

import networkx as nx


class VersionGraph:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    @staticmethod
    def _node_key(document_id: str, version: str) -> str:
        return f"{document_id}::{version}"

    def add_version(
        self,
        document_id: str,
        version: str,
        author: str,
        timestamp: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        node_id = self._node_key(document_id, version)
        if self.graph.has_node(node_id):
            raise ValueError(f"Version node already exists: {node_id}")

        self.graph.add_node(
            node_id,
            document_id=document_id,
            version=version,
            author=author,
            timestamp=timestamp,
            metadata=metadata or {},
        )
        return node_id

    def add_edge(
        self,
        parent_document_id: str,
        parent_version: str,
        child_document_id: str,
        child_version: str,
        relationship: str = "update",
    ) -> None:
        parent_key = self._node_key(parent_document_id, parent_version)
        child_key = self._node_key(child_document_id, child_version)
        if not self.graph.has_node(parent_key):
            raise KeyError(f"Parent node not found: {parent_key}")
        if not self.graph.has_node(child_key):
            raise KeyError(f"Child node not found: {child_key}")

        self.graph.add_edge(parent_key, child_key, relationship=relationship)

    def get_node(self, document_id: str, version: str) -> Dict[str, Any]:
        node_key = self._node_key(document_id, version)
        if not self.graph.has_node(node_key):
            raise KeyError(f"Version node not found: {node_key}")
        return dict(self.graph.nodes[node_key])

    def get_ancestry_paths(self, document_id: str, version: str) -> List[List[str]]:
        target = self._node_key(document_id, version)
        if not self.graph.has_node(target):
            raise KeyError(f"Version node not found: {target}")

        roots = [n for n in self.graph.nodes if self.graph.in_degree(n) == 0]
        paths: List[List[str]] = []
        for root in roots:
            if nx.has_path(self.graph, root, target):
                for path in nx.all_simple_paths(self.graph, root, target):
                    paths.append(path)
        return paths

    def get_descendant_paths(self, document_id: str, version: str) -> List[List[str]]:
        source = self._node_key(document_id, version)
        if not self.graph.has_node(source):
            raise KeyError(f"Version node not found: {source}")

        leaves = [n for n in self.graph.nodes if self.graph.out_degree(n) == 0]
        paths: List[List[str]] = []
        for leaf in leaves:
            if nx.has_path(self.graph, source, leaf):
                for path in nx.all_simple_paths(self.graph, source, leaf):
                    paths.append(path)
        return paths

    def compare_versions(
        self,
        document_id_a: str,
        version_a: str,
        document_id_b: str,
        version_b: str,
    ) -> Dict[str, Any]:
        node_a = self.get_node(document_id_a, version_a)
        node_b = self.get_node(document_id_b, version_b)

        differences: Dict[str, Dict[str, Any]] = {}
        for key in set(node_a.keys()) | set(node_b.keys()):
            if node_a.get(key) != node_b.get(key):
                differences[key] = {"a": node_a.get(key), "b": node_b.get(key)}

        return {
            "document_a": {"document_id": document_id_a, "version": version_a},
            "document_b": {"document_id": document_id_b, "version": version_b},
            "differences": differences,
        }

    def serialize(self) -> Dict[str, Any]:
        return nx.node_link_data(self.graph)

    def load(self, data: Dict[str, Any]) -> None:
        self.graph = nx.node_link_graph(data)

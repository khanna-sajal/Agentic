import pytest

from themis.lineage.version_graph import VersionGraph


def test_add_and_get_node():
    graph = VersionGraph()
    graph.add_version("cluster01", "1", author="Alice", timestamp="2026-01-01T00:00:00Z")
    node = graph.get_node("cluster01", "1")
    assert node["document_id"] == "cluster01"
    assert node["version"] == "1"
    assert node["author"] == "Alice"


def test_add_duplicate_version_raises():
    graph = VersionGraph()
    graph.add_version("cluster01", "1", author="Alice", timestamp="2026-01-01T00:00:00Z")
    with pytest.raises(ValueError):
        graph.add_version("cluster01", "1", author="Alice", timestamp="2026-01-01T00:00:00Z")


def test_add_edge_and_ancestry_paths():
    graph = VersionGraph()
    graph.add_version("cluster01", "1", author="Alice", timestamp="2026-01-01T00:00:00Z")
    graph.add_version("cluster01", "2", author="Bob", timestamp="2026-02-01T00:00:00Z")
    graph.add_edge("cluster01", "1", "cluster01", "2")

    paths = graph.get_ancestry_paths("cluster01", "2")
    assert paths == [["cluster01::1", "cluster01::2"]]


def test_get_descendant_paths():
    graph = VersionGraph()
    graph.add_version("cluster01", "1", author="Alice", timestamp="2026-01-01T00:00:00Z")
    graph.add_version("cluster01", "2", author="Bob", timestamp="2026-02-01T00:00:00Z")
    graph.add_edge("cluster01", "1", "cluster01", "2")

    paths = graph.get_descendant_paths("cluster01", "1")
    assert paths == [["cluster01::1", "cluster01::2"]]


def test_compare_versions_returns_differences():
    graph = VersionGraph()
    graph.add_version("cluster01", "1", author="Alice", timestamp="2026-01-01T00:00:00Z", metadata={"domain": "HIPAA"})
    graph.add_version("cluster01", "2", author="Bob", timestamp="2026-02-01T00:00:00Z", metadata={"domain": "GDPR"})

    diff = graph.compare_versions("cluster01", "1", "cluster01", "2")
    assert diff["document_a"]["version"] == "1"
    assert diff["document_b"]["version"] == "2"
    assert diff["differences"]["author"]["a"] == "Alice"
    assert diff["differences"]["author"]["b"] == "Bob"
    assert diff["differences"]["metadata"]["a"] == {"domain": "HIPAA"}
    assert diff["differences"]["metadata"]["b"] == {"domain": "GDPR"}

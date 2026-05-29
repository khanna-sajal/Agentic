import pytest

from themis.lineage.provenance_tracker import ProvenanceTracker


def test_provenance_tracker_register_and_lineage():
    tracker = ProvenanceTracker()
    tracker.register_version("cluster01", "1", author="Alice", timestamp="2026-01-01T00:00:00Z")
    tracker.register_version("cluster01", "2", author="Bob", timestamp="2026-02-01T00:00:00Z")
    tracker.link_versions("cluster01", "1", "cluster01", "2")

    paths = tracker.get_version_lineage("cluster01", "2")
    assert len(paths) == 1
    assert paths[0][0]["version"] == "1"
    assert paths[0][1]["version"] == "2"


def test_provenance_tracker_tag_chunk_and_retrieve():
    tracker = ProvenanceTracker()
    tracker.register_version("cluster01", "1", author="Alice", timestamp="2026-01-01T00:00:00Z")
    tracker.tag_chunk(
        chunk_id="chunk-001",
        document_id="cluster01",
        version="1",
        offset=0,
        length=128,
        content_hash="abc123",
    )

    provenance = tracker.get_chunk_provenance("chunk-001")
    assert provenance["document_id"] == "cluster01"
    assert provenance["version"] == "1"
    assert provenance["content_hash"] == "abc123"


def test_provenance_tracker_compare_versions():
    tracker = ProvenanceTracker()
    tracker.register_version("cluster01", "1", author="Alice", timestamp="2026-01-01T00:00:00Z", metadata={"domain": "HIPAA"})
    tracker.register_version("cluster01", "2", author="Bob", timestamp="2026-02-01T00:00:00Z", metadata={"domain": "GDPR"})

    diff = tracker.compare_versions("cluster01", "1", "cluster01", "2")
    assert diff["differences"]["author"]["a"] == "Alice"
    assert diff["differences"]["metadata"]["b"] == {"domain": "GDPR"}


def test_tag_chunk_duplicate_raises():
    tracker = ProvenanceTracker()
    tracker.register_version("cluster01", "1", author="Alice", timestamp="2026-01-01T00:00:00Z")
    tracker.tag_chunk(
        chunk_id="chunk-001",
        document_id="cluster01",
        version="1",
        offset=0,
        length=128,
        content_hash="abc123",
    )

    with pytest.raises(ValueError):
        tracker.tag_chunk(
            chunk_id="chunk-001",
            document_id="cluster01",
            version="1",
            offset=128,
            length=64,
            content_hash="def456",
        )

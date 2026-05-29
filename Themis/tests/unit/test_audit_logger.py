from pathlib import Path

from themis.audit.audit_logger import AuditLogger
from themis.db import Database


def test_audit_logger_appends_and_verifies(tmp_path: Path):
    db_path = tmp_path / "audit.db"
    db = Database(db_path)
    logger = AuditLogger(db)

    entry1 = logger.append_log(
        action="query",
        query="What is the encryption requirement?",
        sources=["cluster01_v1"],
        result_summary="Found requirement in cluster01_v1",
    )
    entry2 = logger.append_log(
        action="query",
        query="List version changes",
        sources=["cluster01_v2"],
        result_summary="Version history retrieved",
    )

    assert entry1["previous_hash"] is None
    assert entry2["previous_hash"] == entry1["entry_hash"]
    assert logger.verify()
    db.close()

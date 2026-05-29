from pathlib import Path

from themis.db import Database


def test_database_creates_tables(tmp_path: Path):
    db_path = tmp_path / "test.db"
    db = Database(db_path)
    rows = db.query("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = {row["name"] for row in rows}
    assert "documents" in table_names
    assert "chunks" in table_names
    assert "audit_logs" in table_names
    db.close()

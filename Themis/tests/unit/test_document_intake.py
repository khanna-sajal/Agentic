from pathlib import Path

from themis.db import Database
from themis.parser.document_intake import DocumentIntake


def test_document_intake_ingests_fixture(sample_corpus_dir: Path, tmp_path: Path):
    db_path = tmp_path / "documents.db"
    db = Database(db_path)
    intake = DocumentIntake(db, sample_corpus_dir)

    results = intake.ingest_all()
    assert len(results) == 2
    rows = db.query("SELECT COUNT(*) AS count FROM documents")
    assert rows[0]["count"] == 2
    chunk_rows = db.query("SELECT COUNT(*) AS count FROM chunks")
    assert chunk_rows[0]["count"] >= 2
    db.close()

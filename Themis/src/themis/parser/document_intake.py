from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .schema_validator import validate_metadata
from .yaml_metadata_parser import parse_yaml_front_matter
from themis.db import Database


def compute_content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def split_into_chunks(text: str, chunk_size: int = 512) -> List[str]:
    paragraphs = [paragraph.strip() for paragraph in text.strip().split("\n\n") if paragraph.strip()]
    chunks: List[str] = []
    for paragraph in paragraphs:
        for start in range(0, len(paragraph), chunk_size):
            chunks.append(paragraph[start : start + chunk_size])
    return chunks


class DocumentIntake:
    def __init__(self, db: Database, corpus_path: str | Path) -> None:
        self.db = db
        self.corpus_path = Path(corpus_path)

    def scan_corpus(self) -> Iterable[Path]:
        if not self.corpus_path.exists():
            raise FileNotFoundError(f"Corpus path not found: {self.corpus_path}")
        for path in sorted(self.corpus_path.rglob("*.txt")):
            if path.is_file():
                yield path

    def ingest_document(self, file_path: Path) -> Dict[str, Any]:
        raw_text = file_path.read_text(encoding="utf-8")
        parsed = parse_yaml_front_matter(raw_text, document_id=file_path.stem)
        validation = validate_metadata(parsed["metadata"])
        ingestion_timestamp = datetime.now(timezone.utc).isoformat()
        content_body = parsed.get("content", raw_text)
        content_hash = compute_content_hash(content_body)
        regulatory_domain = parsed["metadata"].get("regulatory_domain")
        if isinstance(regulatory_domain, list):
            regulatory_domain_text = json.dumps(regulatory_domain)
        else:
            regulatory_domain_text = json.dumps([])

        self.db.execute(
            "INSERT OR REPLACE INTO documents (document_id, filename, author, date, version, source_type, regulatory_domain, content_hash, ingestion_timestamp, validation_status, raw_metadata, content) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                file_path.stem,
                str(file_path.name),
                parsed["metadata"].get("author"),
                str(parsed["metadata"].get("date")),
                str(parsed["metadata"].get("version")),
                parsed["metadata"].get("source_type"),
                regulatory_domain_text,
                content_hash,
                ingestion_timestamp,
                "valid" if validation["valid"] else "invalid",
                json.dumps(parsed["metadata"], default=str),
                content_body,
            ],
        )

        chunks = split_into_chunks(content_body)
        for index, chunk in enumerate(chunks, start=1):
            chunk_id = f"{file_path.stem}::chunk::{index}"
            self.db.execute(
                "INSERT OR REPLACE INTO chunks (chunk_id, document_id, version, offset, length, content_hash, chunk_text) VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    chunk_id,
                    file_path.stem,
                    str(parsed["metadata"].get("version")),
                    (index - 1) * 512,
                    len(chunk),
                    compute_content_hash(chunk),
                    chunk,
                ],
            )

        return {
            "document_id": file_path.stem,
            "validation": validation,
            "chunks_created": len(chunks),
            "ingestion_timestamp": ingestion_timestamp,
        }

    def ingest_all(self) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for path in self.scan_corpus():
            results.append(self.ingest_document(path))
        return results

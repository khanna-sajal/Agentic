from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from themis.db import Database
from .hash_chain import compute_entry_hash, verify_hash_chain


class AuditLogger:
    def __init__(self, db: Database) -> None:
        self.db = db

    def _get_last_hash(self) -> Optional[str]:
        rows = self.db.query(
            "SELECT entry_hash FROM audit_logs ORDER BY sequence_number DESC LIMIT 1"
        )
        if not rows:
            return None
        return rows[0]["entry_hash"]

    def append_log(
        self,
        action: str,
        query: str,
        sources: List[str],
        result_summary: str,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        timestamp = timestamp or datetime.now(timezone.utc).isoformat()
        previous_hash = self._get_last_hash()
        entry = {
            "timestamp": timestamp,
            "action": action,
            "query": query,
            "sources": sources,
            "result_summary": result_summary,
            "previous_hash": previous_hash,
        }
        entry_hash = compute_entry_hash(entry)
        entry["entry_hash"] = entry_hash

        self.db.execute(
            "INSERT INTO audit_logs (timestamp, action, query, sources, result_summary, previous_hash, entry_hash) VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                timestamp,
                action,
                query,
                json.dumps(sources, ensure_ascii=False),
                result_summary,
                previous_hash,
                entry_hash,
            ],
        )
        return entry

    def get_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        rows = self.db.query(
            "SELECT sequence_number, timestamp, action, query, sources, result_summary, previous_hash, entry_hash FROM audit_logs ORDER BY sequence_number ASC LIMIT ?",
            [limit],
        )
        for row in rows:
            row["sources"] = json.loads(row["sources"] or "[]")
        return rows

    def verify(self) -> bool:
        rows = self.get_logs(limit=10000)
        entries = [
            {
                "timestamp": row["timestamp"],
                "action": row["action"],
                "query": row["query"],
                "sources": row["sources"],
                "result_summary": row["result_summary"],
                "previous_hash": row["previous_hash"],
                "entry_hash": row["entry_hash"],
            }
            for row in rows
        ]
        return verify_hash_chain(entries)

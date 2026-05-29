from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"
INITIAL_SCHEMA_SQL = MIGRATIONS_DIR / "0001_initial.sql"


class Database:
    def __init__(self, path: str | Path = ":memory:") -> None:
        self.path = Path(path)
        self.conn = sqlite3.connect(str(self.path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self) -> None:
        if not INITIAL_SCHEMA_SQL.exists():
            raise FileNotFoundError(f"Schema file not found: {INITIAL_SCHEMA_SQL}")
        schema = INITIAL_SCHEMA_SQL.read_text(encoding="utf-8")
        self.conn.executescript(schema)
        self.conn.commit()

    def execute(self, statement: str, params: Optional[List[Any]] = None) -> sqlite3.Cursor:
        cursor = self.conn.cursor()
        cursor.execute(statement, params or [])
        self.conn.commit()
        return cursor

    def query(self, statement: str, params: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(statement, params or [])
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def close(self) -> None:
        self.conn.close()


__all__ = ["Database"]

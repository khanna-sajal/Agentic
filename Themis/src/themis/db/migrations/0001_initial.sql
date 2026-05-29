CREATE TABLE IF NOT EXISTS documents (
    document_id TEXT PRIMARY KEY,
    filename TEXT,
    author TEXT,
    date TEXT,
    version TEXT,
    source_type TEXT,
    regulatory_domain TEXT,
    content_hash TEXT,
    ingestion_timestamp TEXT,
    validation_status TEXT,
    raw_metadata TEXT,
    content TEXT
);

CREATE TABLE IF NOT EXISTS chunks (
    chunk_id TEXT PRIMARY KEY,
    document_id TEXT,
    version TEXT,
    offset INTEGER,
    length INTEGER,
    content_hash TEXT,
    chunk_text TEXT
);

CREATE TABLE IF NOT EXISTS audit_logs (
    sequence_number INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    action TEXT NOT NULL,
    query TEXT,
    sources TEXT,
    result_summary TEXT,
    previous_hash TEXT,
    entry_hash TEXT NOT NULL
);

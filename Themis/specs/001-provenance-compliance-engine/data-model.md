# Data Model: Provenance & Compliance Engine

## Entities

- Document
  - id: string (e.g., cluster01_v2)
  - filename: string
  - version: string
  - author: string
  - date: ISO8601
  - source_type: string
  - regulatory_domain: string[]
  - content_hash: hex
  - ingestion_timestamp: ISO8601

- Metadata
  - extracted YAML front-matter fields
  - validation_status: enum (valid, missing_fields, malformed)

- Chunk
  - id: string
  - document_id: string
  - version: string
  - offset: int (character or token)
  - length: int
  - content_hash: hex
  - provenance: { document_id, version, chunk_location }

- Provenance (Graph Node)
  - node_id: string
  - attributes: { document_id, version, author, timestamp, content_hash }
  - edges: parent -> child (relationship: update|branch)

- Conflict
  - conflict_id: string
  - type: enum (exact_string|semantic|date_mismatch|policy_change)
  - documents: [document_id...]
  - conflicting_content: string
  - evidence: [{document_id, version, chunk_id}]
  - severity: LOW|MEDIUM|HIGH
  - detected_by: exact_matcher|semantic_validator

- ComplianceRisk
  - document_id
  - rule_id
  - severity
  - description
  - evidence: [{document_id, chunk_id, excerpt}]

- AuditLogEntry
  - sequence_number: int
  - timestamp: ISO8601
  - action: string
  - query: string
  - sources: [document_id]
  - result_summary: string
  - previous_hash: hex

## Storage Mapping
- Metadata and document records: SQLite table `documents`
- Provenance graph: serialized NetworkX node-link JSON stored in `provenance_graph` table; in-memory cache for runtime
- Conflicts: `conflicts` table with indices on severity and regulatory_domain
- Audit logs: `audit_logs` append-only table with `previous_hash`

## Validation Rules
- Required fields: `author`, `date`, `version` (fail validation if missing)
- `regulatory_domain` must match one or more entries in `regulatory_domains.yaml` (warn if unknown)
- `date` must be ISO8601 and parsable

## Notes
- Chunking strategy: token-based or paragraph-based (configurable)
- All hashes use SHA-256 hex strings
- Provenance graph maintained as directed acyclic graph (DiGraph) using NetworkX

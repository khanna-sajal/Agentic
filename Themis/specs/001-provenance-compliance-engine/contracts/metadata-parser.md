# Contract: YAML Metadata Parser

## Purpose
Extract YAML front-matter from input documents and return validated structured metadata.

## Input
- Plain text document with optional YAML front-matter at the very start.

## Output
- JSON object:
  - `document_id`: string
  - `metadata`: { author, date, version, source_type, regulatory_domain }
  - `validation_status`: `valid` | `missing_fields` | `malformed`
  - `errors`: optional list of parse/validation errors

## Behavior
- If YAML front-matter is present and valid: return `validation_status: valid` and parsed metadata
- If YAML front-matter missing required fields: return `validation_status: missing_fields` with `errors`
- If YAML malformed: return `validation_status: malformed` and include parser error message; processing continues for other documents

## Performance
- Parsing should complete within 100ms per document on average (SC-001)

## Error Handling
- Do not raise exceptions that stop batch processing; surface errors via `errors` field and logs

## Example
Input document:
```
---
author: Alice
date: 2026-01-01
version: 1
source_type: medical_record
regulatory_domain: [HIPAA]
---
Document body...
```

Output JSON:
```
{
  "document_id": "cluster01_v1",
  "metadata": { ... },
  "validation_status": "valid"
}
```

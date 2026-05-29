# Contract: POST /evaluate

## Endpoint

`POST /evaluate`

## Purpose

Evaluate a query and its supporting sources to produce a structured TrustSignal containing provenance evidence, conflict detection, trust scoring, and compliance risk labels.

## Request Schema

```json
{
  "query": "string",
  "rag_answer": "string",
  "sources": [
    {
      "id": "string",
      "cluster": "string",
      "version": "string",
      "author": "string",
      "date": "string",
      "source_type": "string",
      "regulatory_domain": "string",
      "content": "string"
    }
  ]
}
```

### Request Field Definitions

- `query`: The user question or claim being evaluated.
- `rag_answer`: The retrieved answer text from RAG sources.
- `sources`: Array of source documents used to derive the answer.
- `id`: Unique source document identifier.
- `cluster`: Corpus cluster identifier.
- `version`: Document version label.
- `author`: Metadata author.
- `date`: Publication or revision date.
- `source_type`: Source classification (e.g. `policy`, `guidance`).
- `regulatory_domain`: Regulatory domain context (e.g. `GDPR`, `data retention`, `IP law`).
- `content`: Raw document text, including YAML front matter.

## Response Schema

```json
{
  "score": 0.0,
  "flags": ["DATE_CONFLICT", "VERSION_MISMATCH", "COMPLIANCE_RISK"],
  "evidence": [
    {
      "source_id": "string",
      "lineage": ["string"],
      "conflicts": [
        {
          "doc_a": "string",
          "doc_b": "string",
          "conflicting_claim": "string",
          "claim_a": "string",
          "claim_b": "string",
          "conflict_type": "string"
        }
      ],
      "rule_matches": [
        {
          "rule_id": "string",
          "description": "string",
          "evidence": ["string"]
        }
      ]
    }
  ],
  "lineage_chains": [
    {
      "chain_id": "string",
      "nodes": [
        {
          "id": "string",
          "version": "string",
          "author": "string",
          "date": "string",
          "source_type": "string",
          "regulatory_domain": "string"
        }
      ]
    }
  ],
  "source_scores": [
    {
      "source_id": "string",
      "score": 0.0,
      "reason": "string"
    }
  ]
}
```

## Error Responses

- `400 Bad Request`: Missing or invalid input schema
- `422 Unprocessable Entity`: Validation failed on request payload
- `500 Internal Server Error`: Evaluation failure

## Notes

- The response must always include `evidence` and `lineage_chains` whenever a score is present.
- `flags` must include all applicable conflict and compliance risk indicators.

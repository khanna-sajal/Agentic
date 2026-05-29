# Quickstart: Provenance & Compliance Engine

## Prerequisites
- Python 3.11+
- Install dependencies: `pip install -r requirements.txt` (project root)

## Run ingestion (local)

1. Scan corpus and ingest documents:

```bash
python -m src.themis.parser.document_intake --scan ./corpus
```

2. Trigger on-demand ingestion via API:

```bash
uvicorn src.themis.api.ingest_api:app --reload
curl -X POST http://localhost:8000/api/v1/ingest -H "Content-Type: application/json" -d '{"trigger":"all"}'
```

## Run API server

```bash
uvicorn src.themis.api.main:app --host 0.0.0.0 --port 8000
```

## Example requests

- Provenance lookup:

```bash
curl http://localhost:8000/api/v1/provenance/<answer_id>
```

- Version compare:

```bash
curl "http://localhost:8000/api/v1/versions/compare?doc_id=cluster01&v1=1&v2=2"
```

## Tests

```bash
pytest -q
```

## Notes
- Configure `specs/001-provenance-compliance-engine/config/regulatory_domains.yaml` for taxonomy
- Groq API keys and endpoints configured via environment variables (e.g., `GROQ_API_KEY`)

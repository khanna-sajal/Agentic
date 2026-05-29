# Quickstart: Document Provenance & TrustSignal Evaluation

This quickstart shows the intended usage for the feature once implemented.

## 1. Prepare the input

The evaluation endpoint accepts:
- `query`: the user question or claim being evaluated
- `rag_answer`: the retrieved answer text from the source documents
- `sources`: an array of document source objects, each containing metadata and content

Example payload:

```json
{
  "query": "When was Policy X approved?",
  "rag_answer": "Policy X was approved in 2021 according to source v1, but the latest guidance says 2023.",
  "sources": [
    {
      "id": "cluster02_v1",
      "cluster": "cluster02",
      "version": "v1",
      "author": "Policy Team",
      "date": "2021-01-15",
      "source_type": "policy",
      "regulatory_domain": "GDPR",
      "content": "---\nauthor: Policy Team\ndate: 2021-01-15\nversion: v1\nsource_type: policy\nregulatory_domain: GDPR\n---\nPolicy X approved 2021."
    },
    {
      "id": "cluster02_v2",
      "cluster": "cluster02",
      "version": "v2",
      "author": "Compliance Officer",
      "date": "2022-06-20",
      "source_type": "policy",
      "regulatory_domain": "GDPR",
      "content": "---\nauthor: Compliance Officer\ndate: 2022-06-20\nversion: v2\nsource_type: policy\nregulatory_domain: GDPR\n---\nPolicy X policy text updated."
    },
    {
      "id": "cluster02_v3",
      "cluster": "cluster02",
      "version": "v3",
      "author": "Legal Team",
      "date": "2023-03-01",
      "source_type": "policy",
      "regulatory_domain": "GDPR",
      "content": "---\nauthor: Legal Team\ndate: 2023-03-01\nversion: v3\nsource_type: policy\nregulatory_domain: GDPR\n---\nPolicy X approved 2023."
    }
  ]
}
```

## 2. Send request to the evaluation API

```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d @payload.json
```

## 3. Interpret the TrustSignal response

Expected response structure:
- `score`: overall trust composite between 0 and 1
- `flags`: conflict and compliance risk flags
- `evidence`: lineage chain and conflict details per source
- `rule_matches`: matched compliance rules if any

## 4. Demo expectation

For cluster 02 with `v1` stating `2021` and `v3` stating `2023`, the system should return:
- `flags`: includes `DATE_CONFLICT`
- `score`: highest trust assigned to `v2` (target 0.9)
- `evidence`: a lineage chain showing `v1 -> v2 -> v3`
- `rule_matches`: if applicable, compliance rules triggered by conflicting regulatory statements

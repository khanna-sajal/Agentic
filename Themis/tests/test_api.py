from fastapi.testclient import TestClient

from themis.api import app


def test_evaluate_endpoint():
    client = TestClient(app)
    payload = {
        "query": "When was Policy X approved?",
        "rag_answer": "Policy X approved 2021 in v1 and 2023 in v3.",
        "sources": [
            {
                "id": "cluster02_v1",
                "cluster": "cluster02",
                "version": "v1",
                "author": "Policy Team",
                "date": "2021-01-15",
                "source_type": "policy",
                "regulatory_domain": "GDPR",
                "content": "---\nauthor: Policy Team\ndate: 2021-01-15\nversion: v1\nsource_type: policy\nregulatory_domain: GDPR\n---\nPolicy X approved 2021.",
            },
            {
                "id": "cluster02_v2",
                "cluster": "cluster02",
                "version": "v2",
                "author": "Compliance Officer",
                "date": "2022-06-20",
                "source_type": "policy",
                "regulatory_domain": "GDPR",
                "content": "---\nauthor: Compliance Officer\ndate: 2022-06-20\nversion: v2\nsource_type: policy\nregulatory_domain: GDPR\n---\nPolicy X updated.",
            },
            {
                "id": "cluster02_v3",
                "cluster": "cluster02",
                "version": "v3",
                "author": "Legal Team",
                "date": "2023-03-01",
                "source_type": "policy",
                "regulatory_domain": "GDPR",
                "content": "---\nauthor: Legal Team\ndate: 2023-03-01\nversion: v3\nsource_type: policy\nregulatory_domain: GDPR\n---\nPolicy X approved 2023.",
            },
        ],
    }

    response = client.post("/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["score"] >= 0
    assert "DATE_CONFLICT" in data["flags"]
    assert data["lineage_chains"]
    assert any(entry["source_id"] == "cluster02_v2" for entry in data["source_scores"])

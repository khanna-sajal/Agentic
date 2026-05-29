from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .compliance import evaluate_compliance
from .conflict import extract_conflicts
from .provenance import build_lineage_graph, parse_source_document
from .schemas import EvaluateRequest, TrustSignalResponse
from .trustsignal import build_trust_signal

app = FastAPI(title="THEMIS TrustSignal Evaluation API")


@app.post("/evaluate", response_model=TrustSignalResponse)
def evaluate(request: EvaluateRequest):
    try:
        sources = [parse_source_document(source.model_dump()) for source in request.sources]
        lineage_graph = build_lineage_graph(sources)
        conflicts = extract_conflicts(sources)
        rule_matches = evaluate_compliance(conflicts, sources)
        trust_signal = build_trust_signal(sources, conflicts, rule_matches, lineage_graph)
        return trust_signal
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

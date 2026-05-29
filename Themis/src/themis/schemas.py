from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field


class SourceInput(BaseModel):
    id: str
    cluster: str
    version: str
    author: str
    date: str
    source_type: str
    regulatory_domain: str
    content: str
    parent_ids: List[str] = Field(default_factory=list)


class EvaluateRequest(BaseModel):
    query: str
    rag_answer: str
    sources: List[SourceInput]


class ConflictOutput(BaseModel):
    doc_a: str
    doc_b: str
    conflicting_claim: str
    claim_a: str
    claim_b: str
    conflict_type: str
    evidence: List[str]
    rule_id: str | None = None


class RuleMatchOutput(BaseModel):
    rule_id: str
    description: str
    trigger_conditions: str
    evidence: List[str]
    source_ids: List[str]
    domain: str | None = None


class SourceEvidence(BaseModel):
    source_id: str
    lineage: List[str]
    conflicts: List[ConflictOutput]
    rule_matches: List[RuleMatchOutput]


class LineageNode(BaseModel):
    id: str
    version: str
    author: str
    date: str
    source_type: str
    regulatory_domain: str


class LineageChain(BaseModel):
    chain_id: str
    nodes: List[LineageNode]


class SourceScoreOutput(BaseModel):
    source_id: str
    score: float
    reason: str


class TrustSignalResponse(BaseModel):
    score: float
    flags: List[str]
    evidence: List[SourceEvidence]
    lineage_chains: List[LineageChain]
    source_scores: List[SourceScoreOutput]

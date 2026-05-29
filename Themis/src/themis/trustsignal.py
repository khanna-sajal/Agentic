from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, Iterable, List, Optional

from .compliance import RuleMatch
from .conflict import Conflict
from .provenance import LineageGraph, SourceDocument


@dataclass
class SourceScore:
    source_id: str
    score: float
    reason: str

    def to_dict(self) -> Dict[str, object]:
        return {"source_id": self.source_id, "score": self.score, "reason": self.reason}


def _parse_date(value: str) -> Optional[datetime]:
    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y"]:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def _normalize_recency(source: SourceDocument, sources: Iterable[SourceDocument]) -> float:
    dates = [_parse_date(s.date) for s in sources if _parse_date(s.date)]
    if not dates:
        return 0.5
    dates = sorted(dates)
    source_date = _parse_date(source.date)
    if source_date is None:
        return 0.5
    if source_date <= dates[0]:
        return 0.2
    if source_date >= dates[-1]:
        return 1.0
    rank = dates.index(source_date)
    return 0.2 + 0.8 * rank / max(1, len(dates) - 1)


def _metadata_completeness(source: SourceDocument) -> float:
    fields = [source.author, source.date, source.version, source.source_type, source.regulatory_domain]
    filled = sum(bool(value) for value in fields)
    return filled / len(fields)


def _authority_score(source: SourceDocument) -> float:
    authority = {
        "policy": 1.0,
        "regulation": 1.0,
        "guidance": 0.75,
        "notice": 0.7,
    }
    return authority.get(source.source_type.lower(), 0.7)


def _conflict_consistency(source: SourceDocument, conflicts: Iterable[Conflict]) -> float:
    if any(source.id == conflict.doc_a or source.id == conflict.doc_b for conflict in conflicts):
        return 0.0
    return 1.0


def compute_source_score(source: SourceDocument, sources: Iterable[SourceDocument], conflicts: Iterable[Conflict]) -> SourceScore:
    recency = _normalize_recency(source, sources)
    metadata = _metadata_completeness(source)
    authority = _authority_score(source)
    consistency = _conflict_consistency(source, conflicts)
    score = 0.35 * recency + 0.3 * metadata + 0.2 * authority + 0.15 * consistency
    score = max(0.0, min(1.0, score))
    reason = (
        f"recency={recency:.2f}, metadata={metadata:.2f}, authority={authority:.2f}, "
        f"consistency={consistency:.2f}"
    )
    return SourceScore(source_id=source.id, score=round(score, 3), reason=reason)


def build_lineage_chains(lineage_graph: LineageGraph) -> List[Dict[str, object]]:
    chains = []
    for index, path in enumerate(lineage_graph.chains(), start=1):
        chains.append(
            {
                "chain_id": f"chain_{index}",
                "nodes": [
                    {
                        "id": node.id,
                        "version": node.version,
                        "author": node.author,
                        "date": node.date,
                        "source_type": node.source_type,
                        "regulatory_domain": node.regulatory_domain,
                    }
                    for node in path
                ],
            }
        )
    return chains


def build_trust_signal(
    sources: Iterable[SourceDocument],
    conflicts: Iterable[Conflict],
    rule_matches: Iterable[RuleMatch],
    lineage_graph: LineageGraph,
) -> Dict[str, object]:
    source_list = list(sources)
    source_scores = [compute_source_score(source, source_list, conflicts) for source in source_list]
    overall_score = round(sum(score.score for score in source_scores) / max(1, len(source_scores)), 3)
    flags = {conflict.conflict_type for conflict in conflicts}
    if any(rule_matches):
        flags.add("COMPLIANCE_RISK")
    evidence = []
    rules_by_source = {source_id: [] for source_id in [source.id for source in source_list]}
    for rule in rule_matches:
        for source_id in rule.source_ids:
            rules_by_source.setdefault(source_id, []).append(rule.to_dict())

    for source in source_list:
        source_evidence = {
            "source_id": source.id,
            "lineage": lineage_graph.ancestors(source.id) + [source.id],
            "conflicts": [conflict.to_dict() for conflict in conflicts if conflict.doc_a == source.id or conflict.doc_b == source.id],
            "rule_matches": rules_by_source.get(source.id, []),
        }
        evidence.append(source_evidence)

    return {
        "score": overall_score,
        "flags": sorted(flags),
        "evidence": evidence,
        "lineage_chains": build_lineage_chains(lineage_graph),
        "source_scores": [score.to_dict() for score in source_scores],
    }

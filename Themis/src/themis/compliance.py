from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Sequence

from .conflict import Conflict
from .provenance import SourceDocument


@dataclass
class RuleMatch:
    rule_id: str
    description: str
    trigger_conditions: str
    evidence: List[str]
    source_ids: List[str]
    domain: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        return {
            "rule_id": self.rule_id,
            "description": self.description,
            "trigger_conditions": self.trigger_conditions,
            "evidence": self.evidence,
            "source_ids": self.source_ids,
            "domain": self.domain,
        }


def _find_domain(source_map: Dict[str, SourceDocument], conflict: Conflict) -> Optional[str]:
    a_doc = source_map.get(conflict.doc_a)
    b_doc = source_map.get(conflict.doc_b)
    if a_doc and a_doc.regulatory_domain:
        return a_doc.regulatory_domain
    if b_doc and b_doc.regulatory_domain:
        return b_doc.regulatory_domain
    return None


def evaluate_compliance(conflicts: Sequence[Conflict], sources: Sequence[SourceDocument]) -> List[RuleMatch]:
    source_map = {source.id: source for source in sources}
    matches: List[RuleMatch] = []
    for conflict in conflicts:
        domain = _find_domain(source_map, conflict)
        if conflict.conflict_type == "DATE_CONFLICT":
            if domain in {"GDPR", "data retention", "IP law"}:
                matches.append(
                    RuleMatch(
                        rule_id="RULE_DATE_CONFLICT",
                        description="A date-related claim differs across versions in a regulated domain.",
                        trigger_conditions=f"conflict_type == DATE_CONFLICT and regulatory_domain == {domain}",
                        evidence=conflict.evidence,
                        source_ids=[conflict.doc_a, conflict.doc_b],
                        domain=domain,
                    )
                )
        elif conflict.conflict_type == "VERSION_MISMATCH":
            if domain in {"GDPR", "data retention", "IP law"}:
                matches.append(
                    RuleMatch(
                        rule_id="RULE_VERSION_MISMATCH",
                        description="A version mismatch has been detected for a regulated domain.",
                        trigger_conditions=f"conflict_type == VERSION_MISMATCH and regulatory_domain == {domain}",
                        evidence=conflict.evidence,
                        source_ids=[conflict.doc_a, conflict.doc_b],
                        domain=domain,
                    )
                )
        else:
            if domain in {"GDPR", "data retention", "IP law"}:
                matches.append(
                    RuleMatch(
                        rule_id="RULE_COMPLIANCE_RISK",
                        description="A compliance risk was detected in an undetermined conflict type.",
                        trigger_conditions=f"conflict_type == {conflict.conflict_type} and regulatory_domain == {domain}",
                        evidence=conflict.evidence,
                        source_ids=[conflict.doc_a, conflict.doc_b],
                        domain=domain,
                    )
                )
    return matches

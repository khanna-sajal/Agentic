# Contract: Compliance Engine

## Purpose
Evaluate documents against rule-based regulatory taxonomy and produce risk findings.

## Interfaces
- `evaluate_document(document_id)` -> ComplianceRiskReport
- `list_rules(domain)` -> list of rule definitions
- `reload_taxonomy()` -> reload `regulatory_domains.yaml`

## ComplianceRiskReport
- `document_id`, `overall_risk`, `risks` (list of {rule_id, severity, description, evidence}), `recommendations`

## Rule Format
- YAML with fields: `id`, `description`, `severity`, `check` (field expression)

## Scoring
- 1+ HIGH = HIGH; else if any MEDIUM and no HIGH = MEDIUM; else LOW

## Performance
- Evaluate 100 documents in <10s

## Example
- `evaluate_document('cluster01_v2')` -> returns detailed report with rule evidence

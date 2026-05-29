# Contract: Conflict Detection

## Purpose
Detect and report contradictions between documents or document versions.

## Interfaces
- `detect_conflicts(document_ids, domain=None)` -> list of Conflict objects
- `report_conflict(conflict_id)` -> detailed conflict report with evidence

## Conflict Object
- `conflict_id`, `type`, `documents`, `conflicting_content`, `evidence`, `severity`, `detected_by`

## Detection Flow
1. Exact matching phase: find identical claim strings across documents
2. Semantic phase: for unmatched but similar claims, use Groq extraction + embeddings similarity
3. Aggregate results and assign severity

## Output
- Conflicts include source references to exact chunk locations and reason for detection

## Performance
- Batched conflict detection for N documents should scale linearly with document pairs; semantic phase is best-effort and cacheable

## Example
- `detect_conflicts(['cluster01_v1', 'cluster01_v2'])` -> returns conflict list with evidence

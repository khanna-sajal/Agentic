# Feature Specification: LLM-Powered Claim Extraction & Semantic Similarity

**Feature Branch**: `Provenance_Officer` (or feature branch of choice)

**Created**: May 29, 2026

**Status**: Draft

**Input**: Add LLM-powered claim extraction and semantic similarity to improve detection of paraphrased claims, fuzzy matches, and subtle contradictions across document versions. This feature complements the existing deterministic extractor and rule engine.

## Short Name
`llm-claim-extraction`

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Improve Claim Recall for Paraphrases (Priority: P1)

A compliance analyst queries a claim that appears with varied wording across versions (e.g., "approved in 2021" vs "ratified a year earlier"). The LLM-enhanced extractor should normalize paraphrases into canonical claims (e.g., `approval_year`) so conflicts and lineage are reliably identified.

**Independent Test**: Given three sources with paraphrased approval statements, the system extracts the same canonical claim key and detects any differing values.

**Acceptance Scenarios**:
1. **Given** sources with paraphrased claim text, **When** LLM extractor runs, **Then** claim keys match canonical forms and are comparable.
2. **Given** an ambiguous statement, **When** deterministic extractor fails but LLM returns a high-confidence claim, **Then** LLM output is included with provenance and prompt used.

---

### User Story 2 - Semantic Similarity for Soft Conflicts (Priority: P1)

A compliance officer needs to detect when two statements conflict semantically rather than lexically (e.g., "retain data 1 year" vs "retain data up to 12 months"). The semantic similarity module should surface near-equivalent claims and flag potential conflicts requiring human review.

**Independent Test**: For pairs of statements with high semantic similarity but different numeric values, the system produces a similarity score and a recommendation (auto-resolve if within tolerance, otherwise flag).

---

### User Story 3 - Explainability & Prompt Capture (Priority: P2)

Auditors require that LLM inferences are reproducible and auditable. The system must capture the model prompt, model name/version, temperature, and the extracted claim with confidence score.

**Independent Test**: Verify extraction records include `model`, `prompt`, `temperature`, `confidence`, and the raw LLM response.

---

### User Story 4 - Hybrid Pipeline & Fallback (Priority: P2)

Operations require a hybrid pipeline: deterministic extraction first, LLM only when deterministic fails or low confidence. LLM use should be configurable per-request (toggle on/off) and per-domain (cost control).

**Independent Test**: With LLM toggle off, outputs match current deterministic extractor. With toggle on, LLM augments missing claims.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-LLM-001**: System MUST provide an optional LLM-based claim extractor that returns canonical claim keys, claim values, confidence, and extraction rationale.
- **FR-LLM-002**: System MUST compute semantic similarity scores between claim texts and expose them in conflict objects.
- **FR-LLM-003**: System MUST capture and persist LLM metadata (model name/version, prompt, temperature, timestamp) alongside extracted claims.
- **FR-LLM-004**: System MUST implement a hybrid pipeline: deterministic extractor → LLM fallback → merge results with provenance.
- **FR-LLM-005**: System MUST allow per-request and per-domain toggling of LLM usage and set cost/latency constraints.
- **FR-LLM-006**: System MUST expose extraction confidence and similarity thresholds that determine auto-resolution vs human review.
- **FR-LLM-007**: System MUST keep LLM outputs auditable and reproducible (store prompts and deterministic seeds where applicable).
- **FR-LLM-008**: System MUST include a safety filter to redact potentially sensitive content before sending to external LLMs.

### Non-Functional Requirements

- **NFR-LLM-001**: LLM-enhanced extraction end-to-end latency must be configurable; default acceptable demo latency: <1.5s per document (subject to provider variability).
- **NFR-LLM-002**: Costs must be controllable via per-domain toggles and batch inference options.
- **NFR-LLM-003**: Privacy and compliance: PII must be redacted before external API calls unless user explicitly permits.

## Success Criteria *(mandatory)*

- **SC-LLM-001**: Extraction recall for paraphrased claims improves by at least 25% over deterministic-only baseline on a held-out test set.
- **SC-LLM-002**: Semantic similarity produces scores correlated with human judgments (Spearman rho > 0.7 in evaluation sample).
- **SC-LLM-003**: All LLM-based extractions include captured prompt and metadata for every inference.
- **SC-LLM-004**: Toggle and fallback behavior validated: deterministic-only mode produces identical results to current system.

## Assumptions

- Access to an LLM provider (API key, model availability) or local LLM runtime is available.
- Users accept that LLM calls may incur latency and monetary cost; toggles control usage.
- The current canonical claim taxonomy is extendable to accommodate LLM-discovered claim types.

## Risks & Mitigations

- **Risk**: LLM hallucination leads to incorrect claims. **Mitigation**: Always attach confidence, require deterministic corroboration for high-severity flags, and provide human review workflows.
- **Risk**: PII leakage to external APIs. **Mitigation**: Apply automated PII redaction and explicit consent flows.

## Deliverables

- `specs/002-llm-claim-extraction/spec.md` (this file)
- `specs/002-llm-claim-extraction/checklists/requirements.md` (quality checklist)
- Implementation plan (if requested) and tasks to follow `/speckit.plan`

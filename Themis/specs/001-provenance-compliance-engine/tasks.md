---

description: "Generated task list for Provenance & Compliance Intelligence Engine"
---

# Tasks: Provenance & Compliance Intelligence Engine

**Input**: plan.md, spec.md, research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Create project structure per implementation plan in src/ and specs/ (create folders: src/themis, src/themis/parser, src/themis/lineage, src/themis/conflict_detector, src/themis/compliance, src/themis/audit, src/themis/api)
- [ ] T002 Initialize Python project and ensure `requirements.txt` includes PyYAML, networkx, fastapi, uvicorn, pytest, groq-client (or placeholder), pytest-cov
- [ ] T003 [P] Configure linting and formatting: add `.pre-commit-config.yaml` and `pyproject.toml` with black/isort/ruff

---

## Phase 2: Foundational (Blocking Prerequisites)

- [X] T004 Setup SQLite schema and migrations framework (create `src/themis/db/` and Alembic/placeholder migration scripts)
- [X] T005 [P] Implement configuration loader and add `specs/001-provenance-compliance-engine/config/regulatory_domains.yaml` and `src/themis/config/settings.py`
- [X] T006 [P] Implement YAML metadata parser in `src/themis/parser/yaml_metadata_parser.py` (required by US1)
- [X] T007 [P] Implement document intake and chunking pipeline in `src/themis/parser/document_intake.py` and `src/themis/parser/schema_validator.py`
- [X] T008 Implement NetworkX-based version graph in `src/themis/lineage/version_graph.py` (required by US2)
- [X] T009 [P] Implement audit hash chain and logger in `src/themis/audit/hash_chain.py` and `src/themis/audit/audit_logger.py` (required by US5)
- [X] T010 Create test scaffolding and fixtures in `tests/conftest.py` and add sample corpus fixtures under `tests/fixtures/`

---

## Phase 3: User Story 1 - Ingest and Extract Document Metadata (Priority: P1) 🎯 MVP

**Goal**: Ingest documents from `/corpus` and extract YAML front-matter into structured JSON metadata for provenance.

**Independent Test**: Ingest sample corpus and verify extracted metadata for `author`, `date`, `version`, `source_type`, `regulatory_domain`.

- [ ] T011 [P] [US1] Add unit tests for YAML parser in `tests/unit/test_yaml_parser.py`
- [ ] T012 [US1] Implement `src/themis/parser/yaml_metadata_parser.py` to extract YAML front-matter and return validated metadata JSON
- [ ] T013 [US1] Implement `src/themis/parser/schema_validator.py` to validate required fields and emit structured errors
- [ ] T014 [US1] Integrate parser into `src/themis/parser/document_intake.py` and write ingestion flow that scans `corpus/` and registers documents in DB
- [ ] T015 [US1] Add contract test `tests/contract/test_metadata_parser_contract.py` that confirms required output shape per contracts/metadata-parser.md
- [ ] T016 [US1] Add CLI/invocation script `src/themis/parser/cli_ingest.py` to run a local ingestion (used by quickstart)

---

## Phase 4: User Story 2 - Track Document Version History and Source Lineage (Priority: P1)

**Goal**: Store and query immutable version lineage for documents and tag chunks with provenance.

**Independent Test**: Ingest multiple versions and verify lineage and chunk provenance returned by lineage queries.

- [ ] T017 [P] [US2] Add unit tests for version graph in `tests/unit/test_version_graph.py`
- [ ] T018 [US2] Implement `src/themis/lineage/version_graph.py` using NetworkX DiGraph to model versions and edges
- [ ] T019 [US2] Implement `src/themis/lineage/provenance_tracker.py` to tag chunks and answers with document_id/version/offset
- [ ] T020 [US2] Implement Version Comparison API in `src/themis/api/version_api.py` (endpoint: GET `/api/v1/versions/compare`)
- [ ] T021 [US2] Add contract test `tests/contract/test_provenance_lineage_contract.py` to validate lineage API responses

---

## Phase 5: User Story 3 - Detect Contradictory Claims Across Documents (Priority: P2)

**Goal**: Identify contradictory claims with exact-match-first approach and Groq-based semantic fallback.

**Independent Test**: Run conflict detection on known conflicting corpus pairs and verify reported conflicts include evidence and source references.

- [ ] T022 [P] [US3] Implement exact string matcher in `src/themis/conflict_detector/exact_matcher.py`
- [ ] T023 [US3] Implement semantic validator interface in `src/themis/conflict_detector/semantic_validator.py` (Groq client wrapper + caching)
- [ ] T024 [US3] Implement conflict aggregation and report generation in `src/themis/conflict_detector/conflict_report.py`
- [ ] T025 [US3] Add unit tests `tests/unit/test_exact_matcher.py` and `tests/unit/test_semantic_validator.py` (semantic tests may mock Groq)
- [ ] T026 [US3] Add Conflict Report API in `src/themis/api/conflict_api.py` (endpoint: GET `/api/v1/conflicts`)

---

## Phase 6: User Story 4 - Assess Compliance Risk and Regulatory Gaps (Priority: P2)

**Goal**: Evaluate documents against YAML-defined rules and produce risk assessments with evidence.

**Independent Test**: Evaluate sample documents and verify rule violations and overall risk classification.

- [ ] T027 [P] [US4] Add `specs/001-provenance-compliance-engine/config/regulatory_domains.yaml` with sample rules (HIPAA, GDPR, SOX)
- [ ] T028 [US4] Implement `src/themis/compliance/rule_engine.py` to evaluate rule expressions against metadata/chunks
- [ ] T029 [US4] Implement `src/themis/compliance/risk_scorer.py` to aggregate violations into LOW/MEDIUM/HIGH
- [ ] T030 [US4] Add unit tests `tests/unit/test_rule_engine.py` and `tests/unit/test_risk_scorer.py`
- [ ] T031 [US4] Implement Compliance Risk Report API in `src/themis/api/compliance_api.py` (endpoint: GET `/api/v1/compliance-risk`)

---

## Phase 7: User Story 5 - Generate Audit-Ready Traceability Logs (Priority: P2)

**Goal**: Produce append-only audit logs for retrievals with SHA-256 chain for tamper detection.

**Independent Test**: Perform multiple retrievals, then run verification to detect tampering if entries are modified.

- [ ] T032 [P] [US5] Implement `src/themis/audit/hash_chain.py` to compute and verify chained SHA-256 hashes
- [ ] T033 [US5] Implement `src/themis/audit/audit_logger.py` to append entries and persist `previous_hash`
- [ ] T034 [US5] Add unit test `tests/unit/test_hash_chain.py` and integration `tests/integration/test_audit_trail.py`

---

## Phase 8: Polish & Cross-Cutting Concerns

- [ ] T035 Documentation: update `specs/001-provenance-compliance-engine/quickstart.md` and write `docs/provenance_compliance_guide.md`
- [ ] T036 [P] Add integration test `tests/integration/test_document_flow.py` for end-to-end ingest → parse → lineage → conflict → compliance
- [ ] T037 Run full test suite and address failures (`pytest -q`)
- [ ] T038 Performance tuning and caching (provenance graph and Groq response cache)

---

## Dependencies & Execution Order

- Setup (Phase 1) must run first
- Foundational (Phase 2) tasks block user stories; complete T004–T010 before US1/US2/US5
- User stories US1 and US2 (P1) should be implemented immediately after Foundational tasks
- US3–US5 (P2) can be implemented after Foundational tasks; semantic validator (T023) depends on Groq credentials and may be mocked in tests
- Final polish tasks depend on all user stories completion

## Parallel Opportunities

- Tasks marked `[P]` can be done in parallel by different engineers (e.g., parser, NetworkX graph, audit module)
- User stories themselves can be executed in parallel after Foundational tasks complete

## Task Counts & Summary

- Total tasks: 38
- P1 story tasks (US1, US2) prioritized for MVP
- Parallel opportunities: multiple `[P]` tasks across foundational and story phases

## Implementation Strategy

- MVP: Complete Phase 1 + Phase 2 + Phase 3 (US1) and Phase 4 (US2) first
- Validate by running contract tests and the integration `test_document_flow.py`
- Incrementally implement US3–US5 and expose APIs

---

## Files created by this command
- `specs/001-provenance-compliance-engine/tasks.md`


**End of generated tasks.md**

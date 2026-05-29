# Tasks: Document Provenance Tracing & Conflict Detection

**Input**: Design documents from `specs/001-provenance-conflict-detection/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize the project feature and dependencies for provenance, lineage, conflict, and compliance evaluation.

- [x] T001 Create `specs/001-provenance-conflict-detection/tasks.md` from the tasks template
- [x] T002 Update `requirements.txt` to include `PyYAML`, `pydantic`, `fastapi`, and `httpx2`
- [x] T003 [P] Add or update `README.md` and `specs/001-provenance-conflict-detection/quickstart.md` with the evaluation workflow

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the core provenance and evaluation infrastructure required by all user stories.

- [x] T004 [P] Extend `src/themis/provenance.py` with robust YAML front-matter parsing and `SourceDocument` metadata extraction
- [x] T005 [P] Add provenance graph support in `src/themis/provenance.py` to model immutable version lineage
- [x] T006 [P] Create `src/themis/conflict.py` support for structured conflict objects and claim-level mismatch detection
- [x] T007 [P] Create `src/themis/compliance.py` with rule-based compliance evaluation for regulatory domains
- [x] T008 [P] Create `src/themis/trustsignal.py` or equivalent payload builder to standardize TrustSignal output
- [x] T009 Add baseline unit tests in `tests/test_provenance.py` and `tests/test_conflict.py` for new provenance and conflict primitives
- [x] T010 Add contract docs in `specs/001-provenance-conflict-detection/contracts/evaluate-api.md` and `specs/001-provenance-conflict-detection/contracts/trustsignal-schema.md`

---

## Phase 3: User Story 1 - Detect Conflicting Claims Across Document Versions (Priority: P1) 🎯 MVP

**Goal**: Detect and report claim-level contradictions across source versions, including the demo conflict between cluster 02 v1 and v3.

**Independent Test**: Verify a cluster 02 query returns `DATE_CONFLICT` for approval year mismatch and includes both source claims.

- [x] T011 [US1] Implement `SourceDocument` loading and claim normalization in `src/themis/provenance.py`
- [x] T012 [US1] Implement lineage-aware claim comparison in `src/themis/conflict.py`
- [x] T013 [US1] Add structured conflict output with `doc_a`, `doc_b`, `conflicting_claim`, `claim_a`, `claim_b`, and `conflict_type` in `src/themis/conflict.py`
- [x] T014 [US1] Add unit test for demo cluster 02 conflict detection in `tests/test_conflict.py`
- [x] T015 [US1] Add integration test for source pair `cluster02_v1` vs `cluster02_v3` in `tests/test_conflict.py`

---

## Phase 4: User Story 2 - Evaluate Trust Score of Document Versions (Priority: P1)

**Goal**: Rank competing sources with a composite trust score and surface the most authoritative version.

**Independent Test**: Verify v2 receives the highest score (target 0.9) against v1 and v3 in a cluster 02 demo.

- [x] T016 [US2] Implement trust score calculation in `src/themis/trustsignal.py` using recency, metadata completeness, source authority, and consistency
- [x] T017 [P] [US2] Add per-source score reasoning in `src/themis/trustsignal.py`
- [x] T018 [US2] Add unit test for trust score ranking in `tests/test_trustsignal.py`
- [x] T019 [US2] Extend TrustSignal payload support in `specs/001-provenance-conflict-detection/contracts/trustsignal-schema.md`

---

## Phase 5: User Story 3 - Trace Provenance "Lineage Chain" to Audit Source Origin (Priority: P2)

**Goal**: Produce an explicit lineage chain from origin through all versions for auditability.

**Independent Test**: Verify provenance chain output shows v1 → v2 → v3 with metadata for each node.

- [x] T020 [US3] Implement lineage chain generation in `src/themis/provenance.py`
- [x] T021 [P] [US3] Add lineage chain serialization to TrustSignal output in `src/themis/trustsignal.py`
- [x] T022 [US3] Add unit test for lineage chain generation in `tests/test_provenance.py`

---

## Phase 6: User Story 4 - Flag Regulatory & Compliance Risks (Priority: P2)

**Goal**: Map detected conflicts to explicit compliance risk flags and rule-based findings.

**Independent Test**: Verify `COMPLIANCE_RISK` and `VERSION_MISMATCH` are triggered for conflicting GDPR or data retention claims.

- [x] T023 [US4] Implement compliance rule matching in `src/themis/compliance.py`
- [x] T024 [P] [US4] Define regulatory rules for GDPR, data retention, and IP law in `src/themis/compliance.py`
- [x] T025 [US4] Add flag generation for `COMPLIANCE_RISK` and `VERSION_MISMATCH` in `src/themis/conflict.py`
- [x] T026 [US4] Add unit test for compliance risk labeling in `tests/test_compliance.py`

---

## Phase 7: User Story 5 - Evaluate Multiple Sources via POST /evaluate Endpoint (Priority: P1)

**Goal**: Expose the evaluation feature via a stable API endpoint and return structured TrustSignal JSON.

**Independent Test**: Verify `POST /evaluate` returns `score`, `flags`, `evidence`, and `lineage_chains` for a demo request.

- [x] T027 [US5] Implement `POST /evaluate` endpoint in `src/themis/api.py`
- [x] T028 [US5] Add request/response schemas in `src/themis/schemas.py`
- [x] T029 [US5] Add contract/integration test for `POST /evaluate` in `tests/test_api.py`
- [x] T030 [US5] Validate the API contract against `specs/001-provenance-conflict-detection/contracts/evaluate-api.md`

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Clean up, document, and validate the feature across stories.

- [x] T031 [P] Update documentation and quickstart examples in `specs/001-provenance-conflict-detection/quickstart.md`
- [x] T032 [P] Run `pytest` and fix any regression errors
- [x] T033 [P] Refactor code for explicit evidence chains and deterministic output in `src/themis/`
- [x] T034 [P] Add or update `tests/test_provenance.py`, `tests/test_conflict.py`, and `tests/test_api.py` to cover all user-story behaviors
- [x] T035 [P] Ensure `specs/001-provenance-conflict-detection/contracts/trustsignal-schema.md` and API docs stay synchronized with implementation

---

## Dependencies & Execution Order

- **Phase 1**: Start immediately
- **Phase 2**: Must complete before any user story work begins
- **Phase 3**: Depends on Phase 2
- **Phase 4**: Depends on Phase 2
- **Phase 5**: Depends on Phase 2
- **Phase 6**: Depends on Phase 2
- **Phase 7**: Depends on Phase 2
- **Phase 8**: Depends on all user stories being implemented

### Parallel Opportunities

- Setup tasks (`T002`, `T003`) can run in parallel
- Foundational tasks (`T004`-`T010`) can run in parallel where they touch different files
- User story implementation can proceed in parallel after Phase 2
- Tests marked `[P]` can run in parallel within each story

# Implementation Plan: Provenance & Compliance Intelligence Engine

**Branch**: `001-provenance-compliance-engine` | **Date**: May 29, 2026 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-provenance-compliance-engine/spec.md`

## Summary

The Provenance & Compliance Intelligence Engine is a modular system for RAG document intake, metadata extraction, version lineage tracking, and compliance risk analysis. The system will automatically scan the `/corpus` directory, extract YAML front-matter metadata (author, date, version, source_type, regulatory_domain), track document version history using NetworkX-based provenance graphs, detect contradictory claims using Groq NLP with exact-match-first fallback, and assess compliance risks using rule-based evaluation against a configurable regulatory domain taxonomy. All operations maintain cryptographic audit trails via SHA-256 hash chains, exposing REST APIs for provenance lookup, version comparison, conflict reports, and compliance risk assessment.

## Technical Context

**Language/Version**: Python 3.11+ (aligns with existing THEMIS codebase)

**Primary Dependencies**:
- YAML parsing: `PyYAML` for metadata extraction
- Version lineage: `NetworkX` for directed acyclic graph (DAG) representation of document versions
- Conflict detection: `Groq` API for LLM-based claim extraction and semantic similarity
- Compliance engine: Rule-based custom module (in-house)
- API framework: `FastAPI` for REST endpoints
- Cryptographic hashing: `hashlib` (stdlib) for SHA-256 hash chains
- Data persistence: SQLite (initial) with migration path to PostgreSQL for production
- Testing: `pytest` with plugins for unit, integration, and provenance testing

**Storage**: 
- Metadata and provenance graph: SQLite initially, upgradeable to PostgreSQL with Alembic migrations
- Vector index integration: Via existing RAG system's vector store (extended with provenance fields)
- Audit logs: Append-only database table with SHA-256 hash chains
- Configuration: YAML files for regulatory domain taxonomy (`regulatory_domains.yaml`)

**Testing**: pytest + pytest-cov (unit tests, integration tests, contract tests, provenance lineage verification, conflict detection validation)

**Target Platform**: Linux servers (same as THEMIS backend); RESTful API-first design allows future mobile clients

**Project Type**: Library component + REST API service (embedded in THEMIS backend)

**Performance Goals**:
- Document ingestion: Process 100 documents in <5 seconds (batch)
- Metadata extraction: Extract YAML + validate schema in <100ms per document
- Version lineage graph traversal: Complete comparison of 10 versions in <2 seconds (SC-005)
- Conflict detection: Identify 95%+ of conflicts with <500ms latency per document pair (SC-003, SC-007)
- Compliance risk analysis: Score 100 documents for risk in <10 seconds
- API response time: <500ms for 99% of requests (SC-007)

**Constraints**:
- Audit logs must be tamper-proof: SHA-256 cryptographic verification for all entries
- Version history immutability: No overwrites; all updates create new versions
- Conflict detection must be explainable: Reasons for conflict must be documentable
- Compliance rule mapping: Every risk must be traceable to a rule in the taxonomy
- Graceful YAML handling: Malformed YAML logs error but does NOT stop corpus processing
- Regulatory domain configuration: Non-developers must be able to add/update domains without code changes

**Scale/Scope**:
- Initial corpus: 5 clusters × 3 versions = 15 documents (fits in development; production scalable to thousands)
- Supported regulatory domains: Minimum 3 (HIPAA, GDPR, SOX); extensible
- Concurrent users: Compliance team of 5-10; RESTful design scales to 100+ queries/day
- Data retention: All audit logs retained for compliance review (no deletion/purge policy)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### THEMIS Constitution Alignment

| Principle | Feature Compliance | Evidence |
|-----------|-------------------|----------|
| **Evidence-First Provenance** | ✅ COMPLIANT | Every chunk, answer, and conflict is tagged with document metadata (ID, version, author, date). Hash chains on audit logs provide complete traceability. FR-006, FR-013, FR-014, FR-018 mandate source lineage |
| **Immutable Version Lineage** | ✅ COMPLIANT | NetworkX DAG stores all versions as immutable nodes. New versions link to parent via edges. No overwrites; metadata captures timestamp, author, origin. Supports SC-002 requirement for complete provenance chains |
| **Explicit Conflict Detection** | ✅ COMPLIANT | Two-phase conflict detection (exact matching → semantic similarity) explicitly documents reasoning. Conflict Report API (FR-016) includes conflicting sources, content, and rationale. No opaque scoring |
| **Compliance Risk Rule Mapping** | ✅ COMPLIANT | All risks map to regulatory domain rules (FR-011, FR-012). Rule-based checker validates against taxonomy. Risk severity (LOW/MEDIUM/HIGH) tied to specific rule violations and evidence |
| **Quality, Testing, UX, Performance** | ✅ COMPLIANT | Modular APIs (FR-014–FR-017), unit tests for parsers/conflict/risk (FR-020), human-readable outputs (conflict summaries, audit logs), performance targets in spec (SC-001–SC-010) |

**Gate Status**: ✅ **PASS** — Feature fully aligns with THEMIS constitution. No violations or tradeoffs.

## Project Structure

### Documentation (this feature)

```text
specs/001-provenance-compliance-engine/
├── plan.md                              # This file
├── research.md                          # Phase 0: Research on Groq integration, NetworkX usage patterns
├── data-model.md                        # Phase 1: Metadata schema, conflict representation, graph structure
├── quickstart.md                        # Phase 1: Setup, configuration, example API calls
├── contracts/
│   ├── metadata-parser.md               # Contract: YAML extraction, validation
│   ├── provenance-lineage.md            # Contract: DAG construction, traversal
│   ├── conflict-detection.md            # Contract: Conflict identification and reporting
│   ├── compliance-engine.md             # Contract: Rule evaluation and risk scoring
│   └── audit-logging.md                 # Contract: Hash chain construction and verification
└── checklists/
    └── requirements.md                  # Quality validation (already created)
```

### Source Code (repository root)

```text
src/themis/
├── __init__.py
├── conflict.py                          # Existing conflict detection module (will extend)
├── provenance.py                        # Existing provenance module (will extend)
├── parser/
│   ├── __init__.py
│   ├── yaml_metadata_parser.py          # YAML front-matter extraction and validation
│   ├── document_intake.py               # Corpus scanning and document registration
│   └── schema_validator.py              # YAML schema consistency checker
├── lineage/
│   ├── __init__.py
│   ├── version_graph.py                 # NetworkX-based version DAG
│   ├── provenance_tracker.py            # Source lineage tracking for chunks/answers
│   └── lineage_queries.py               # Graph traversal and comparison queries
├── conflict_detector/
│   ├── __init__.py
│   ├── exact_matcher.py                 # Phase 1: Exact string matching
│   ├── semantic_validator.py            # Phase 2: Groq-based NLP fallback
│   ├── conflict_report.py               # Conflict aggregation and reporting
│   └── conflict_types.py                # Type definitions for different conflict categories
├── compliance/
│   ├── __init__.py
│   ├── regulatory_taxonomy.py           # Load and manage regulatory domain config
│   ├── rule_engine.py                   # Rule-based compliance checker
│   ├── risk_scorer.py                   # Assign risk severity (LOW/MEDIUM/HIGH)
│   └── compliance_report.py             # Risk assessment and remediation recommendations
├── audit/
│   ├── __init__.py
│   ├── hash_chain.py                    # SHA-256 hash chain construction and verification
│   ├── audit_logger.py                  # Append-only audit log with tamper detection
│   └── audit_queries.py                 # Log retrieval and verification
├── api/
│   ├── __init__.py
│   ├── provenance_api.py                # FastAPI endpoints for provenance lookup
│   ├── version_api.py                   # Version comparison API
│   ├── conflict_api.py                  # Conflict report API
│   ├── compliance_api.py                # Compliance risk report API
│   ├── ingest_api.py                    # Document ingestion trigger API
│   └── models.py                        # Pydantic models for request/response schemas
└── config/
    ├── __init__.py
    ├── settings.py                      # Configuration management (batch schedule, thresholds, etc.)
    └── regulatory_domains.yaml          # Domain taxonomy (HIPAA, GDPR, SOX, FDA, PCI-DSS)

tests/
├── unit/
│   ├── test_yaml_parser.py              # Metadata extraction edge cases
│   ├── test_version_graph.py            # NetworkX DAG construction and queries
│   ├── test_exact_matcher.py            # Exact string conflict detection
│   ├── test_semantic_validator.py       # Groq-based conflict detection
│   ├── test_rule_engine.py              # Compliance rule evaluation
│   ├── test_hash_chain.py               # SHA-256 tamper detection
│   └── test_risk_scorer.py              # Risk severity assignment
├── integration/
│   ├── test_document_flow.py            # End-to-end: ingest → parse → lineage → conflict → compliance
│   ├── test_api_endpoints.py            # REST API contract testing
│   └── test_audit_trail.py              # Hash chain accuracy across operations
├── contract/
│   ├── test_metadata_parser_contract.md # Contract: schema validation behavior
│   └── test_conflict_contract.md        # Contract: conflict detection accuracy
└── conftest.py                          # Pytest fixtures, test corpus, mock Groq responses

docs/
└── provenance_compliance_guide.md       # User guide for provenance and compliance features
```

**Structure Decision**: Single-project modular architecture with clear separation of concerns:
- **Parser module** handles document intake and YAML extraction
- **Lineage module** manages version graphs and provenance tracking
- **Conflict detector** implements two-phase detection strategy
- **Compliance module** implements rule-based risk evaluation
- **Audit module** manages cryptographic log integrity
- **API module** exposes REST endpoints
- **Config** manages regulatory domains and system settings

This structure aligns with THEMIS principles (modular APIs, explicit evidence chains) and supports future extensibility (PDF/DOCX parsers can plug into `parser/`; new compliance rules in `config/`).

## Complexity Tracking

| Aspect | Justification | Simpler Alternative Rejection |
|--------|---------------|------------------------------|
| NetworkX for version graphs | DAG structure naturally represents version history with ancestor/descendant relationships; enables efficient lineage queries and cycle detection | Direct parent-child pointers insufficient for visualizing the full version tree or detecting conflicting lineages |
| Groq NLP for semantic detection | Phase 2 fallback after exact matching requires understanding context; Groq API provides low-cost LLM access for claim extraction without on-prem inference | Rule-based string similarity patterns too rigid for regulatory domain language variations |
| SHA-256 hash chains for audit logs | Cryptographic verification required for compliance audit readiness; hash chains provide proof-of-integrity without external PKI | Simple checksums don't prevent tampering; signatures alone require key management overhead |
| Rule-based compliance checker (not ML) | Regulatory compliance requires explainability; rules map directly to domain taxonomy; human-maintainable | ML-based risk scoring violates THEMIS principle "Trust scores alone are forbidden unless accompanied by explicit evidence" |
| SQLite → PostgreSQL migration path | SQLite sufficient for development; clear upgrade path for production scale without re-architecting data layer | SQLite-only design limits horizontal scaling; hardcoding PostgreSQL adds unnecessary setup complexity |

---

## Next Steps

**Phase 0 (Research)**: 
- Research optimal Groq prompt engineering for regulatory claim extraction
- Document NetworkX best practices for DAG versioning patterns
- Define hash chain initialization and verification algorithms

**Phase 1 (Design & Contracts)**:
- Generate `data-model.md` with Metadata, Conflict, Provenance, AuditLog schemas
- Define API contracts in `contracts/` with request/response examples
- Create `quickstart.md` with setup and example usage

**Phase 2 (Tasks)**:
- Decompose into testable implementation tasks with dependencies
- Priority: P1 (parser, lineage), P2 (conflict detection, compliance), P3 (API, audit)

**Status**: ✅ Plan ready for Phase 0 research execution
# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]

**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]

**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]

**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]

**Project Type**: [e.g., library/cli/web-service/mobile-app/compiler/desktop-app or NEEDS CLARIFICATION]

**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]

**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]

**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined based on constitution file]

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

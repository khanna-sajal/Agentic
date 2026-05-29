# Feature Specification: Document Provenance Tracing & Conflict Detection

**Feature Branch**: `Provenance_Officer`

**Created**: May 29, 2026

**Status**: Draft

**Input**: Traces the origin and version history of every source document, detects conflicts between sources (e.g. two docs contradict each other on the same claim), and flags regulatory or compliance risks. Policy, compliance & regulatory domains (GDPR, data retention, IP law, etc.)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Detect Conflicting Claims Across Document Versions (Priority: P1)

A compliance analyst needs to identify when multiple versions of regulatory documents make conflicting claims about the same policy. This is the core value: discovering that v1 says "Policy X approved 2021" and v3 says "2023", which could indicate either an update, a mistake, or a document synchronization issue.

**Why this priority**: Conflicts are the primary risk signal in compliance work. If systems rely on contradictory information, decision-making fails and regulatory exposure increases. P1 is the gate—without conflict detection, the entire trust system is unreliable.

**Independent Test**: Query system with 3 sources from cluster 02 where v1 and v3 contradict on a claim (e.g., approval date). System correctly surfaces the conflict and prevents false confidence.

**Acceptance Scenarios**:

1. **Given** query "When was Policy X approved?" **When** system retrieves v1 (2021), v2 (updates facts), and v3 (2023), **Then** system returns conflict flag `DATE_CONFLICT` with doc_a=v1, doc_b=v3, claim="approval_year"
2. **Given** three versions of a regulatory document **When** v1 and v3 make contradictory claims, **Then** system explicitly surfaces both claims with source lineage
3. **Given** a clean document set with no contradictions **When** query executes, **Then** no conflict flags appear

---

### User Story 2 - Evaluate Trust Score of Document Versions (Priority: P1)

A policy officer needs to know which document version is most trustworthy. The system must rank competing sources by a composite trust score (0–1), allowing the officer to make informed choices about which claim to rely on.

**Why this priority**: Without trust scoring, conflict detection alone is just noise—the user still doesn't know what to believe. Trust scores enable decision-making. Once conflicts are discovered, scoring determines which source wins. This is equally critical to conflict detection.

**Independent Test**: Compare three versions of the same policy; system assigns highest trust score (0.9) to v2 (most recent/authoritative update), lower scores to v1 (original, may be outdated) and v3 (contradicts v1). User can see the reasoning.

**Acceptance Scenarios**:

1. **Given** three versions of a document with different update dates **When** trust scoring evaluates them, **Then** v2 receives highest score (0.9) because it represents the most recent authoritative update
2. **Given** a conflict between v1 and v3 **When** v2 provides factual correction or newer info, **Then** v2's score remains highest
3. **Given** a document with missing metadata (author, date), **When** scoring evaluates it, **Then** score reflects uncertainty (reduced accordingly)

---

### User Story 3 - Trace Provenance "Lineage Chain" to Audit Source Origin (Priority: P2)

A compliance auditor must answer: "Where did this claim originate, has it been updated, and what is the full update chain?" The system must produce a lineage chain showing document origin, versions, and timestamp progression.

**Why this priority**: Provenance tracing is essential for regulatory audits and accountability. However, P2 reflects that once conflicts are detected and scored, lineage becomes a supporting detail rather than the primary decision point. It's mandatory for compliance but secondary to conflict detection flow.

**Independent Test**: Track a single claim through v1 → v2 → v3 across cluster documents. System outputs: origin date, author, update history, version progression, and final state.

**Acceptance Scenarios**:

1. **Given** a policy claim that appears in v1, v2, and v3 **When** user requests evidence lineage, **Then** system returns complete chain: v1 (author: Policy Team, date: 2021-01-15) → v2 (author: Compliance Officer, date: 2022-06-20, change: "approval date updated to 2023") → v3 (author: Legal Team, date: 2023-03-01)
2. **Given** metadata in document YAML front-matter **When** lineage is generated, **Then** all metadata fields (author, date, version, source_type, regulatory_domain) are included in trace
3. **Given** a document with full history **When** auditor exports lineage, **Then** output is machine-readable and human-auditable

---

### User Story 4 - Flag Regulatory & Compliance Risks (Priority: P2)

A compliance manager needs the system to automatically flag when documents contain regulatory risks: mismatches between versions, compliance violations, data retention conflicts, GDPR contradictions, etc.

**Why this priority**: Risk flagging is essential but P2 because it builds on conflict detection (P1). Once we know conflicts exist and trust scores are assigned, we categorize them as compliance risks. This is a classification layer on top of P1/P1 work.

**Independent Test**: Feed documents with known compliance issues (e.g., data retention policy says "delete after 1 year" in v1 but "delete after 5 years" in v3). System flags `COMPLIANCE_RISK` alongside `DATE_CONFLICT` and `VERSION_MISMATCH`.

**Acceptance Scenarios**:

1. **Given** documents from regulatory domains (GDPR, data retention, IP law) **When** conflicts are detected, **Then** system flags: `DATE_CONFLICT`, `VERSION_MISMATCH`, or `COMPLIANCE_RISK` as appropriate
2. **Given** v1 says "retain data 1 year" and v3 says "retain 5 years" **When** query executes on data retention domain, **Then** system flags `VERSION_MISMATCH` and `COMPLIANCE_RISK`
3. **Given** two clusters with regulatory domains **When** both have conflicts, **Then** risk flags appear consistently across clusters

---

### User Story 5 - Evaluate Multiple Sources via POST /evaluate Endpoint (Priority: P1)

A system integrating THEMIS needs a standardized API endpoint to submit a query with RAG answer and source list, and receive structured TrustSignal output.

**Why this priority**: API endpoint is the integration boundary. Without this P1 mechanism, all other features (conflict detection, scoring, flagging) are unreachable to downstream systems. This is critical for demo and production use.

**Independent Test**: POST query + 3 sources to `/evaluate`. Receive JSON response with score, evidence lineage, and flags.

**Acceptance Scenarios**:

1. **Given** POST request to `/evaluate` with query, rag_answer, and sources array (3 items from cluster 02) **When** request is processed, **Then** response contains: score (0–1), evidence lineage (chain per source), flags (DATE_CONFLICT, etc.)
2. **Given** invalid input (missing sources or query), **When** endpoint receives it, **Then** returns 400 with error details
3. **Given** valid input with conflicts **When** endpoint processes, **Then** returns 200 with complete TrustSignal payload

---

### Edge Cases

- What happens when a query has only 1 source? (Answer: No conflicts possible; trust score reflects single source metadata)
- How does the system handle when all three versions (v1, v2, v3) are identical? (Answer: No conflict; scores reflect document recency/authority, not differentiation)
- What if a source is missing metadata (author, date, version)? (Answer: Trust score reduced; flag indicates incomplete provenance)
- What if v2 contradicts both v1 and v3? (Answer: Multiple conflicts recorded; system identifies v2 as the anomaly or breaking change)
- What if source_type is inconsistent across versions (e.g., v1=policy, v3=guidance)? (Answer: Flag as `VERSION_MISMATCH` and impact trust score)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept query, rag_answer, and sources[] array as input
- **FR-002**: System MUST identify when two documents (diff versions) make contradictory claims on the same topic
- **FR-003**: System MUST generate a TrustSignal output with: score (0–1 composite), evidence (lineage chain per source), flags (DATE_CONFLICT, VERSION_MISMATCH, COMPLIANCE_RISK)
- **FR-004**: System MUST calculate trust score as composite of: document recency, metadata completeness, authority (source_type), update consistency
- **FR-005**: System MUST trace full provenance lineage: origin→v1→v2→v3 with timestamps and author info from YAML front-matter
- **FR-006**: System MUST maintain conflict ground truth file: cluster, doc_a, doc_b, conflicting_claim
- **FR-007**: System MUST flag conflicts as DATE_CONFLICT (temporal mismatch), VERSION_MISMATCH (structural/type change), or COMPLIANCE_RISK (regulatory domain contradiction)
- **FR-008**: System MUST support regulatory domains: GDPR, data retention, IP law (extensible to others)
- **FR-009**: System MUST provide POST /evaluate endpoint returning structured JSON TrustSignal
- **FR-010**: System MUST ensure each document version in corpus has YAML front-matter: author, date, version, source_type, regulatory_domain

### Key Entities

- **Source Document**: Represents a specific version of a regulatory/policy document, with metadata (author, date, version, source_type, regulatory_domain)
- **Conflict**: Represents a contradiction between two sources on a specific claim; includes conflicting_claim field and flag type
- **TrustSignal**: Composite output of THEMIS evaluation; contains score, evidence lineage, and conflict flags
- **Lineage Chain**: Ordered sequence of document versions showing origin and all updates with timestamps and metadata
- **Corpus Cluster**: Logical group of related documents (e.g., cluster 02); supports ground truth conflict mapping

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Demo query on cluster 02 sources returns DATE_CONFLICT flag when v1 (2021) and v3 (2023) contradict on approval year
- **SC-002**: Trust score for v2 (most recent update) reaches 0.9 or higher; v1 and v3 scores lower due to conflicts or staleness
- **SC-003**: Lineage chain traces full document history: shows origin date, all updates, authors, and changes
- **SC-004**: At least 2 corpus clusters include regulatory_domain metadata; conflicts within those clusters trigger COMPLIANCE_RISK flags
- **SC-005**: POST /evaluate endpoint processes request in <500ms and returns valid TrustSignal JSON
- **SC-006**: Conflict ground truth file has entries for all identified contradictions in corpus; can be used to validate system against expected conflicts
- **SC-007**: 100% of source documents have YAML front-matter with required fields; system rejects incomplete metadata
- **SC-008**: TrustSignal output matches demo specification: score (0–1), evidence (lineage), flags (DATE_CONFLICT/VERSION_MISMATCH/COMPLIANCE_RISK)

## Assumptions

- **Assumptions about data**: Source documents in corpus follow versioning convention (v1, v2, v3) and have consistent YAML front-matter structure (author, date, version, source_type, regulatory_domain)
- **Assumption about scope**: v1 = original document; v2 = updates some facts; v3 = intentionally contradicts v1 on at least one claim (for demo purposes and conflict detection validation)
- **Assumption about conflicts**: Contradictions are explicit claim-level mismatches (e.g., approval date 2021 vs 2023), not minor wording variations
- **Assumption about regulatory domains**: THEMIS focuses on policy, compliance & regulatory domains; security/infrastructure monitoring is out of scope
- **Assumption about trust scoring**: Higher scores favor recent, well-metadata'd, authoritative documents (source_type=policy beats guidance)
- **Assumption about extensibility**: New regulatory domains and flag types can be added without core logic changes; flag types default to DATE_CONFLICT, VERSION_MISMATCH, COMPLIANCE_RISK
- **Assumption about integration**: Downstream systems will integrate via POST /evaluate endpoint; internal corpus usage is secondary
- **Assumption about ground truth**: Conflict ground truth file is manually curated and serves as validation oracle for system accuracy testing

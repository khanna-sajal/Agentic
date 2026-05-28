# THEMIS Constitution

## Core Principles

### 1. Evidence-First Provenance
All TrustSignal outputs must be explainable, deterministic, and traceable to explicit source documents. Every inference step and decision path must reference document metadata, provenance graph nodes, or document lineage identifiers. No output is acceptable without an evidence chain that can be replayed and audited.

### 2. Immutable Version Lineage
Document versions are immutable artifacts. Historical versions may never be overwritten; every update must create a new version with metadata and graph relationships linking it back to its ancestors. Metadata must capture source document origin, version timestamp, authoring context, and lineage relationships.

### 3. Explicit Conflict Detection
THEMIS must detect factual, version, date, policy, regulatory, and other conflicts with explicit reasoning. Conflict reports must identify conflicting claims, involved documents, conflict type, and exactly why the evidence does not align. No conflict should be reported without a documented reasoning path.

### 4. Compliance Risk Rule Mapping
All compliance risks must map directly to defined rules. Risk findings must be tied to a rule identifier, rule text, and supporting evidence from source documents. Compliance evaluations must produce rule-based outputs rather than opaque judgments.

### 5. Quality, Testing, UX, and Performance
Code quality is non-negotiable: modular APIs, static analysis, and documented contracts are required. Testing must include unit, integration, regression, provenance, and conflict-detection coverage before changes merge. User experience must be consistent, human-readable, and audit-friendly for all provenance, conflict, and compliance outputs. Performance requirements must ensure deterministic evaluation, bounded graph traversal, and responsive API interactions.

## Architectural Constraints
THEMIS must expose modular APIs for ingest, provenance graph management, conflict detection, compliance evaluation, and TrustSignal generation. All provenance outputs must be structured, human-readable, and machine-parseable. Trust scores alone are forbidden unless accompanied by an explicit evidence path, deterministic reasoning trace, and source citation. Provenance must be stored as metadata and graph relationships so every artifact can be reconstructed from source inputs.

## Development Workflow
All work must follow a test-first workflow: tests defining provenance, lineage, conflict, and compliance behavior are written before implementation. Code reviews must validate metadata schemas, graph lineage integrity, explicit conflict reasoning, and the absence of historical version overwrites. CI must verify deterministic TrustSignal reproduction from source documents and enforce requirements for auditability, reproducibility, and performance.

## Governance
This constitution is the authoritative guide for THEMIS design, implementation, and review. Amendments require a documented rationale, version change, and regression coverage for evidence, lineage, conflict, and compliance protections. All pull requests and reviews must verify that changes preserve immutable lineage, avoid hallucination, maintain explicit evidence mapping, and do not introduce opaque trust scores. Exceptions must be documented with a governance decision record.

**Version**: 0.1.0 | **Ratified**: 2026-05-28 | **Last Amended**: 2026-05-28

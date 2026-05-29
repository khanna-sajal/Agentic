# Research: Provenance Extraction, Lineage, Conflict Extraction, Compliance Labelling

## Decision: YAML metadata parser for provenance extraction

**What was chosen**: Use YAML front-matter parsing to extract provenance metadata from each source document.

**Rationale**: The corpus requirement explicitly calls for YAML front-matter fields (`author`, `date`, `version`, `source_type`, `regulatory_domain`). A YAML parser is the most reliable and maintainable way to extract this metadata without brittle regex.

**Alternatives considered**:
- Regex-based extraction: easier to implement but fragile and hard to validate across document variants.
- JSON or custom delimiter format: would require corpus conversion and reduce compatibility with existing YAML-based sources.

## Decision: NetworkX or dict graph for version lineage

**What was chosen**: Model lineage as a directed graph using NetworkX when available, with a lightweight dict-based graph abstraction as a fallback.

**Rationale**: Provenance lineage is naturally graph-shaped, and NetworkX provides graph traversal, cycle detection, and readable APIs. A dict-backed graph interface ensures the feature remains deployable without a hard dependency if necessary.

**Alternatives considered**:
- Pure linear version sequence: too restrictive for documents with branching or shared ancestry.
- Relational tables or database storage: unnecessary for the initial feature and adds undue complexity.

## Decision: Groq for conflict extraction + compliance labelling

**What was chosen**: Use a Groq-inspired declarative query mechanism to identify claim mismatches and rule-triggering patterns across source documents.

**Rationale**: Conflict extraction and compliance labelling require expressive but auditable queries. Groq-style queries provide a clear mapping from source document data to conflict indicators, making the logic easier to review and maintain.

**Alternatives considered**:
- Hand-coded procedural matching: more error-prone and harder to maintain over multiple claim types.
- Machine-learned classification: not appropriate for explicit regulatory rule mapping and auditability.

## Decision: Rule-based compliance checker

**What was chosen**: Implement compliance risk detection using explicit rules mapped to regulatory domains and claim-level evidence.

**Rationale**: THEMIS governance requires rule-based outputs rather than opaque judgments. A rule engine lets us attach specific rule IDs, rule text, and supporting evidence to every `COMPLIANCE_RISK` finding.

**Alternatives considered**:
- Score-only risk heuristics: violates the evidence-first constitution and is not audit-friendly.
- Statistical or ML risk assessment: out of scope for deterministic compliance reasoning.

## Research Summary

- Provenance extraction is best served by YAML metadata parsing.
- Lineage should be represented as an immutable DAG with graph traversal support.
- Conflict extraction should use Groq-style declarative queries for claim matching.
- Compliance labelling must be rule-based and evidence-backed.
- These decisions align with the feature spec and THEMIS constitution, eliminating the need for further clarification.

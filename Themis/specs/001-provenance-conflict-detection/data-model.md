# Data Model: Document Provenance & Conflict Detection

## Entities

### SourceDocument
Represents one source document or version in the corpus.

Fields:
- `id`: unique identifier (e.g. `cluster02_v1`)
- `cluster`: cluster identifier (e.g. `cluster02`)
- `version`: version label (e.g. `v1`, `v2`, `v3`)
- `author`: metadata author
- `date`: metadata publication/update date
- `source_type`: policy, guidance, regulation, etc.
- `regulatory_domain`: GDPR, data retention, IP law, etc.
- `content`: raw document content
- `parsed_claims`: extracted structured claims from content
- `parent_ids`: list of immediate predecessor document IDs
- `lineage_id`: optional lineage group identifier

### ProvenanceGraph
Represents immutable version relationships.

Fields:
- `nodes`: collection of `SourceDocument` nodes
- `edges`: directed edges representing `derived_from` relationships
- `root_nodes`: source origins with no parents
- `descendants(source_id)`: function to traverse downstream versions
- `ancestors(source_id)`: function to traverse upstream provenance

### Claim
Represents a normalized statement extracted from a source document.

Fields:
- `claim_key`: canonical claim identifier (e.g. `approval_year`)
- `claim_text`: original claim text
- `claim_value`: normalized value (e.g. `2021`)
- `source_id`: source document reference
- `confidence`: optional metadata for extraction confidence

### Conflict
Represents a contradiction between two source documents.

Fields:
- `doc_a`: source document ID
- `doc_b`: source document ID
- `conflicting_claim`: canonical claim key
- `claim_a`: value in doc_a
- `claim_b`: value in doc_b
- `conflict_type`: `DATE_CONFLICT`, `VERSION_MISMATCH`, or `COMPLIANCE_RISK`
- `evidence`: list of supporting claim citations and metadata
- `rule_id`: optional compliance rule tied to the conflict

### ComplianceRule
Represents a named regulatory rule used for risk labelling.

Fields:
- `rule_id`: unique rule identifier
- `domain`: regulatory domain (e.g. GDPR)
- `description`: rule text or logic summary
- `trigger_conditions`: Groq-style query or predicate
- `severity`: risk weighting or classification

### TrustSignal
Represents the final evaluation payload.

Fields:
- `score`: float between 0 and 1
- `flags`: list of severity flags (e.g. `DATE_CONFLICT`, `VERSION_MISMATCH`, `COMPLIANCE_RISK`)
- `evidence`: lineage chain(s) and conflict details per source
- `lineage_chains`: ordered path(s) from origin to latest version
- `rule_matches`: matched compliance rules with evidence
- `source_scores`: per-document trust scores and metadata contributions

## Relationships

- A `SourceDocument` may have zero or more parents (
  `derived_from` relations) and zero or more derived children.
- A `ProvenanceGraph` links `SourceDocument` nodes into immutable version lineages.
- `Claim` objects are extracted from `SourceDocument` content and are the basis for `Conflict` detection.
- `Conflict` findings reference two `SourceDocument` nodes and one canonical claim key.
- `TrustSignal` aggregates provenance, scores, conflicts, and compliance risk evidence.

## Validation Rules

- Every document must include YAML metadata: `author`, `date`, `version`, `source_type`, `regulatory_domain`.
- Conflicts are only reported when document claims are semantically distinct and the same claim key differs.
- Trust scores are computed from document recency, metadata completeness, authority, and update consistency.
- Compliance flags require an explicit matching rule and evidence chain.

## Sample Data Model Flow

1. Parse YAML metadata from `cluster02/themis_cluster02_v1.txt`, `v2.txt`, `v3.txt`.
2. Build `SourceDocument` nodes and `ProvenanceGraph` edges: `v2` derived from `v1`, `v3` derived from `v2` or `v1` depending on assignment.
3. Extract claims such as `approval_year` from each source.
4. Detect a conflict between `v1` and `v3` on `approval_year` → create `Conflict` object.
5. Evaluate compliance rules for the regulatory domain and attach `COMPLIANCE_RISK` if needed.
6. Produce a `TrustSignal` with `score`, `flags`, and `evidence` chains.

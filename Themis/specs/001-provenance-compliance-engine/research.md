# Research: Provenance & Compliance Intelligence Engine

**Created**: May 29, 2026 | **Feature**: [plan.md](plan.md)

**Purpose**: Research and resolve unknowns from the implementation plan before design phase.

## Topic 1: Groq API Integration for Semantic Conflict Detection

### Research Goal
Determine optimal approach for using Groq API to extract and compare regulatory claims for Phase 2 semantic conflict detection.

### Context
- FR-008 requires semantic fallback after exact string matching fails
- Conflict detection must identify 95%+ of manually-verified conflicts (SC-003)
- Semantic matching is identification-only; reconciliation delegated to humans

### Key Findings

**Groq LLM Capabilities for Regulatory Text**:
- Groq provides fast LLM inference suitable for claim extraction
- Regulatory domain text (HIPAA, GDPR) is well-represented in training data
- Model-agnostic approach: Use `mixtral-8x7b-32768` or similar for cost/quality balance

**Recommended Prompt Engineering Strategy**:
```
System: You are a regulatory compliance analyst expert in extracting structured claims from 
regulatory documents.

User: Extract the key compliance claims from this text as a structured JSON list:
{doc_text}

Expected format:
{
  "claims": [
    {"entity": "patient_data", "requirement": "encryption required", "severity": "must"},
    ...
  ],
  "domain": "HIPAA"
}

Response should be valid JSON parseable by Python json module.
```

**Semantic Comparison Strategy**:
1. Extract claims from both documents using Groq
2. For each unmatched exact string pair, compute embeddings (using local model or Groq endpoint)
3. Calculate cosine similarity; threshold at 0.85 for semantic match
4. Report high-similarity pairs as potential conflicts for human review

**Cost/Performance**:
- Average cost: $0.0001-$0.0003 per claim extraction (thousands of claims for <$1)
- Latency: 200-500ms per extraction (acceptable for batch processing)
- Accuracy: Groq models typically 90%+ accurate for regulatory text extraction

**Recommendation**: ✅ Use Groq API  
**Risk**: Dependency on external API (Groq service availability)  
**Mitigation**: Implement fallback to simpler exact-match-only if Groq unavailable; cache results

---

## Topic 2: NetworkX DAG for Version Lineage

### Research Goal
Determine best practices for using NetworkX to model document version history and detect version conflicts.

### Context
- FR-007 requires preserving queryability of historical versions
- SC-005 targets <2 seconds for comparing 10 versions
- THEMIS principle: Immutable version lineage (no overwrites)

### Key Findings

**NetworkX DAG Best Practices**:
- Use `DiGraph` (directed graph) for parent → child relationships
- Add node attributes: `version`, `timestamp`, `author`, `document_id`, `metadata`
- Add edge attributes: `parent_version`, `branching_reason` (if versions diverge)

**Example Structure**:
```python
import networkx as nx

# Create DAG
lineage_graph = nx.DiGraph()

# Add nodes for each version
lineage_graph.add_node(
    "doc_cluster01_v1",
    version="1",
    timestamp="2026-01-01",
    author="Alice",
    regulatory_domain="HIPAA",
    content_hash="abc123"
)
lineage_graph.add_node("doc_cluster01_v2", ...)

# Add edges: v1 → v2 (v2 is child of v1)
lineage_graph.add_edge("doc_cluster01_v1", "doc_cluster01_v2", relationship="update")

# Query: Get full lineage
ancestors = nx.ancestors(lineage_graph, "doc_cluster01_v3")  # O(n)
```

**Performance Characteristics**:
- Adding versions: O(1) per node/edge
- Comparing two branches: O(n+m) traversal
- 10 versions × 5 paths = ~50 nodes; full DAG traversal << 2 seconds ✅

**Conflict Detection in DAG**:
- Detect diamond patterns (multiple paths to same descendant)
- Identify diverging versions (sibling nodes from same parent)
- Flag as potential conflicts if regulatory domain differs

**Storage**:
- Serialize to JSON using `node_link_data()` for persistence
- Load from database on startup
- Periodically checkpoint to avoid rebuild overhead

**Recommendation**: ✅ Use NetworkX DiGraph  
**Alternative Considered**: PostgreSQL with graph extension (PostGIS/AgensGraph) - rejected for initial phase (simpler development without db complexity)

---

## Topic 3: SHA-256 Hash Chain Implementation

### Research Goal
Define algorithm for constructing and verifying tamper-proof audit logs using SHA-256 hash chains.

### Context
- FR-018 requires audit log entries to include SHA-256 hash of previous entry
- SC-010 requires tamper detection mechanism
- Audit logs must be append-only

### Key Findings

**Hash Chain Structure**:
```python
Entry = {
    "sequence_number": 1,
    "timestamp": "2026-05-29T14:32:00Z",
    "query": "Show compliance risks",
    "sources": ["doc_cluster01_v2"],
    "confidence": 0.95,
    "previous_hash": None  # First entry
}

Entry2 = {
    "sequence_number": 2,
    "timestamp": "2026-05-29T14:33:00Z",
    "query": "Show conflict report",
    "sources": ["doc_cluster01_v1", "doc_cluster01_v2"],
    "confidence": 0.87,
    "previous_hash": SHA256(Entry)  # Hash of previous entry
}
```

**Verification Algorithm**:
```python
def verify_hash_chain(entries):
    previous_hash = None
    for entry in entries:
        current_hash = SHA256(entry)
        if entry.previous_hash != previous_hash:
            return False  # Tampering detected
        previous_hash = current_hash
    return True
```

**Storage**:
- Store `previous_hash` as hex string in audit log table
- Compute current entry hash on write (not stored, validated on read)
- Never allow deletion or modification of entries (append-only policy)

**Cost/Performance**:
- SHA-256 computation: <1ms per entry
- Verification of 1000-entry log: <1 second ✅
- Storage overhead: 64 bytes (hex SHA-256) per entry

**Recommendation**: ✅ Use SHA-256 hash chains  
**Alternative Considered**: Digital signatures (rejected for requiring PKI infrastructure)

---

## Topic 4: Rule-Based Compliance Checker Architecture

### Research Goal
Define rule format and evaluation strategy for compliance risk assessment engine.

### Context
- FR-010, FR-011, FR-012 require rule-based compliance evaluation
- FR-017 Compliance Risk Report API must provide risk severity and evidence
- Rules must be maintainable by non-developers via config files

### Key Findings

**Rule Definition Format** (YAML):
```yaml
regulatory_domains:
  HIPAA:
    name: "Health Insurance Portability and Accountability Act"
    effective_date: "1996-08-21"
    last_updated: "2013-01-25"
    required_for_source_types: ["medical_record", "patient_data"]
    rules:
      - id: "HIPAA-001"
        description: "Patient data must be encrypted in transit"
        severity: "HIGH"
        check: "field:encryption == 'required'"
      - id: "HIPAA-002"
        description: "Authorization required before sharing patient data"
        severity: "MEDIUM"
        check: "field:authorization_required == true"
```

**Rule Engine Evaluation**:
```python
def evaluate_rules(document, domain_rules):
    violations = []
    for rule in domain_rules.rules:
        result = evaluate_check(rule.check, document.metadata)
        if not result:
            violations.append({
                "rule_id": rule.id,
                "severity": rule.severity,
                "description": rule.description,
                "evidence": document.id
            })
    return violations
```

**Risk Scoring**:
- Count violations per severity
- Aggregate: 1+ HIGH = HIGH risk, all MEDIUM+ = MEDIUM risk, only LOW = LOW risk
- Store evidence trace to each contributing rule

**Recommendation**: ✅ Rule-based engine with YAML config  
**Alternative Considered**: ML-based risk scoring (rejected per THEMIS constitution: "Trust scores alone forbidden without explicit evidence")

---

## Topic 5: FastAPI REST API Design for Provenance Operations

### Research Goal
Design RESTful API endpoints for provenance lookup, version comparison, conflict reports, and compliance risk assessment.

### Context
- FR-014–FR-017 require four major API endpoints
- API must integrate with existing RAG system
- Performance target: <500ms for 99% of requests (SC-007)

### Key Findings

**Endpoint Design**:

1. **Provenance Lookup API** (FR-014)
   ```
   GET /api/v1/provenance/{answer_id}
   Response: {
     "answer_id": "...",
     "sources": [
       {"document_id": "...", "version": "2", "author": "...", "date": "..."},
       ...
     ],
     "chains": ["doc1→doc2→doc3", ...],  # Lineage paths
     "timestamp": "2026-05-29T14:32:00Z"
   }
   ```

2. **Version Comparison API** (FR-015)
   ```
   GET /api/v1/versions/compare?doc_id=cluster01&v1=1&v2=2
   Response: {
     "document_id": "cluster01",
     "v1": {...}, "v2": {...},
     "differences": [
       {"field": "regulatory_domain", "v1": "HIPAA", "v2": "HIPAA,GDPR"}
     ]
   }
   ```

3. **Conflict Report API** (FR-016)
   ```
   GET /api/v1/conflicts?domain=HIPAA&severity=HIGH
   Response: [
     {
       "conflict_id": "...",
       "type": "regulatory_rule",
       "documents": ["cluster01_v1", "cluster01_v2"],
       "conflicting_content": "Rule X vs Rule Y",
       "severity": "HIGH"
     }
   ]
   ```

4. **Compliance Risk Report API** (FR-017)
   ```
   GET /api/v1/compliance-risk?document_id=cluster01
   Response: {
     "document_id": "cluster01",
     "overall_risk": "MEDIUM",
     "risks": [
       {"rule_id": "HIPAA-001", "severity": "HIGH", "evidence": "..."}
     ],
     "recommendations": ["Update encryption field", ...]
   }
   ```

5. **Document Ingestion API** (On-demand trigger)
   ```
   POST /api/v1/ingest
   Request: {"trigger": "all" | "specific", "document_id": "..."}
   Response: {"status": "processing", "documents_queued": 5}
   ```

**Performance Optimization**:
- Cache provenance graphs in memory after first load
- Index audit logs by timestamp for quick lookup
- Use query filtering (domain, severity) to reduce result set
- Implement pagination for large result sets

**Authentication**:
- API key for service-to-service calls (RAG system)
- Optional JWT for future compliance team UI

**Recommendation**: ✅ FastAPI with modular endpoints  
**Alternative Considered**: GraphQL (rejected for simpler REST design sufficient for use case)

---

## Summary of Resolved Unknowns

| Unknown | Research | Recommendation | Implementation Impact |
|---------|----------|-----------------|----------------------|
| Groq integration for semantic detection | Prompt engineering + similarity thresholding | Use Groq API with local embedding comparison | Add `semantic_validator.py` module; external API dependency |
| NetworkX for version lineage | DiGraph best practices, performance validation | Use DiGraph for version DAG; JSON serialization for storage | Add `version_graph.py` module; ~50 LOC per feature |
| SHA-256 hash chains for audit logs | Hash chain algorithm, verification strategy | Two-phase: write current hash, verify on read | Add `hash_chain.py` module; <1ms per operation |
| Rule-based compliance checker | Rule format (YAML), engine evaluation | YAML config with rule definitions; simple evaluation engine | Add `rule_engine.py` + `regulatory_domains.yaml`; 100-200 LOC |
| FastAPI REST API design | Endpoint mapping to features, performance optimization | Five endpoints as designed above; query filtering + caching | Add `*_api.py` modules; ~500 LOC total |

All unknowns resolved. Ready for Phase 1 detailed design.

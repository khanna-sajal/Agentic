# Contract: Provenance Lineage

## Purpose
Provide programmatic access to the version DAG for documents and enable lineage queries.

## Interfaces
- `get_lineage(document_id, version)` -> returns ancestry and descendant paths
- `add_version(parent_document_id, parent_version, new_document)` -> adds node and edge
- `compare_versions(doc_id, v1, v2)` -> returns field-level differences and path differences

## Data Shape
- Nodes: `{ node_id, document_id, version, timestamp, author, content_hash }`
- Edges: `{ parent_node_id, child_node_id, relationship }`

## Performance
- Ancestry traversal for 10 versions should complete <2s (SC-005)

## Persistence
- Serialize using NetworkX node-link format for storage and reload

## Error Handling
- Reject attempts to overwrite existing version nodes; require explicit creation of new version nodes

## Example
- `get_lineage('cluster01', '3')` -> `['cluster01_v1' -> 'cluster01_v2' -> 'cluster01_v3']`

# Contract: Audit Logging and Hash Chains

## Purpose
Append-only audit log with SHA-256 previous-hash linkage for tamper detection.

## Interfaces
- `append_log(entry)` -> writes new audit log entry with computed previous_hash
- `verify_log()` -> boolean (true if chain intact)
- `get_logs(filter)` -> paginated audit entries

## Entry Shape
- `sequence_number`, `timestamp`, `action`, `query`, `sources`, `result_summary`, `previous_hash`

## Verification
- Recompute chained hashes sequentially and compare stored `previous_hash` values

## Performance
- Hash computation <1ms per entry; verify 1000 entries <1s

## Example
- `append_log({...})` -> writes entry with `previous_hash` set to SHA256(prev_entry)

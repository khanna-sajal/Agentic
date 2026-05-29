import hashlib
import json
from typing import Any, Dict, Iterable, List


def canonicalize(entry: Dict[str, Any]) -> str:
    return json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_entry_hash(entry: Dict[str, Any]) -> str:
    payload = {k: entry[k] for k in sorted(entry) if k != "entry_hash"}
    return hashlib.sha256(canonicalize(payload).encode("utf-8")).hexdigest()


def verify_hash_chain(entries: Iterable[Dict[str, Any]]) -> bool:
    previous_hash: str | None = None
    for entry in entries:
        expected_prev = entry.get("previous_hash")
        if expected_prev != previous_hash:
            return False
        computed_hash = compute_entry_hash(entry)
        if entry.get("entry_hash") != computed_hash:
            return False
        previous_hash = computed_hash
    return True

from typing import Dict
from pathlib import Path


def detect_conflict(a_path: str, b_path: str, key: str = 'date') -> Dict[str, str]:
    """Detect a simple metadata key conflict between two documents.

    Returns a dict with conflict details if conflict found, otherwise empty dict.
    This function is intentionally simple for scaffolding; replace with
    richer deterministic reasoning in implementation.
    """
    from .provenance import get_lineage
    a_meta = get_lineage(a_path)
    b_meta = get_lineage(b_path)
    if key in a_meta and key in b_meta and a_meta[key] != b_meta[key]:
        return {
            'conflict_key': key,
            'a_value': a_meta[key],
            'b_value': b_meta[key],
            'reason': f"metadata '{key}' differs"
        }
    return {}

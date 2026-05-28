from typing import Dict
from pathlib import Path


def get_lineage(file_path: str) -> Dict[str, str]:
    """Extract simple YAML-like metadata header between '---' markers.

    Returns a dict of metadata keys -> values. Raises ValueError if header missing.
    """
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(file_path)
    text = p.read_text(encoding='utf-8')
    if '---' not in text:
        raise ValueError('No metadata header found')
    parts = text.split('---')
    # metadata is expected in the first header block after the opening '---'
    if len(parts) < 3:
        raise ValueError('Malformed metadata header')
    header = parts[1].strip().splitlines()
    meta = {}
    for line in header:
        if ':' in line:
            key, val = line.split(':', 1)
            meta[key.strip()] = val.strip()
    return meta

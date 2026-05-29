"""THEMIS package"""

__version__ = "0.1.0"

from .provenance import (
    SourceDocument,
    build_lineage_graph,
    get_lineage,
    load_source_document,
    parse_source_document,
)
from .conflict import Conflict, detect_conflict, extract_conflicts
from .trustsignal import build_trust_signal

__all__ = [
    "SourceDocument",
    "build_lineage_graph",
    "get_lineage",
    "load_source_document",
    "parse_source_document",
    "Conflict",
    "detect_conflict",
    "extract_conflicts",
    "build_trust_signal",
]

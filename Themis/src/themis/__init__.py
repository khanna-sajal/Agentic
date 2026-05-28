"""THEMIS package"""

__version__ = "0.1.0"

from .provenance import get_lineage
from .conflict import detect_conflict

__all__ = ["get_lineage", "detect_conflict"]

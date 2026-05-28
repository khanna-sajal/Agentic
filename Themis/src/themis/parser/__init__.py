"""THEMIS parser package

This package will contain parsers that extract structured claims, metadata,
and provenance tokens from source documents in the corpus.
"""

from .simple_parser import parse_metadata, extract_claims

__all__ = ["parse_metadata", "extract_claims"]

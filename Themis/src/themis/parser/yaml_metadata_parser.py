import re
from typing import Any, Dict, List, Optional

import yaml


FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _normalize_regulatory_domain(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def parse_yaml_front_matter(text: str, document_id: Optional[str] = None) -> Dict[str, Any]:
    """Parse YAML front-matter from the start of a document.

    Returns a dict with keys:
      - document_id
      - metadata (dict)
      - validation_status: 'valid' | 'missing_fields' | 'malformed' | 'none'
      - errors: list of error messages (optional)

    The parser is forgiving: malformed YAML does not raise, it returns status 'malformed'
    and an errors list so batch ingestion can continue.
    """
    result: Dict[str, Any] = {
        "document_id": document_id,
        "metadata": {},
        "validation_status": "none",
        "errors": [],
    }

    m = FRONT_MATTER_RE.match(text)
    if not m:
        result["validation_status"] = "none"
        result["content"] = text
        return result

    fm_text = m.group(1)
    body_start = m.end()
    body_text = text[body_start:]
    try:
        parsed = yaml.safe_load(fm_text)
    except Exception as exc:  # yaml parser error
        result["validation_status"] = "malformed"
        result["errors"].append(str(exc))
        result["content"] = body_text
        return result

    if not isinstance(parsed, dict):
        result["validation_status"] = "malformed"
        result["errors"].append("YAML front-matter did not parse to a mapping/dict")
        return result

    # Extract expected fields
    metadata: Dict[str, Any] = {}
    metadata["author"] = parsed.get("author")
    metadata["date"] = parsed.get("date")
    metadata["version"] = parsed.get("version")
    metadata["source_type"] = parsed.get("source_type")
    metadata["regulatory_domain"] = _normalize_regulatory_domain(parsed.get("regulatory_domain"))

    # Validate required fields
    missing: List[str] = []
    for f in ("author", "date", "version"):
        if metadata.get(f) is None:
            missing.append(f)

    result["metadata"] = metadata
    result["content"] = body_text
    if missing:
        result["validation_status"] = "missing_fields"
        result["errors"].append(f"missing required fields: {', '.join(missing)}")
    else:
        result["validation_status"] = "valid"

    return result


__all__ = ["parse_yaml_front_matter"]

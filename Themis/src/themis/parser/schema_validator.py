from typing import Any, Dict, List


def validate_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    if not isinstance(metadata, dict):
        errors.append("Metadata must be a dictionary")
        return {"valid": False, "errors": errors, "metadata": metadata}

    required_fields = ["author", "date", "version"]
    missing = [field for field in required_fields if metadata.get(field) is None]
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    if "regulatory_domain" in metadata and metadata["regulatory_domain"] is not None:
        if not isinstance(metadata["regulatory_domain"], list):
            errors.append("regulatory_domain must be a list if present")

    return {
        "valid": not errors,
        "errors": errors,
        "metadata": metadata,
    }

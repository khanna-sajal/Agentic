from themis.parser.yaml_metadata_parser import parse_yaml_front_matter


def test_parse_valid_front_matter():
    doc = """---
author: Alice
date: 2026-01-01
version: 1
source_type: medical_record
regulatory_domain: [HIPAA]
---
This is the body.
"""

    res = parse_yaml_front_matter(doc, document_id="cluster01_v1")
    assert res["validation_status"] == "valid"
    assert res["metadata"]["author"] == "Alice"
    assert res["metadata"]["version"] == 1
    assert res["metadata"]["regulatory_domain"] == ["HIPAA"]


def test_parse_missing_fields():
    doc = """---
author: Bob
source_type: report
---
Body
"""
    res = parse_yaml_front_matter(doc)
    assert res["validation_status"] == "missing_fields"
    assert "missing required fields" in res["errors"][0]


def test_no_front_matter():
    doc = "This document has no front matter.\nContent here.\n"
    res = parse_yaml_front_matter(doc)
    assert res["validation_status"] == "none"


def test_malformed_yaml():
    doc = """---
author: Alice
date: 2026-01-01
version: [1, 2
---
Body
"""
    res = parse_yaml_front_matter(doc)
    assert res["validation_status"] == "malformed"
    assert res["errors"]

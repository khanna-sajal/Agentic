from themis import SourceDocument
from themis.compliance import evaluate_compliance
from themis.conflict import extract_conflicts


def test_evaluate_compliance_risk():
    docs = [
        SourceDocument(
            id='cluster02_v1',
            cluster='cluster02',
            version='v1',
            author='Policy Team',
            date='2021-01-15',
            source_type='policy',
            regulatory_domain='GDPR',
            content='---\nauthor: Policy Team\ndate: 2021-01-15\nversion: v1\nsource_type: policy\nregulatory_domain: GDPR\n---\nPolicy X approved 2021.',
        ),
        SourceDocument(
            id='cluster02_v3',
            cluster='cluster02',
            version='v3',
            author='Legal Team',
            date='2023-03-01',
            source_type='policy',
            regulatory_domain='GDPR',
            content='---\nauthor: Legal Team\ndate: 2023-03-01\nversion: v3\nsource_type: policy\nregulatory_domain: GDPR\n---\nPolicy X approved 2023.',
        ),
    ]
    conflicts = extract_conflicts(docs)
    rule_matches = evaluate_compliance(conflicts, docs)
    assert len(rule_matches) == 1
    assert rule_matches[0].rule_id == 'RULE_DATE_CONFLICT'
    assert 'GDPR' in rule_matches[0].trigger_conditions

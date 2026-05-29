from themis import SourceDocument
from themis.compliance import evaluate_compliance
from themis.conflict import extract_conflicts
from themis.provenance import build_lineage_graph
from themis.trustsignal import build_trust_signal


def test_build_trust_signal_prioritizes_non_conflicting_source():
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
            id='cluster02_v2',
            cluster='cluster02',
            version='v2',
            author='Compliance Officer',
            date='2022-06-20',
            source_type='policy',
            regulatory_domain='GDPR',
            content='---\nauthor: Compliance Officer\ndate: 2022-06-20\nversion: v2\nsource_type: policy\nregulatory_domain: GDPR\n---\nPolicy X updated.',
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
    lineage_graph = build_lineage_graph(docs)
    conflicts = extract_conflicts(docs)
    rules = evaluate_compliance(conflicts, docs)
    signal = build_trust_signal(docs, conflicts, rules, lineage_graph)

    scores = {entry['source_id']: entry['score'] for entry in signal['source_scores']}
    assert scores['cluster02_v2'] >= scores['cluster02_v3']
    assert scores['cluster02_v2'] >= scores['cluster02_v1']
    assert 'DATE_CONFLICT' in signal['flags']
    assert signal['lineage_chains'][0]['chain_id'].startswith('chain_')

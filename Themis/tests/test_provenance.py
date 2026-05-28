from themis import get_lineage


def test_get_lineage(tmp_path):
    p = tmp_path / 'doc.txt'
    p.write_text('''---\nname: testdoc\ndate: 2023-01-01\nversion: v1\n---\nContent''')
    meta = get_lineage(str(p))
    assert meta['name'] == 'testdoc'
    assert meta['date'] == '2023-01-01'
    assert meta['version'] == 'v1'

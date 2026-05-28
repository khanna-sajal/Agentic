from themis import detect_conflict


def test_detect_conflict(tmp_path):
    a = tmp_path / 'a.txt'
    b = tmp_path / 'b.txt'
    a.write_text('''---\ndate: 2023-01-01\nversion: v1\n---\nA''')
    b.write_text('''---\ndate: 2024-01-01\nversion: v2\n---\nB''')
    res = detect_conflict(str(a), str(b), key='date')
    assert res
    assert res['conflict_key'] == 'date'
    assert res['a_value'] == '2023-01-01'
    assert res['b_value'] == '2024-01-01'

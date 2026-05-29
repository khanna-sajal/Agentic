import shutil
from pathlib import Path

import pytest


@pytest.fixture
def sample_corpus_dir(tmp_path: Path) -> Path:
    fixture_dir = Path(__file__).resolve().parent / "fixtures" / "sample_corpus"
    target_dir = tmp_path / "corpus"
    shutil.copytree(fixture_dir, target_dir)
    return target_dir

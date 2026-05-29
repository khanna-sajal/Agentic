from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml


class Settings:
    def __init__(self, regulatory_yaml_path: str | None = None) -> None:
        self.regulatory_yaml_path = regulatory_yaml_path or os.getenv(
            "THEMIS_REGULATORY_DOMAINS_PATH"
        )
        if not self.regulatory_yaml_path:
            repo_root = Path(__file__).resolve().parents[3]
            self.regulatory_yaml_path = str(
                repo_root
                / "specs"
                / "001-provenance-compliance-engine"
                / "config"
                / "regulatory_domains.yaml"
            )

    def load_regulatory_domains(self) -> Dict[str, Any]:
        path = Path(self.regulatory_yaml_path)
        if not path.exists():
            raise FileNotFoundError(f"Regulatory domains file not found: {path}")
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)


config = Settings()

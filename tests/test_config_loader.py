import json
from pathlib import Path

import pytest

from log_analyzer.config_loader import ConfigLoader
from log_analyzer.exceptions import LogFileNotFoundError


def test_config_loader_loads_config(tmp_path: Path) -> None:
    config_file = tmp_path / "config.json"

    config_file.write_text(
        json.dumps(
            {
                "input_path": "logs/sample.txt",
                "output_path": "reports/report.txt",
                "format_type": "txt",
            }
        ),
        encoding="utf-8",
    )

    config = ConfigLoader(config_file).load()

    assert config.input_path.name == "sample.txt"
    assert config.output_path.name == "report.txt"
    assert config.format_type == "txt"


def test_config_loader_raises_for_missing_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.json"

    with pytest.raises(LogFileNotFoundError, match="doesn't exist"):
        ConfigLoader(missing_file).load()

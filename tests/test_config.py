from pathlib import Path

import pytest

from log_analyzer.config import AppConfig


def test_app_config_raises_for_unsupported_format(tmp_path: Path) -> None:
    input_path = tmp_path / "sample.txt"
    output_path = tmp_path / "report.txt"

    input_path.write_text(
        "\n".join(
            [
                "2026-04-10 10:00:00 INFO Application started",
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Unsupported format: xml"):
        AppConfig(
            input_path=input_path,
            output_path=output_path,
            format_type="xml",
        )

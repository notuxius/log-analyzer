from pathlib import Path

import pytest

from log_analyzer.config import AppConfig
from log_analyzer.container import AppContainer


def test_app_config_unsupported_format(tmp_path: Path) -> None:
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


def test_app_container_runs_pipeline(tmp_path: Path) -> None:
    input_path = tmp_path / "sample.txt"
    output_path = tmp_path / "report.txt"

    input_path.write_text(
        "\n".join(
            [
                "2026-04-10 10:00:00 INFO Application started",
                "2026-04-10 10:01:00 ERROR Something failed",
            ]
        ),
        encoding="utf-8",
    )

    config = AppConfig(
        input_path=input_path,
        output_path=output_path,
        format_type="txt",
    )

    container = AppContainer(config)
    report, saved_path = container.run()

    assert saved_path == output_path.resolve()
    assert output_path.read_text(encoding="utf-8") == report
    assert "Total lines: 2" in report
    assert "ERROR: 1" in report
    assert "- Something failed" in report

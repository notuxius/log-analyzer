import subprocess
import sys
from pathlib import Path


def test_cli_runs_and_creates_report(tmp_path: Path) -> None:
    input_file = tmp_path / "log.txt"
    output_file = tmp_path / "report.txt"

    input_file.write_text(
        "2026-04-10 10:00:00 INFO Application started\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "log_analyzer.main",
            "--input",
            str(input_file),
            "--output",
            str(output_file),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_file.exists()
    assert "Total lines: 1" in output_file.read_text()

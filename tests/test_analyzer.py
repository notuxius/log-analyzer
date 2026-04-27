import sys
import textwrap

import pytest

from log_analyzer.analyzer import (
    format_log_report,
    load_log_entries,
    save_report,
    summarize_logs,
)
from log_analyzer.main import main
from log_analyzer.models import LogEntry, LogLevel, LogSummary


def test_load_log_entries(tmp_path):
    log_file = tmp_path / "log.txt"
    log_file.write_text(
        "\n".join(
            [
                "2026-04-10 10:00:00 INFO Application started",
                "2026-04-10 10:01:00 ERROR Something failed",
            ]
        ),
        encoding="utf-8",
    )
    entries = load_log_entries(log_file)
    assert len(entries) == 2
    assert entries[0]["level"] == LogLevel.INFO
    assert entries[1]["level"] == LogLevel.ERROR
    assert entries[0]["message"] == "Application started"
    assert entries[1]["message"] == "Something failed"


def test_load_log_entries_raises_for_invalid_level(tmp_path):
    log_file = tmp_path / "log.txt"
    log_file.write_text(
        "\n".join(
            [
                "2026-04-10 10:00:00 INFO Application started",
                "2026-04-10 10:01:00 error Something failed",
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_log_entries(log_file)


def test_summarize_logs():
    entries: list[LogEntry] = [
        {
            "timestamp": "2026-04-10 10:00:00",
            "level": LogLevel.INFO,
            "message": "Application started",
        },
        {
            "timestamp": "2026-04-10 10:01:00",
            "level": LogLevel.WARNING,
            "message": "Something went wrong",
        },
        {
            "timestamp": "2026-04-10 10:01:00",
            "level": LogLevel.ERROR,
            "message": "Something failed",
        },
    ]
    summary = summarize_logs(entries)
    assert summary == {
        "total_lines": 3,
        "info_count": 1,
        "warning_count": 1,
        "error_count": 1,
        "error_messages": ["Something failed"],
    }


def test_format_log_report():
    summary: LogSummary = {
        "total_lines": 3,
        "info_count": 1,
        "warning_count": 1,
        "error_count": 1,
        "error_messages": ["Something failed"],
    }
    report = format_log_report(summary)
    expected = textwrap.dedent("""\
        Total lines: 3
        INFO: 1
        WARNING: 1
        ERROR: 1
        Error messages:
        - Something failed
        """).strip()

    assert report == expected


def test_save_report(tmp_path):
    output_path = tmp_path / "report.txt"
    report = textwrap.dedent("""\
        Total lines: 3
        INFO: 1
        WARNING: 1
        ERROR: 1
        Error messages:
        - Something failed
        """).strip()

    result_path = save_report(report, output_path)
    assert result_path == output_path
    assert output_path.read_text(encoding="utf-8") == report


def test_save_empty_report_raises_value_error(tmp_path):
    output_path = tmp_path / "report.txt"

    with pytest.raises(ValueError, match="Report cannot be empty"):
        save_report("", output_path)


def test_main_success(tmp_path, capsys, monkeypatch):
    log_file = tmp_path / "log.txt"
    log_file.write_text(
        "\n".join(
            [
                "2026-04-26 09:00:00 INFO Application started",
                "2026-04-26 09:01:12 INFO Loaded configuration",
                "2026-04-26 09:03:45 WARNING Disk usage above 80 percent",
                "2026-04-26 09:05:10 ERROR Database connection failed",
                "2026-04-26 09:06:20 INFO Retrying database connection",
                "2026-04-26 09:07:34 WARNING External API response was slow",
                "2026-04-26 09:08:02 ERROR Timeout while calling external API",
                "2026-04-26 09:10:00 INFO Report generation completed",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "log-analyzer",
            "--input",
            str(log_file),
            "--output",
            str(tmp_path / "report"),
            "--print-report",
        ],
    )

    return_code = main()
    assert return_code == 0

    output_file = tmp_path / "report.txt"
    assert output_file.exists()

    captured = capsys.readouterr()
    report = textwrap.dedent("""\
        Total lines: 8
        INFO: 4
        WARNING: 2
        ERROR: 2
        Error messages:
        - Database connection failed
        - Timeout while calling external API
        """).strip()
    assert captured.out.strip() == report

    content = output_file.read_text(encoding="utf-8")
    assert content == report


def test_main_failure(tmp_path, capsys, caplog, monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "log-analyzer",
            "--input",
            str(tmp_path / "missing.txt"),
            "--output",
            str(tmp_path / "report"),
            "--print-report",
        ],
    )

    return_code = main()
    assert return_code == 1

    output_file = tmp_path / "report.txt"
    assert not output_file.exists()

    captured = capsys.readouterr()
    assert captured.out.strip() == ""

    assert "doesn't exist" in caplog.text

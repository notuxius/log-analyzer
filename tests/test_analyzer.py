import textwrap

import pytest

from log_analyzer.analyzer import (
    format_log_report,
    load_log_entries,
    save_report,
    summarize_logs,
)
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

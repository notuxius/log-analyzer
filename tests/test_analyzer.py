import json
import sys
import textwrap

import pytest

from log_analyzer.analyzer import (
    FormatterFactory,
    JsonFormatter,
    LogLoader,
    LogProcessor,
    LogSummarizer,
    ReportSaver,
    TextFormatter,
)
from log_analyzer.config import AppConfig
from log_analyzer.container import AppContainer
from log_analyzer.main import main
from log_analyzer.models import LogEntry, LogLevel, LogSummary


def test_log_loader_loads_valid_entries(tmp_path):
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

    entries = LogLoader(log_file).load()

    assert len(entries) == 2
    assert entries[0]["level"] == LogLevel.INFO
    assert entries[1]["level"] == LogLevel.ERROR
    assert entries[0]["message"] == "Application started"
    assert entries[1]["message"] == "Something failed"


def test_log_loader_raises_for_invalid_level(tmp_path):
    log_file = tmp_path / "log.txt"
    log_file.write_text(
        "2026-04-10 10:01:00 error Something failed",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid log message level"):
        LogLoader(log_file).load()


def test_log_loader_raises_for_missing_file(tmp_path):
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError, match="doesn't exist"):
        LogLoader(missing_file).load()


def test_log_loader_raises_for_empty_file(tmp_path):
    log_file = tmp_path / "empty.txt"
    log_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="Log file cannot be empty"):
        LogLoader(log_file).load()


def test_log_loader_skips_malformed_lines(tmp_path):
    log_file = tmp_path / "log.txt"
    log_file.write_text(
        "\n".join(
            [
                "malformed line",
                "2026-04-10 10:00:00 INFO Application started",
            ]
        ),
        encoding="utf-8",
    )

    entries = LogLoader(log_file).load()

    assert len(entries) == 1
    assert entries[0]["message"] == "Application started"


def test_log_loader_skips_empty_messages(tmp_path):
    log_file = tmp_path / "log.txt"
    log_file.write_text(
        "2026-04-10 10:00:00 INFO    ",
        encoding="utf-8",
    )

    entries = LogLoader(log_file).load()

    assert entries == []


def test_log_summarizer_returns_expected_summary():
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
            "timestamp": "2026-04-10 10:02:00",
            "level": LogLevel.ERROR,
            "message": "Something failed",
        },
    ]

    summary = LogSummarizer().summarize(entries)

    assert summary == {
        "total_lines": 3,
        "info_count": 1,
        "warning_count": 1,
        "error_count": 1,
        "error_messages": ["Something failed"],
    }


def test_text_formatter_returns_expected_report():
    summary: LogSummary = {
        "total_lines": 3,
        "info_count": 1,
        "warning_count": 1,
        "error_count": 1,
        "error_messages": ["Something failed"],
    }

    report = TextFormatter().format(summary)

    expected = textwrap.dedent("""\
        Total lines: 3
        INFO: 1
        WARNING: 1
        ERROR: 1
        Error messages:
        - Something failed
        """).strip()

    assert report == expected


def test_json_formatter_returns_json_string():
    summary: LogSummary = {
        "total_lines": 1,
        "info_count": 1,
        "warning_count": 0,
        "error_count": 0,
        "error_messages": [],
    }

    report = JsonFormatter().format(summary)

    assert json.loads(report) == summary


def test_formatter_factory_returns_text_formatter():
    formatter = FormatterFactory.create("txt")

    assert isinstance(formatter, TextFormatter)


def test_formatter_factory_returns_json_formatter():
    formatter = FormatterFactory.create("json")

    assert isinstance(formatter, JsonFormatter)


def test_formatter_factory_raises_for_unsupported_format():
    with pytest.raises(ValueError, match="Unsupported format"):
        FormatterFactory.create("xml")


def test_report_saver_writes_report(tmp_path):
    output_path = tmp_path / "report.txt"
    report = "Total lines: 3"

    result_path = ReportSaver(output_path).save(report)

    assert result_path == output_path.resolve()
    assert output_path.read_text(encoding="utf-8") == report


def test_report_saver_raises_for_empty_report(tmp_path):
    output_path = tmp_path / "report.txt"

    with pytest.raises(ValueError, match="Report cannot be empty"):
        ReportSaver(output_path).save("")


def test_log_processor_returns_formatted_report(tmp_path):
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

    processor = LogProcessor(
        loader=LogLoader(log_file),
        summarizer=LogSummarizer(),
        formatter=TextFormatter(),
    )

    report = processor.process()

    assert "Total lines: 2" in report
    assert "INFO: 1" in report
    assert "ERROR: 1" in report
    assert "- Something failed" in report


def test_app_container_runs_pipeline(tmp_path):
    input_path = tmp_path / "sample.txt"
    output_path = tmp_path / "report.txt"

    input_path.write_text(
        "2026-04-10 10:00:00 ERROR Something failed",
        encoding="utf-8",
    )

    config = AppConfig(
        input_path=input_path,
        output_path=output_path,
        format_type="txt",
    )

    report, saved_path = AppContainer(config).run()

    assert saved_path == output_path.resolve()
    assert output_path.read_text(encoding="utf-8") == report
    assert "ERROR: 1" in report


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
    expected_report = textwrap.dedent("""\
        Total lines: 8
        INFO: 4
        WARNING: 2
        ERROR: 2
        Error messages:
        - Database connection failed
        - Timeout while calling external API
        """).strip()

    assert captured.out.strip() == expected_report
    assert output_file.read_text(encoding="utf-8") == expected_report


def test_main_success_json_format(tmp_path, monkeypatch):
    log_file = tmp_path / "log.txt"
    output_base = tmp_path / "report"

    log_file.write_text(
        "2026-04-10 10:00:00 ERROR Something failed",
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
            str(output_base),
            "--format",
            "json",
        ],
    )

    return_code = main()

    assert return_code == 0

    output_file = tmp_path / "report.json"
    assert output_file.exists()

    content = json.loads(output_file.read_text(encoding="utf-8"))
    assert content["total_lines"] == 1
    assert content["error_count"] == 1
    assert content["error_messages"] == ["Something failed"]


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
    assert not (tmp_path / "report.txt").exists()

    captured = capsys.readouterr()
    assert captured.out.strip() == ""
    assert "doesn't exist" in caplog.text

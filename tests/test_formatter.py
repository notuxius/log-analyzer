import json
import textwrap

from log_analyzer.formatter import (
    CsvFormatter,
    FormatterFactory,
    HtmlFormatter,
    JsonFormatter,
    TextFormatter,
)
from log_analyzer.models import LogSummary
from tests.fakes.fake_formatter import FakeFormatter


def test_formatter_factory_registers_custom_formatter() -> None:
    FormatterFactory.register("fake", FakeFormatter)

    formatter = FormatterFactory.create("fake")

    summary: LogSummary = {
        "total_lines": 1,
        "debug_count": 0,
        "info_count": 1,
        "warning_count": 0,
        "error_count": 0,
        "error_messages": [],
    }

    assert formatter.format(summary) == "Processed 1 entries"


def test_text_formatter_returns_placeholder_when_no_errors():
    summary: LogSummary = {
        "total_lines": 1,
        "debug_count": 1,
        "info_count": 1,
        "warning_count": 0,
        "error_count": 0,
        "error_messages": [],
    }

    report = TextFormatter().format(summary)

    assert "- (none)" in report


def test_text_formatter_returns_expected_report():
    summary: LogSummary = {
        "total_lines": 3,
        "debug_count": 1,
        "info_count": 1,
        "warning_count": 1,
        "error_count": 1,
        "error_messages": ["Something failed"],
    }

    report = TextFormatter().format(summary)

    expected = textwrap.dedent("""\
        Total lines: 3
        DEBUG: 1
        INFO: 1
        WARNING: 1
        ERROR: 1
        Error messages:
        - Something failed
        """).strip()

    assert report == expected


def test_json_formatter_returns_valid_json():
    summary: LogSummary = {
        "total_lines": 1,
        "debug_count": 1,
        "info_count": 1,
        "warning_count": 0,
        "error_count": 0,
        "error_messages": [],
    }

    report = JsonFormatter().format(summary)

    assert json.loads(report) == summary


def test_csv_formatter_returns_csv_report() -> None:
    summary: LogSummary = {
        "total_lines": 3,
        "debug_count": 1,
        "info_count": 1,
        "warning_count": 0,
        "error_count": 1,
        "error_messages": ["Something failed"],
    }

    report = CsvFormatter().format(summary)

    assert "metric,value" in report
    assert "total_lines,3" in report
    assert "debug_count,1" in report
    assert "error_messages,Something failed" in report


def test_html_formatter_returns_html_report() -> None:
    summary: LogSummary = {
        "total_lines": 3,
        "debug_count": 1,
        "info_count": 1,
        "warning_count": 0,
        "error_count": 1,
        "error_messages": ["Something failed"],
    }

    report = HtmlFormatter().format(summary)

    assert "<html>" in report
    assert "<h1>Log Report</h1>" in report
    assert "<li>DEBUG: 1</li>" in report
    assert "<li>Something failed</li>" in report

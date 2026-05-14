import json
import textwrap

from log_analyzer.formatter import (
    JsonFormatter,
    TextFormatter,
)
from log_analyzer.models import LogSummary


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

from log_analyzer.analyzer import (
    LogSummarizer,
)
from log_analyzer.models import LogEntry, LogLevel


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

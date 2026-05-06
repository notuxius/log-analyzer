from log_analyzer.analyzer import (
    LogEntry,
    LogLoader,
    LogProcessor,
    LogSummarizer,
    LogSummary,
    TextFormatter,
)
from log_analyzer.models import LogLevel


class FakeLoader:
    def load(self) -> list[LogEntry]:
        return [
            {
                "timestamp": "2026-04-10 10:00:00",
                "level": LogLevel.INFO,
                "message": "Application started",
            },
            {
                "timestamp": "2026-04-10 10:01:00",
                "level": LogLevel.ERROR,
                "message": "Something failed",
            },
        ]


class FakeFormatter:
    def format(self, summary: LogSummary) -> str:
        return "FAKE REPORT"


def test_log_processor_with_fakes() -> None:
    processor = LogProcessor(
        loader=FakeLoader(),
        summarizer=LogSummarizer(),
        formatter=FakeFormatter(),
    )

    result = processor.process()
    assert result == "FAKE REPORT"


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

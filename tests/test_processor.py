from log_analyzer.analyzer import LogEntry, LogProcessor, LogSummarizer, LogSummary
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

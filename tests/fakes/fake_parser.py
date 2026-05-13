from log_analyzer.models import LogEntry, LogLevel


class FakeParser:
    def parse(self, line: str) -> LogEntry | None:
        return {
            "timestamp": "2026-01-01 00:00:00",
            "level": LogLevel.INFO,
            "message": "FAKE",
        }

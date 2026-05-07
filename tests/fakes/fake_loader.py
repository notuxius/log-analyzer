from collections.abc import Iterable

from log_analyzer.models import LogEntry, LogLevel


class FakeLoader:
    def load(self) -> Iterable[LogEntry]:
        yield {
            "timestamp": "2026-04-10 10:00:00",
            "level": LogLevel.INFO,
            "message": "Application started",
        }

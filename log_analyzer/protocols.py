from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Protocol

from log_analyzer.models import LogEntry, LogSummary


class Loader(Protocol):
    def load(self) -> Iterator[LogEntry]: ...


class Summarizer(Protocol):
    def summarize(self, entries: Iterable[LogEntry]) -> LogSummary: ...


class Formatter(Protocol):
    def format(self, summary: LogSummary) -> str: ...


class Saver(Protocol):
    def save(self, report: str) -> Path: ...

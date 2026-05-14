from dataclasses import dataclass
from enum import StrEnum
from typing import TypedDict


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass(frozen=True)
class LogEntry:
    timestamp: str
    level: LogLevel
    message: str


class LogSummary(TypedDict):
    total_lines: int
    debug_count: int
    info_count: int
    warning_count: int
    error_count: int
    error_messages: list[str]

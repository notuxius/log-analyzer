from collections.abc import Iterator
from pathlib import Path

from log_analyzer.exceptions import (
    EmptyLogFileError,
    InvalidLogLevelError,
    LogFileNotFoundError,
)
from log_analyzer.logger import AppLogger
from log_analyzer.models import LogEntry, LogLevel


class LogLoader:
    def __init__(self, log_file: str | Path, logger: AppLogger | None = None) -> None:
        self.log_file = Path(log_file)
        self.logger = logger or AppLogger()

    def _read_lines(self) -> Iterator[str]:
        if not self.log_file.exists():
            raise LogFileNotFoundError(f"Log file {self.log_file} doesn't exist.")

        with self.log_file.open(encoding="utf-8") as file:
            for line in file:
                yield line.rstrip("\n")

    def _parse_line(self, line: str) -> LogEntry | None:
        parts = line.split(" ", 3)

        if len(parts) != 4:
            self.logger.warning("Skipped malformed log message: %s", line)
            return None

        date_part, time_part, level_part, message_part = parts

        timestamp = f"{date_part} {time_part}"

        try:
            level = LogLevel(level_part)

        except ValueError as error:
            raise InvalidLogLevelError(
                f"Invalid log message level: {level_part}"
            ) from error

        if not message_part.strip():
            self.logger.warning("Skipped empty log message.")
            return None

        log_entry: LogEntry = {
            "timestamp": timestamp,
            "level": level,
            "message": message_part,
        }

        return log_entry

    def load(self) -> Iterator[LogEntry]:
        has_content = False

        for line in self._read_lines():
            if line.strip():
                has_content = True
            else:
                continue

            log_entry = self._parse_line(line)

            if log_entry is not None:
                yield log_entry

        if not has_content:
            raise EmptyLogFileError("Log file cannot be empty.")

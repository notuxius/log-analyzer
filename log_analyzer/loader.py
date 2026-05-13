from collections.abc import Iterator
from pathlib import Path

from log_analyzer.exceptions import (
    EmptyLogFileError,
    LogFileNotFoundError,
)
from log_analyzer.logger import AppLogger
from log_analyzer.models import LogEntry
from log_analyzer.parser import LogParser
from log_analyzer.protocols import Parser


class LogLoader:
    def __init__(
        self,
        log_file: str | Path,
        parser: Parser | None = None,
        logger: AppLogger | None = None,
    ) -> None:
        self.log_file = Path(log_file)
        self.parser = parser or LogParser()
        self.logger = logger or AppLogger()

    def _read_lines(self) -> Iterator[str]:
        if not self.log_file.exists():
            raise LogFileNotFoundError(f"Log file {self.log_file} doesn't exist.")

        with self.log_file.open(encoding="utf-8") as file:
            for line in file:
                yield line.rstrip("\n")

    def _parse_line(self, line: str) -> LogEntry | None:
        log_entry = self.parser.parse(line)

        if log_entry is None:
            self.logger.warning("Skipped malformed or empty log message: %s", line)
            return None

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

import gzip
import time
from collections.abc import Iterator
from pathlib import Path
from typing import TextIO

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
        self._running = False

    def _iter_file_lines(self, file: TextIO) -> Iterator[str]:
        for line in file:
            yield line.rstrip("\n")

    def _read_lines(self) -> Iterator[str]:
        if not self.log_file.exists():
            raise LogFileNotFoundError(f"Log file {self.log_file} doesn't exist.")
        if self.log_file.suffix == ".gz":
            with gzip.open(self.log_file, mode="rt", encoding="utf-8") as file:
                yield from self._iter_file_lines(file)
        else:
            with self.log_file.open(encoding="utf-8") as file:
                yield from self._iter_file_lines(file)

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

    def follow(self, poll_interval: float = 1.0) -> Iterator[LogEntry]:
        if not self.log_file.exists():
            raise LogFileNotFoundError(f"Log file {self.log_file} doesn't exist.")

        self._running = True

        with self.log_file.open(encoding="utf-8") as file:
            file.seek(0, 2)

            while self._running:
                line = file.readline()

                if not line:
                    time.sleep(poll_interval)
                    continue

                line = line.rstrip("\n")

                if not line.strip():
                    continue

                log_entry = self._parse_line(line)

                if log_entry is not None:
                    yield log_entry

    def stop(self) -> None:
        self._running = False

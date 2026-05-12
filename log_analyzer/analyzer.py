import json
from collections.abc import Iterable, Iterator
from pathlib import Path

from log_analyzer.exceptions import (
    EmptyLogFileError,
    EmptyReportError,
    InvalidLogLevelError,
    LogFileNotFoundError,
    UnsupportedFormatError,
)
from log_analyzer.logger import AppLogger
from log_analyzer.models import LogEntry, LogLevel, LogSummary
from log_analyzer.protocols import Formatter, Loader, Summarizer


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


class LogSummarizer:
    def summarize(self, entries: Iterable[LogEntry]) -> LogSummary:
        total_lines = 0
        info_count = 0
        warning_count = 0
        error_count = 0
        error_messages: list[str] = []

        for log_entry in entries:
            total_lines += 1
            log_entry_level = log_entry["level"]

            match log_entry_level:
                case LogLevel.INFO:
                    info_count += 1
                case LogLevel.WARNING:
                    warning_count += 1
                case LogLevel.ERROR:
                    error_count += 1
                    error_messages.append(log_entry["message"])

        log_summary: LogSummary = {
            "total_lines": total_lines,
            "info_count": info_count,
            "warning_count": warning_count,
            "error_count": error_count,
            "error_messages": error_messages,
        }

        return log_summary


class TextFormatter:
    def format(self, summary: LogSummary) -> str:
        lines = [
            f"Total lines: {summary['total_lines']}",
            f"INFO: {summary['info_count']}",
            f"WARNING: {summary['warning_count']}",
            f"ERROR: {summary['error_count']}",
            "Error messages:",
        ]

        if summary["error_messages"]:
            lines.extend(
                f"- {error_message}" for error_message in summary["error_messages"]
            )
        else:
            lines.append("- (none)")

        return "\n".join(lines)


class JsonFormatter:
    def format(self, summary: LogSummary) -> str:
        return json.dumps(summary, indent=2)


class LogProcessor:
    def __init__(
        self, loader: Loader, summarizer: Summarizer, formatter: Formatter
    ) -> None:
        self.loader = loader
        self.summarizer = summarizer
        self.formatter = formatter

    def process(self) -> str:
        entries = self.loader.load()
        summary = self.summarizer.summarize(entries)
        return self.formatter.format(summary)


class FormatterFactory:
    FORMATTERS = {
        "txt": TextFormatter,
        "json": JsonFormatter,
    }

    @staticmethod
    def create(format_type: str) -> Formatter:
        format_type = format_type.lower()
        try:
            formatter_class = FormatterFactory.FORMATTERS[format_type]
        except KeyError as error:
            raise UnsupportedFormatError(
                f"Unsupported format: {format_type}"
            ) from error

        return formatter_class()


class ReportSaver:
    def __init__(self, output_path: Path | str) -> None:
        self.file_path = Path(output_path)

    def save(self, report: str) -> Path:
        if not report.strip():
            raise EmptyReportError("Report cannot be empty.")

        path = self.file_path.resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")

        return path

import json
from pathlib import Path
from typing import Protocol

from log_analyzer.models import LogEntry, LogLevel, LogSummary


class Loader(Protocol):
    def load(self) -> list[LogEntry]: ...


class Summarizer(Protocol):
    def summarize(self, entries: list[LogEntry]) -> LogSummary: ...


class Formatter(Protocol):
    def format(self, summary: LogSummary) -> str: ...


class Saver(Protocol):
    def save(self, report: str) -> Path: ...


class LogLoader:
    def __init__(self, log_file: str | Path) -> None:
        self.log_file = Path(log_file)

    def _read_lines(self) -> list[str]:
        if not self.log_file.exists():
            raise FileNotFoundError(f"Log file {self.log_file} doesn't exist.")

        lines = self.log_file.read_text(encoding="utf-8").splitlines()
        if not any(line.strip() for line in lines):
            raise ValueError("Log file cannot be empty.")
        return lines

    def _parse_line(self, line: str) -> LogEntry | None:
        parts = line.split(" ", 3)

        if len(parts) != 4:
            # logging.warning("Skipped malformed log message: %s", line)
            return None

        date_part, time_part, level_part, message_part = parts

        timestamp = f"{date_part} {time_part}"

        try:
            level = LogLevel(level_part)

        except ValueError as error:
            raise ValueError(f"Invalid log message level: {level_part}") from error

        if not message_part.strip():
            # logging.warning("Skipped empty log message: %s", message_part)
            return None

        log_entry: LogEntry = {
            "timestamp": timestamp,
            "level": level,
            "message": message_part,
        }

        return log_entry

    def load(self) -> list[LogEntry]:
        lines = self._read_lines()
        log_entries: list[LogEntry] = []

        for line in lines:
            if not line.strip():
                continue

            log_entry = self._parse_line(line)

            if log_entry is not None:
                log_entries.append(log_entry)

        return log_entries


class LogSummarizer:
    def summarize(self, entries: list[LogEntry]) -> LogSummary:
        info_count = 0
        warning_count = 0
        error_count = 0
        error_messages: list[str] = []

        for log_entry in entries:
            log_entry_level = log_entry["level"]
            if log_entry_level == LogLevel.INFO:
                info_count += 1
            elif log_entry_level == LogLevel.WARNING:
                warning_count += 1
            elif log_entry_level == LogLevel.ERROR:
                error_count += 1
                error_messages.append(log_entry["message"])

        log_summary: LogSummary = {
            "total_lines": len(entries),
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
        loaded = self.loader.load()
        summary = self.summarizer.summarize(loaded)
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
            raise ValueError(f"Unsupported format: {format_type}") from error

        return formatter_class()


class ReportSaver:
    def __init__(self, output_path: Path | str) -> None:
        self.file_path = Path(output_path)

    def save(self, report: str) -> Path:
        if not report.strip():
            raise ValueError("Report cannot be empty.")

        path = self.file_path.resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")

        return path

import logging
from pathlib import Path

from log_analyzer.models import LogEntry, LogLevel, LogSummary


def load_log_entries(log_file: str | Path) -> list[LogEntry]:
    path = Path(log_file)

    if not path.exists():
        raise FileNotFoundError(f"Log file {path} doesn't exist.")

    lines = path.read_text(encoding="utf-8").splitlines()
    if not any(line.strip() for line in lines):
        raise ValueError("Log file cannot be empty.")

    log_entries: list[LogEntry] = []

    for line in lines:
        if not line.strip():
            continue

        parts = line.split(" ", 3)

        if len(parts) != 4:
            logging.warning("Skipped malformed log message: %s", line)
            continue

        date_part, time_part, level_part, message_part = parts

        timestamp = f"{date_part} {time_part}"

        try:
            level = LogLevel(level_part)

        except ValueError as error:
            raise ValueError(f"Invalid log message level: {level_part}") from error

        if not message_part.strip():
            logging.warning("Skipped empty log message: %s", message_part)
            continue

        log_entry: LogEntry = {
            "timestamp": timestamp,
            "level": level,
            "message": message_part,
        }

        log_entries.append(log_entry)

    return log_entries


def format_log_report(log_summary: LogSummary) -> str:
    lines = [
        f"Total lines: {log_summary['total_lines']}",
        f"INFO: {log_summary['info_count']}",
        f"WARNING: {log_summary['warning_count']}",
        f"ERROR: {log_summary['error_count']}",
        "Error messages:",
    ]

    if log_summary["error_messages"]:
        lines.extend(
            f"- {error_message}" for error_message in log_summary["error_messages"]
        )
    else:
        lines.append("- (none)")

    return "\n".join(lines)


def save_report(report: str, file_path: Path | str) -> Path:
    if not report.strip():
        raise ValueError("Report cannot be empty.")

    path = Path(file_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")

    return path

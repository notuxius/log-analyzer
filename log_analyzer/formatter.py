import json

from log_analyzer.exceptions import (
    UnsupportedFormatError,
)
from log_analyzer.models import LogSummary
from log_analyzer.protocols import Formatter


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

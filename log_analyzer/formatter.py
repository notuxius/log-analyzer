import csv
import json
from io import StringIO

from log_analyzer.exceptions import (
    UnsupportedFormatError,
)
from log_analyzer.models import LogSummary
from log_analyzer.protocols import Formatter


class TextFormatter:
    def format(self, summary: LogSummary) -> str:
        lines = [
            f"Total lines: {summary['total_lines']}",
            f"DEBUG: {summary['debug_count']}",
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


class CsvFormatter:
    def format(self, summary: LogSummary) -> str:
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(["metric", "value"])
        writer.writerow(["total_lines", summary["total_lines"]])
        writer.writerow(["debug_count", summary["debug_count"]])
        writer.writerow(["info_count", summary["info_count"]])
        writer.writerow(["warning_count", summary["warning_count"]])
        writer.writerow(["error_count", summary["error_count"]])
        writer.writerow(["error_messages", "; ".join(summary["error_messages"])])

        return output.getvalue().strip()


class FormatterFactory:
    FORMATTERS = {
        "txt": TextFormatter,
        "json": JsonFormatter,
        "csv": CsvFormatter,
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

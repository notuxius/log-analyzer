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


class HtmlFormatter:
    def format(self, summary: LogSummary) -> str:
        error_items = "\n".join(
            f"<li>{error_message}</li>" for error_message in summary["error_messages"]
        )

        if not error_items:
            error_items = "<li>(none)</li>"

        return f"""<!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Log Report</title>
                </head>
                <body>
                    <h1>Log Report</h1>
                    <ul>
                        <li>Total lines: {summary["total_lines"]}</li>
                        <li>DEBUG: {summary["debug_count"]}</li>
                        <li>INFO: {summary["info_count"]}</li>
                        <li>WARNING: {summary["warning_count"]}</li>
                        <li>ERROR: {summary["error_count"]}</li>
                    </ul>
                    <h2>Error messages</h2>
                    <ul>
                        {error_items}
                    </ul>
                </body>
                </html>"""


class FormatterFactory:
    FORMATTER_REGISTRY: dict[str, type[Formatter]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        formatter_class: type[Formatter],
    ) -> None:
        cls.FORMATTER_REGISTRY[name.lower()] = formatter_class

    @classmethod
    def create(cls, format_type: str) -> Formatter:
        format_type = format_type.lower()
        try:
            formatter_class = cls.FORMATTER_REGISTRY[format_type]
        except KeyError as error:
            raise UnsupportedFormatError(
                f"Unsupported format: {format_type}"
            ) from error

        return formatter_class()


BUILTIN_FORMATTERS: dict[str, type[Formatter]] = {
    "txt": TextFormatter,
    "json": JsonFormatter,
    "csv": CsvFormatter,
    "html": HtmlFormatter,
}

for name, formatter_class in BUILTIN_FORMATTERS.items():
    FormatterFactory.register(name, formatter_class)


def available_formats() -> tuple[str, ...]:
    return tuple(FormatterFactory.FORMATTER_REGISTRY)

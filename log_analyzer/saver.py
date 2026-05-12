from pathlib import Path

from log_analyzer.exceptions import (
    EmptyReportError,
)


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

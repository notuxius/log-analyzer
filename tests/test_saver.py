import pytest

from log_analyzer.analyzer import (
    ReportSaver,
)
from log_analyzer.exceptions import (
    EmptyReportError,
)


def test_report_saver_writes_report(tmp_path):
    output_path = tmp_path / "report.txt"
    report = "Total lines: 3"

    result_path = ReportSaver(output_path).save(report)

    assert result_path == output_path.resolve()
    assert output_path.read_text(encoding="utf-8") == report


def test_report_saver_raises_for_empty_report(tmp_path):
    output_path = tmp_path / "report.txt"

    with pytest.raises(EmptyReportError, match="Report cannot be empty"):
        ReportSaver(output_path).save("")

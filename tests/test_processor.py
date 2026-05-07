from log_analyzer.analyzer import (
    LogLoader,
    LogProcessor,
    LogSummarizer,
    TextFormatter,
)
from tests.fakes.fake_formatter import FakeFormatter
from tests.fakes.fake_loader import FakeLoader


def test_log_processor_with_fakes() -> None:
    processor = LogProcessor(
        loader=FakeLoader(),
        summarizer=LogSummarizer(),
        formatter=FakeFormatter(),
    )

    result = processor.process()
    assert result == "Processed 1 entries"


def test_log_processor_returns_formatted_report(tmp_path):
    log_file = tmp_path / "log.txt"
    log_file.write_text(
        "\n".join(
            [
                "2026-04-10 10:00:00 INFO Application started",
                "2026-04-10 10:01:00 ERROR Something failed",
            ]
        ),
        encoding="utf-8",
    )

    processor = LogProcessor(
        loader=LogLoader(log_file),
        summarizer=LogSummarizer(),
        formatter=TextFormatter(),
    )

    report = processor.process()

    assert "Total lines: 2" in report
    assert "INFO: 1" in report
    assert "ERROR: 1" in report
    assert "- Something failed" in report

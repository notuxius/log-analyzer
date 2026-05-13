from pathlib import Path

import pytest

from log_analyzer.exceptions import (
    EmptyLogFileError,
    LogFileNotFoundError,
)
from log_analyzer.loader import LogLoader
from log_analyzer.models import LogLevel
from tests.fakes.fake_parser import FakeParser


def test_log_loader_returns_iterator(tmp_path: Path) -> None:
    log_file = tmp_path / "log.txt"

    log_file.write_text(
        "2026-04-10 10:00:00 INFO Application started",
        encoding="utf-8",
    )

    entries = LogLoader(log_file).load()

    assert iter(entries) is entries


def test_log_loader_loads_valid_entries(tmp_path: Path) -> None:
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

    entries = list(LogLoader(log_file).load())

    assert len(entries) == 2
    assert entries[0].level == LogLevel.INFO
    assert entries[1].level == LogLevel.ERROR
    assert entries[0].message == "Application started"
    assert entries[1].message == "Something failed"


def test_log_loader_skips_blank_lines(tmp_path: Path) -> None:
    log_file = tmp_path / "log.txt"
    log_file.write_text(
        "\n".join(
            [
                "",
                "2026-04-10 10:00:00 INFO Application started",
                "",
                "2026-04-10 10:01:00 ERROR Something failed",
                "",
            ]
        ),
        encoding="utf-8",
    )

    entries = list(LogLoader(log_file).load())

    assert len(entries) == 2
    assert entries[0].message == "Application started"
    assert entries[1].message == "Something failed"


def test_log_loader_logs_warning_for_malformed_line(
    tmp_path: Path,
    capsys,
) -> None:
    log_file = tmp_path / "log.txt"

    log_file.write_text(
        "\n".join(
            [
                "malformed line",
                "2026-04-10 10:00:00 INFO Application started",
            ]
        ),
        encoding="utf-8",
    )

    entries = list(LogLoader(log_file).load())
    captured = capsys.readouterr()

    assert len(entries) == 1
    assert "Skipped malformed or empty log message" in captured.err


def test_log_loader_logs_warning_for_empty_message(
    tmp_path: Path,
    capsys,
) -> None:
    log_file = tmp_path / "log.txt"

    log_file.write_text(
        "2026-04-10 10:00:00 INFO    ",
        encoding="utf-8",
    )

    entries = list(LogLoader(log_file).load())
    captured = capsys.readouterr()

    assert entries == []
    assert "Skipped malformed or empty log message" in captured.err


def test_log_loader_raises_for_empty_file(tmp_path: Path) -> None:
    log_file = tmp_path / "empty.txt"
    log_file.write_text("", encoding="utf-8")

    with pytest.raises(EmptyLogFileError, match="Log file cannot be empty"):
        list(LogLoader(log_file).load())


def test_log_loader_raises_for_missing_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(LogFileNotFoundError, match="doesn't exist"):
        list(LogLoader(missing_file).load())


def test_log_loader_uses_injected_parser(tmp_path: Path) -> None:
    log_file = tmp_path / "log.txt"

    log_file.write_text(
        "anything",
        encoding="utf-8",
    )

    loader = LogLoader(
        log_file,
        parser=FakeParser(),
    )

    entries = list(loader.load())

    assert entries[0].message == "FAKE"

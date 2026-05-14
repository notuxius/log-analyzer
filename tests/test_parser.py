import pytest

from log_analyzer.exceptions import InvalidLogLevelError
from log_analyzer.models import LogLevel
from log_analyzer.parser import LogParser


def test_log_parser_parses_valid_info_entry() -> None:
    line = "2026-04-10 10:00:00 INFO Application started"

    entry = LogParser().parse(line)

    assert entry is not None
    assert entry.timestamp == "2026-04-10 10:00:00"
    assert entry.level == LogLevel.INFO
    assert entry.message == "Application started"


def test_log_parser_parses_valid_error_entry() -> None:
    line = "2026-04-10 10:01:00 ERROR Something failed"

    entry = LogParser().parse(line)

    assert entry is not None
    assert entry.timestamp == "2026-04-10 10:01:00"
    assert entry.level == LogLevel.ERROR
    assert entry.message == "Something failed"


def test_log_parser_parses_valid_debug_entry() -> None:
    line = "2026-04-10 10:01:00 DEBUG Application initialized"

    entry = LogParser().parse(line)

    assert entry is not None
    assert entry.timestamp == "2026-04-10 10:01:00"
    assert entry.level == LogLevel.DEBUG
    assert entry.message == "Application initialized"


def test_log_parser_returns_none_for_empty_message() -> None:
    line = "2026-04-10 10:00:00 INFO    "

    entry = LogParser().parse(line)

    assert entry is None


def test_log_parser_returns_none_for_malformed_line() -> None:
    line = "malformed line"

    entry = LogParser().parse(line)

    assert entry is None


def test_log_parser_raises_for_invalid_level() -> None:
    line = "2026-04-10 10:01:00 error Something failed"

    with pytest.raises(InvalidLogLevelError, match="Invalid log message level"):
        LogParser().parse(line)

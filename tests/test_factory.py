import pytest

from log_analyzer.exceptions import (
    UnsupportedFormatError,
)
from log_analyzer.formatter import (
    CsvFormatter,
    FormatterFactory,
    JsonFormatter,
    TextFormatter,
)


def test_formatter_factory_returns_text_formatter():
    formatter = FormatterFactory.create("txt")

    assert isinstance(formatter, TextFormatter)


def test_formatter_factory_returns_json_formatter():
    formatter = FormatterFactory.create("json")

    assert isinstance(formatter, JsonFormatter)


def test_formatter_factory_returns_csv_formatter() -> None:
    formatter = FormatterFactory.create("csv")

    assert isinstance(formatter, CsvFormatter)


def test_formatter_factory_raises_for_unsupported_format():
    with pytest.raises(UnsupportedFormatError, match="Unsupported format"):
        FormatterFactory.create("xml")

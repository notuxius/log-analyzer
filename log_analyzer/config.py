from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from log_analyzer.exceptions import UnsupportedFormatError
from log_analyzer.formatters import FormatterFactory


@dataclass
class AppConfig:
    input_path: Path
    output_path: Path
    format_type: str

    @classmethod
    def create(
        cls,
        input_path: Path | str,
        output_path: Path | str,
        format_type: str,
    ) -> AppConfig:
        return cls(
            input_path=Path(input_path),
            output_path=Path(output_path),
            format_type=format_type,
        )

    def __post_init__(self) -> None:
        self.format_type = self.format_type.lower()

        if self.format_type not in FormatterFactory.FORMATTERS:
            raise UnsupportedFormatError(f"Unsupported format: {self.format_type}")

        if not self.output_path.suffix:
            self.output_path = self.output_path.with_suffix(f".{self.format_type}")

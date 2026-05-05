from dataclasses import dataclass
from pathlib import Path
from log_analyzer.analyzer import FormatterFactory


@dataclass
class AppConfig:
    input_path: Path | str
    output_path: Path | str
    format_type: str

    def __post_init__(self) -> None:
        self.input_path = Path(self.input_path)
        self.output_path = Path(self.output_path)
        self.format_type = self.format_type.lower()

        if self.format_type not in FormatterFactory.FORMATTERS:
            raise ValueError(f"Unsupported format: {self.format_type}")

        if not self.output_path.suffix:
            self.output_path = self.output_path.with_suffix(f".{self.format_type}")

from pathlib import Path
from dataclasses import dataclass


@dataclass
class AppConfig:
    input_path: Path
    output_path: Path
    format_type: str

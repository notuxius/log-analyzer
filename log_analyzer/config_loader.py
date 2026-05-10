import json
from pathlib import Path

from log_analyzer.config import AppConfig
from log_analyzer.exceptions import LogFileNotFoundError


class ConfigLoader:
    def __init__(self, config_path: Path | str) -> None:
        self.config_path = Path(config_path)

    def load(self) -> AppConfig:
        if not self.config_path.exists():
            raise LogFileNotFoundError(f"Config file {self.config_path} doesn't exist.")

        data = json.loads(self.config_path.read_text(encoding="utf-8"))

        return AppConfig.create(
            input_path=data["input_path"],
            output_path=data["output_path"],
            format_type=data["format_type"],
        )

import json
from json import JSONDecodeError
from pathlib import Path

from log_analyzer.config import AppConfig
from log_analyzer.exceptions import InvalidConfigError, LogFileNotFoundError


class ConfigLoader:
    def __init__(self, config_path: Path | str) -> None:
        self.config_path = Path(config_path)

    def load(self) -> AppConfig:
        if not self.config_path.exists():
            raise LogFileNotFoundError(f"Config file {self.config_path} doesn't exist.")

        try:
            data = json.loads(self.config_path.read_text(encoding="utf-8"))
        except JSONDecodeError as error:
            raise InvalidConfigError(
                f"Config file {self.config_path} contains invalid JSON."
            ) from error

        required_fields = ("input_path", "output_path", "format_type")
        missing_fields = {field for field in required_fields if field not in data}

        if missing_fields:
            raise InvalidConfigError(
                f"Config file {self.config_path} is missing required fields: "
                f"{', '.join(missing_fields)}"
            )

        return AppConfig.create(
            input_path=data["input_path"],
            output_path=data["output_path"],
            format_type=data["format_type"],
        )

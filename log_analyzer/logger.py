import logging

from log_analyzer.constants import APP_NAME


class AppLogger:
    def __init__(self, level: str = "INFO") -> None:
        numeric_level = getattr(logging, level.upper(), logging.INFO)

        logging.basicConfig(
            level=numeric_level,
            format="%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
            force=True,
        )

        self.logger = logging.getLogger(APP_NAME)
        self.logger.setLevel(numeric_level)

    def debug(self, message: str, *args: object) -> None:
        self.logger.debug(message, *args)

    def info(self, message: str, *args: object) -> None:
        self.logger.info(message, *args)

    def warning(self, message: str, *args: object) -> None:
        self.logger.warning(message, *args)

    def error(self, message: str, *args: object) -> None:
        self.logger.error(message, *args)

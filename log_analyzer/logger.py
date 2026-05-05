import logging


class AppLogger:
    def __init__(self, level: str = "INFO") -> None:
        logging.basicConfig(
            level=getattr(logging, level.upper(), logging.INFO),
            format="%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
        )

    def info(self, message: str, *args: object) -> None:
        logging.info(message, *args)

    def error(self, message: str, *args: object) -> None:
        logging.error(message, *args)

import logging


class AppLogger:
    def info(self, message: str, *args: object) -> None:
        logging.info(message, *args)

    def error(self, message: str, *args: object) -> None:
        logging.error(message, *args)

import logging

from log_analyzer.constants import APP_NAME
from log_analyzer.logger import AppLogger


def test_logger_uses_requested_level() -> None:
    logger = AppLogger("DEBUG")

    assert logger.logger.getEffectiveLevel() == logging.DEBUG


def test_logger_has_correct_name() -> None:
    logger = AppLogger()

    assert logger.logger.name == APP_NAME

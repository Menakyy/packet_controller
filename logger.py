import logging
from typing import List


class DebugFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelname == "DEBUG"


def _add_basic_handler(logger: logging.Logger) -> logging.Logger:
    if not any(
        isinstance(handler, logging.StreamHandler) and handler.level == logging.INFO
        for handler in logger.handlers
    ):
        basic_logger_handler = logging.StreamHandler()
        basic_logger_handler.setLevel(logging.INFO)
        basic_logger_format = logging.Formatter(
            "%(asctime)s - %(message)s",
            "%d-%b-%y %H:%M:%S",
        )
        basic_logger_handler.setFormatter(basic_logger_format)
        logger.addHandler(basic_logger_handler)
    return logger


def _add_advance_handler(logger: logging.Logger) -> logging.Logger:
    if not any(
        isinstance(handler, logging.StreamHandler) and handler.level == logging.DEBUG
        for handler in logger.handlers
    ):
        advanced_logger_handler = logging.StreamHandler()
        advanced_logger_handler.setLevel(logging.DEBUG)
        advanced_logger_format = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
            "%d-%b-%y %H:%M:%S",
        )
        advanced_logger_handler.setFormatter(advanced_logger_format)
        advanced_logger_handler.addFilter(DebugFilter())
        logger.addHandler(advanced_logger_handler)
    return logger


def init(logger_names: List[str], logger_level: int) -> None:
    for loger_name in logger_names:
        logger = logging.getLogger(loger_name)
        logger.setLevel(logging.getLevelName(logger_level))
        _add_advance_handler(logger)
        _add_basic_handler(logger)

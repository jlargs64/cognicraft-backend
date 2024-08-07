import logging

from pythonjsonlogger import jsonlogger

from app.core.settings import Settings, get_settings


def configure_logging() -> None:
    """Configure the JSON logger"""
    logger = logging.getLogger()
    _set_logging_level(logger)
    _set_handlers(logger)


def _set_handlers(logger: logging.Logger) -> None:
    """Set all the handlers in the logger

    Args:
        logger (logging.Logger): The logger ot set the handler for
    """
    _set_json_handler(logger)


def _set_json_handler(logger: logging.Logger) -> None:
    """Set the JSON handler up for logger

    Args:
        logger (logging.Logger): The logger to set the handler for
    """
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)


def _set_logging_level(logger: logging.Logger, settings: Settings) -> None:
    """Sets the logging level based on env level.

    Args:
        logger (logging.Logger): Logger to use log level
        settings (Settings): The settings to find env info
    """
    if settings.env == "dev":
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO
    logger.setLevel(logging_level)

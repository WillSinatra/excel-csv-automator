"""Centralized logging module with colored console output.

Usage:
    from modules.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Ready.")
"""

import logging
from pathlib import Path

from colorama import Fore, Style, init

init(autoreset=True)


class _ColoredFormatter(logging.Formatter):
    """Formatter that adds ANSI color codes based on log level."""

    _COLORS: dict[int, str] = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record: logging.LogRecord) -> str:  # noqa: A003
        color = self._COLORS.get(record.levelno, "")
        record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger with file and colored console handlers.

    Args:
        name: Logger name, typically ``__name__``.

    Returns:
        A fully configured :class:`logging.Logger` instance.
    """
    # Evitar duplicar handlers si el logger ya existe
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Importación diferida para evitar dependencia circular
    import config  # noqa: PLC0415

    # Crear directorio de logs si no existe
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file: Path = config.LOG_DIR / "app.log"

    # Handler de archivo — nivel DEBUG
    file_handler = logging.FileHandler(log_file, encoding=config.ENCODING)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt=config.DATE_FORMAT,
        )
    )

    # Handler de consola — nivel INFO con colores
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        _ColoredFormatter(
            fmt="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%H:%M:%S",
        )
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

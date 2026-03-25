"""Rotating log setup for Bob runtime diagnostics."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from pathlib import Path


@dataclass(frozen=True)
class LoggingConfig:
    """Settings for local rotating log behavior."""

    directory: str = "logs"
    filename: str = "bob.log"
    level: str = "INFO"
    max_bytes: int = 1_048_576
    backup_count: int = 3


def build_rotating_file_handler(config: LoggingConfig) -> RotatingFileHandler:
    """Create a rotating file handler and ensure the log directory exists."""
    log_dir = Path(config.directory)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / config.filename
    handler = RotatingFileHandler(
        log_path,
        maxBytes=config.max_bytes,
        backupCount=config.backup_count,
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )
    return handler


def configure_logging(
    logger_name: str,
    config: LoggingConfig,
    *,
    handler: logging.Handler | None = None,
) -> logging.Logger:
    """Configure a named logger for local runtime diagnostics."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, config.level.upper(), logging.INFO))
    logger.propagate = False

    for existing in list(logger.handlers):
        logger.removeHandler(existing)
        try:
            existing.close()
        except Exception:
            pass

    logger.addHandler(handler or build_rotating_file_handler(config))
    return logger

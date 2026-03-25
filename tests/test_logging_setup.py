"""Tests for rotating log configuration."""

from __future__ import annotations

import logging
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.observability import LoggingConfig, configure_logging


def test_configure_logging_creates_rotating_file_handler(tmp_path: Path) -> None:
    logger = configure_logging(
        "bob.test.logging",
        LoggingConfig(
            directory=str(tmp_path / "logs"),
            filename="bob-test.log",
            level="DEBUG",
            max_bytes=256,
            backup_count=2,
        ),
    )

    logger.debug("hello logger")

    log_path = tmp_path / "logs" / "bob-test.log"
    assert logger.level == logging.DEBUG
    assert log_path.exists() is True
    assert "hello logger" in log_path.read_text(encoding="utf-8")

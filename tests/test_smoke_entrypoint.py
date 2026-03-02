"""Smoke tests for bootstrap entrypoint."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def _run_bob(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR / "src")
    return subprocess.run(
        [sys.executable, "-m", "bob", *args],
        cwd=ROOT_DIR,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def test_module_entrypoint_version() -> None:
    result = _run_bob("--version")
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "0.1.0"


def test_module_entrypoint_default() -> None:
    result = _run_bob()
    assert result.returncode == 0, result.stderr
    assert "bootstrap entrypoint ready" in result.stdout.lower()

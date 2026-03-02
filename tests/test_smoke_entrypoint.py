"""Smoke tests for bootstrap entrypoint."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.audio.devices import format_audio_devices


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


def test_format_audio_devices_output() -> None:
    lines = format_audio_devices(
        [
            {
                "name": "Mic Device",
                "max_input_channels": 1,
                "max_output_channels": 0,
            }
        ]
    )
    assert lines[0] == "Detected audio devices:"
    assert "Mic Device" in lines[1]

"""Unit tests for audio device discovery helpers."""

from __future__ import annotations

import builtins
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.audio.devices import format_audio_devices, print_audio_devices


def test_format_audio_devices_empty() -> None:
    assert format_audio_devices([]) == ["No audio devices found."]


def test_format_audio_devices_missing_fields() -> None:
    lines = format_audio_devices([{"name": "Unknown Device"}])
    assert lines[0] == "Detected audio devices:"
    assert "Unknown Device" in lines[1]
    assert "inputs=0" in lines[1]
    assert "outputs=0" in lines[1]


def test_print_audio_devices_success(monkeypatch, capsys) -> None:
    class FakeSoundDevice:
        @staticmethod
        def query_devices():
            return [
                {
                    "name": "Fake Mic",
                    "max_input_channels": 1,
                    "max_output_channels": 0,
                }
            ]

    monkeypatch.setitem(sys.modules, "sounddevice", FakeSoundDevice)

    result = print_audio_devices()
    output = capsys.readouterr().out

    assert result == 0
    assert "Detected audio devices:" in output
    assert "Fake Mic" in output


def test_print_audio_devices_missing_dependency(monkeypatch, capsys) -> None:
    monkeypatch.delitem(sys.modules, "sounddevice", raising=False)
    real_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "sounddevice":
            raise ImportError("sounddevice not available")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    result = print_audio_devices()
    output = capsys.readouterr().out

    assert result == 1
    assert "sounddevice is not installed" in output

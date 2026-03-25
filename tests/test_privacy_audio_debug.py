"""Tests for privacy gating around raw debug audio capture."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from _testing import run_audio_capture_wav, run_utterance_record


def write_config(path: Path, allow_debug_audio_capture: bool) -> None:
    payload = {
        "project": {"name": "Bob", "environment": "development", "log_level": "INFO"},
        "assistant": {
            "name": "Bob",
            "wake_phrase": "Hey Bob",
            "deterministic_reply": "Hello, I'm here.",
            "start_muted": False,
        },
        "timeouts": {
            "listen_seconds": 8,
            "response_start_seconds": 3,
            "network_fallback_seconds": 5,
        },
        "audio": {
            "input_device": "default",
            "output_device": "default",
            "sample_rate_hz": 16000,
            "watchdog_timeout_seconds": 5,
        },
        "actions": {"open_app": {"enabled": True, "aliases": {"calculator": "calc.exe"}}},
        "stt": {
            "engine": "vosk",
            "model_path": "models/vosk/model",
            "language": "en",
            "sample_rate_hz": 16000,
            "fallback_engine": None,
        },
        "tts": {"engine": "pyttsx3", "speech_rate": 150, "voice_id": None},
        "observability": {
            "logs_directory": "logs",
            "log_filename": "bob.log",
            "log_max_bytes": 1048576,
            "log_backup_count": 3,
            "health_summary_interval_seconds": 300,
        },
        "privacy": {"allow_debug_audio_capture": allow_debug_audio_capture},
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_audio_capture_wav_refuses_without_explicit_opt_in(tmp_path: Path) -> None:
    config_path = tmp_path / "settings.json"
    write_config(config_path, allow_debug_audio_capture=False)

    result = run_audio_capture_wav(
        seconds=0.0,
        output=str(tmp_path / "capture.wav"),
        allow_debug_audio=False,
        config_path=str(config_path),
    )

    assert result == 1
    assert (tmp_path / "capture.wav").exists() is False


def test_utterance_record_refuses_without_explicit_opt_in(tmp_path: Path) -> None:
    config_path = tmp_path / "settings.json"
    write_config(config_path, allow_debug_audio_capture=False)

    result = run_utterance_record(
        output=str(tmp_path / "utterance.wav"),
        allow_debug_audio=False,
        config_path=str(config_path),
    )

    assert result == 1
    assert (tmp_path / "utterance.wav").exists() is False

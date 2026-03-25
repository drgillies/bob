"""Tests for centralized config loading and validation."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.config import ConfigError, load_app_config, load_open_app_settings, load_stt_settings


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def base_payload() -> dict:
    return {
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
        "actions": {
            "open_app": {
                "enabled": True,
                "aliases": {"calculator": "calc.exe"},
            }
        },
        "stt": {
            "engine": "vosk",
            "model_path": "models/vosk/model",
            "language": "en",
            "fallback_engine": None,
        },
        "tts": {
            "engine": "pyttsx3",
            "speech_rate": 150,
            "voice_id": None,
        },
        "observability": {
            "logs_directory": "logs",
            "log_filename": "bob.log",
            "log_max_bytes": 1048576,
            "log_backup_count": 3,
            "health_summary_interval_seconds": 300,
        },
        "privacy": {
            "allow_debug_audio_capture": False,
        },
    }


def test_load_app_config_merges_example_and_local_override(tmp_path: Path) -> None:
    example_path = tmp_path / "settings.example.json"
    local_path = tmp_path / "settings.local.json"
    env_path = tmp_path / ".env"
    write_json(example_path, base_payload())
    write_json(
        local_path,
        {
            "assistant": {"wake_phrase": "Yo Bob"},
            "actions": {"open_app": {"aliases": {"notepad": "notepad.exe"}}},
            "stt": {"sample_rate_hz": 22050},
        },
    )
    env_path.write_text("OPENAI_API_KEY=test-key\n", encoding="utf-8")

    config = load_app_config(
        example_path=example_path,
        local_path=local_path,
        env_path=env_path,
        environ={},
    )

    assert config.assistant.wake_phrase == "Yo Bob"
    assert config.actions.open_app.aliases == {
        "calculator": "calc.exe",
        "notepad": "notepad.exe",
    }
    assert config.stt.sample_rate_hz == 22050
    assert config.audio.watchdog_timeout_seconds == 5
    assert config.privacy.allow_debug_audio_capture is False
    assert config.secrets.values["OPENAI_API_KEY"] == "test-key"


def test_load_app_config_prefers_environment_secret_over_dotenv(tmp_path: Path) -> None:
    example_path = tmp_path / "settings.example.json"
    env_path = tmp_path / ".env"
    write_json(example_path, base_payload())
    env_path.write_text("OPENAI_API_KEY=file-key\n", encoding="utf-8")

    config = load_app_config(
        example_path=example_path,
        local_path=tmp_path / "missing.local.json",
        env_path=env_path,
        environ={"OPENAI_API_KEY": "env-key"},
    )

    assert config.secrets.values["OPENAI_API_KEY"] == "env-key"


def test_load_app_config_rejects_missing_required_field(tmp_path: Path) -> None:
    example_path = tmp_path / "settings.example.json"
    payload = base_payload()
    del payload["assistant"]["wake_phrase"]
    write_json(example_path, payload)

    try:
        load_app_config(
            example_path=example_path,
            local_path=tmp_path / "missing.local.json",
            env_path=tmp_path / ".env",
            environ={},
        )
        assert False, "Expected ConfigError"
    except ConfigError as exc:
        assert "wake_phrase" in str(exc)


def test_load_app_config_rejects_invalid_timeout_type(tmp_path: Path) -> None:
    example_path = tmp_path / "settings.example.json"
    payload = base_payload()
    payload["timeouts"]["listen_seconds"] = "fast"
    write_json(example_path, payload)

    try:
        load_app_config(
            example_path=example_path,
            local_path=tmp_path / "missing.local.json",
            env_path=tmp_path / ".env",
            environ={},
        )
        assert False, "Expected ConfigError"
    except ConfigError as exc:
        assert "listen_seconds" in str(exc)


def test_load_app_config_rejects_invalid_dotenv_line(tmp_path: Path) -> None:
    example_path = tmp_path / "settings.example.json"
    env_path = tmp_path / ".env"
    write_json(example_path, base_payload())
    env_path.write_text("NOT_VALID\n", encoding="utf-8")

    try:
        load_app_config(
            example_path=example_path,
            local_path=tmp_path / "missing.local.json",
            env_path=env_path,
            environ={},
        )
        assert False, "Expected ConfigError"
    except ConfigError as exc:
        assert ".env" in str(exc)


def test_load_open_app_settings_returns_validated_mapping(tmp_path: Path) -> None:
    example_path = tmp_path / "settings.example.json"
    write_json(example_path, base_payload())

    settings = load_open_app_settings(
        example_path=example_path,
        local_path=tmp_path / "missing.local.json",
        env_path=tmp_path / ".env",
        environ={},
    )

    assert settings["enabled"] is True
    assert settings["aliases"] == {"calculator": "calc.exe"}


def test_load_stt_settings_returns_validated_mapping(tmp_path: Path) -> None:
    example_path = tmp_path / "settings.example.json"
    write_json(example_path, base_payload())

    settings = load_stt_settings(
        example_path=example_path,
        local_path=tmp_path / "missing.local.json",
        env_path=tmp_path / ".env",
        environ={},
    )

    assert settings["engine"] == "vosk"
    assert settings["model_path"] == "models/vosk/model"

"""Centralized config loading and validation for Bob."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


ROOT_DIR = Path(__file__).resolve().parents[3]
DEFAULT_EXAMPLE_PATH = ROOT_DIR / "config" / "settings.example.json"
DEFAULT_LOCAL_PATH = ROOT_DIR / "config" / "settings.local.json"
DEFAULT_ENV_PATH = ROOT_DIR / ".env"
SUPPORTED_SECRET_KEYS = (
    "OPENAI_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "ELEVENLABS_API_KEY",
)


class ConfigError(RuntimeError):
    """Raised when configuration cannot be loaded or validated."""


@dataclass(frozen=True)
class ProjectConfig:
    name: str
    environment: str
    log_level: str


@dataclass(frozen=True)
class AssistantConfig:
    name: str
    wake_phrase: str
    deterministic_reply: str
    start_muted: bool


@dataclass(frozen=True)
class TimeoutConfig:
    listen_seconds: int
    response_start_seconds: int
    network_fallback_seconds: int


@dataclass(frozen=True)
class AudioConfig:
    input_device: str
    output_device: str
    sample_rate_hz: int


@dataclass(frozen=True)
class OpenAppConfig:
    enabled: bool
    aliases: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ActionConfig:
    open_app: OpenAppConfig


@dataclass(frozen=True)
class SttConfig:
    engine: str
    model_path: str
    language: str
    fallback_engine: str | None = None
    sample_rate_hz: int = 16000


@dataclass(frozen=True)
class TtsConfig:
    engine: str
    speech_rate: int
    voice_id: str | None = None


@dataclass(frozen=True)
class SecretConfig:
    values: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class AppConfig:
    project: ProjectConfig
    assistant: AssistantConfig
    timeouts: TimeoutConfig
    audio: AudioConfig
    actions: ActionConfig
    stt: SttConfig
    tts: TtsConfig
    secrets: SecretConfig


def load_app_config(
    *,
    example_path: Path | str | None = None,
    local_path: Path | str | None = None,
    env_path: Path | str | None = None,
    environ: Mapping[str, str] | None = None,
) -> AppConfig:
    """Load config from example defaults, local overrides, and env secrets."""
    example_file = Path(example_path) if example_path is not None else DEFAULT_EXAMPLE_PATH
    local_file = Path(local_path) if local_path is not None else DEFAULT_LOCAL_PATH
    env_file = Path(env_path) if env_path is not None else DEFAULT_ENV_PATH

    if not example_file.exists():
        raise ConfigError(f"Missing config template: '{example_file}'")

    merged = _load_json_mapping(example_file)
    if local_file.exists():
        merged = _deep_merge(merged, _load_json_mapping(local_file))

    secrets = _load_secret_values(env_file=env_file, environ=environ)
    return _build_app_config(merged, secrets)


def load_open_app_settings(
    *,
    example_path: Path | str | None = None,
    local_path: Path | str | None = None,
    env_path: Path | str | None = None,
    environ: Mapping[str, str] | None = None,
) -> dict[str, object]:
    """Return validated open-app settings in mapping form for existing action builder."""
    config = load_app_config(
        example_path=example_path,
        local_path=local_path,
        env_path=env_path,
        environ=environ,
    )
    return {
        "enabled": config.actions.open_app.enabled,
        "aliases": dict(config.actions.open_app.aliases),
    }


def load_stt_settings(
    *,
    example_path: Path | str | None = None,
    local_path: Path | str | None = None,
    env_path: Path | str | None = None,
    environ: Mapping[str, str] | None = None,
) -> dict[str, object]:
    """Return validated STT settings in mapping form for existing STT builder."""
    config = load_app_config(
        example_path=example_path,
        local_path=local_path,
        env_path=env_path,
        environ=environ,
    )
    return {
        "engine": config.stt.engine,
        "model_path": config.stt.model_path,
        "language": config.stt.language,
        "sample_rate_hz": config.stt.sample_rate_hz,
    }


def _load_json_mapping(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Invalid JSON in '{path}': {exc}") from exc
    if not isinstance(payload, dict):
        raise ConfigError(f"Expected top-level object in '{path}'.")
    return payload


def _deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = dict(base)
    for key, value in override.items():
        if (
            key in merged
            and isinstance(merged[key], Mapping)
            and isinstance(value, Mapping)
        ):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _load_secret_values(
    *,
    env_file: Path,
    environ: Mapping[str, str] | None,
) -> dict[str, str]:
    values: dict[str, str] = {}
    if env_file.exists():
        values.update(_parse_dotenv(env_file))

    merged_environ = os.environ if environ is None else environ
    for key in SUPPORTED_SECRET_KEYS:
        value = merged_environ.get(key)
        if value:
            values[key] = value
    return values


def _parse_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ConfigError(f"Invalid .env line in '{path}': '{raw_line}'")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ConfigError(f"Invalid .env key in '{path}': '{raw_line}'")
        values[key] = value
    return values


def _build_app_config(payload: Mapping[str, Any], secrets: Mapping[str, str]) -> AppConfig:
    project = _require_mapping(payload, "project")
    assistant = _require_mapping(payload, "assistant")
    timeouts = _require_mapping(payload, "timeouts")
    audio = _require_mapping(payload, "audio")
    actions = _require_mapping(payload, "actions")
    open_app = _require_mapping(actions, "open_app")
    stt = _require_mapping(payload, "stt")
    tts = _require_mapping(payload, "tts")

    aliases_value = _require_mapping(open_app, "aliases")
    aliases: dict[str, str] = {}
    for key, value in aliases_value.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ConfigError("actions.open_app.aliases must be string-to-string.")
        aliases[key.lower().strip()] = value.strip()

    config = AppConfig(
        project=ProjectConfig(
            name=_require_str(project, "name"),
            environment=_require_str(project, "environment"),
            log_level=_require_str(project, "log_level"),
        ),
        assistant=AssistantConfig(
            name=_require_str(assistant, "name"),
            wake_phrase=_require_str(assistant, "wake_phrase"),
            deterministic_reply=_require_str(assistant, "deterministic_reply"),
            start_muted=_require_bool(assistant, "start_muted"),
        ),
        timeouts=TimeoutConfig(
            listen_seconds=_require_positive_int(timeouts, "listen_seconds"),
            response_start_seconds=_require_positive_int(timeouts, "response_start_seconds"),
            network_fallback_seconds=_require_positive_int(timeouts, "network_fallback_seconds"),
        ),
        audio=AudioConfig(
            input_device=_require_str(audio, "input_device"),
            output_device=_require_str(audio, "output_device"),
            sample_rate_hz=_require_positive_int(audio, "sample_rate_hz"),
        ),
        actions=ActionConfig(
            open_app=OpenAppConfig(
                enabled=_require_bool(open_app, "enabled"),
                aliases=aliases,
            )
        ),
        stt=SttConfig(
            engine=_require_str(stt, "engine"),
            model_path=_require_str(stt, "model_path"),
            language=_require_str(stt, "language"),
            fallback_engine=_optional_str(stt, "fallback_engine"),
            sample_rate_hz=_optional_positive_int(stt, "sample_rate_hz", default=16000),
        ),
        tts=TtsConfig(
            engine=_require_str(tts, "engine"),
            speech_rate=_require_positive_int(tts, "speech_rate"),
            voice_id=_optional_str(tts, "voice_id"),
        ),
        secrets=SecretConfig(values=dict(secrets)),
    )
    return config


def _require_mapping(mapping: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise ConfigError(f"Missing or invalid object for '{key}'.")
    return value


def _require_str(mapping: Mapping[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"Missing or invalid string for '{key}'.")
    return value.strip()


def _optional_str(mapping: Mapping[str, Any], key: str) -> str | None:
    value = mapping.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ConfigError(f"Expected string or null for '{key}'.")
    stripped = value.strip()
    return stripped or None


def _require_bool(mapping: Mapping[str, Any], key: str) -> bool:
    value = mapping.get(key)
    if not isinstance(value, bool):
        raise ConfigError(f"Missing or invalid boolean for '{key}'.")
    return value


def _require_positive_int(mapping: Mapping[str, Any], key: str) -> int:
    value = mapping.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ConfigError(f"Missing or invalid positive integer for '{key}'.")
    return value


def _optional_positive_int(mapping: Mapping[str, Any], key: str, *, default: int) -> int:
    value = mapping.get(key, default)
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ConfigError(f"Missing or invalid positive integer for '{key}'.")
    return value

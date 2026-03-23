"""pyttsx3-backed text-to-speech implementation."""

from __future__ import annotations

from typing import Any, Callable

from bob.tts.service import TTSConfig, TextToSpeechError


class Pyttsx3SpeechSynthesizer:
    """Synchronous `pyttsx3` speech adapter for deterministic responses."""

    def __init__(
        self,
        config: TTSConfig | None = None,
        engine_factory: Callable[[], Any] | None = None,
    ) -> None:
        self._config = config or TTSConfig()
        self._engine = self._build_engine(engine_factory)
        self._apply_config()

    def speak(self, text: str) -> None:
        try:
            self._engine.say(text)
            self._engine.runAndWait()
        except Exception as exc:  # pragma: no cover - depends on local engine/runtime
            raise TextToSpeechError(f"Failed to speak text: {exc}") from exc

    def _build_engine(self, engine_factory: Callable[[], Any] | None) -> Any:
        if engine_factory is not None:
            try:
                return engine_factory()
            except Exception as exc:
                raise TextToSpeechError(
                    f"Failed to initialize pyttsx3 engine: {exc}"
                ) from exc

        try:
            import pyttsx3
        except ImportError as exc:
            raise TextToSpeechError(
                "pyttsx3 is not installed. Install it before using speech output."
            ) from exc

        try:
            return pyttsx3.init()
        except Exception as exc:  # pragma: no cover - depends on local engine/runtime
            raise TextToSpeechError(
                f"Failed to initialize pyttsx3 engine: {exc}"
            ) from exc

    def _apply_config(self) -> None:
        try:
            self._engine.setProperty("rate", self._config.speech_rate)
            if self._config.voice_id is not None:
                self._engine.setProperty("voice", self._config.voice_id)
        except Exception as exc:  # pragma: no cover - depends on local engine/runtime
            raise TextToSpeechError(f"Failed to configure pyttsx3 engine: {exc}") from exc

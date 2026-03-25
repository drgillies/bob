"""pyttsx3-backed text-to-speech implementation."""

from __future__ import annotations

import re
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
            prepared = self._prepare_text(text)
            self._engine.say(prepared)
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
            self._engine.setProperty("volume", self._config.volume)
            if self._config.voice_id is not None:
                self._engine.setProperty("voice", self._config.voice_id)
            elif self._config.preferred_gender is not None:
                selected_voice_id = self._select_voice_id_by_gender(
                    self._config.preferred_gender
                )
                if selected_voice_id is not None:
                    self._engine.setProperty("voice", selected_voice_id)
        except Exception as exc:  # pragma: no cover - depends on local engine/runtime
            raise TextToSpeechError(f"Failed to configure pyttsx3 engine: {exc}") from exc

    def _prepare_text(self, text: str) -> str:
        if self._config.sentence_pause_ms <= 0:
            return text
        pause_marker = " " + ("." * max(1, self._config.sentence_pause_ms // 100))
        return re.sub(r"([.!?])\s+", rf"\1{pause_marker} ", text)

    def _select_voice_id_by_gender(self, preferred_gender: str) -> str | None:
        try:
            voices = self._engine.getProperty("voices")
        except Exception:
            return None

        if not voices:
            return None

        for voice in voices:
            detected_gender = self._detect_voice_gender(voice)
            if detected_gender == preferred_gender:
                voice_id = getattr(voice, "id", None)
                if isinstance(voice_id, str) and voice_id.strip():
                    return voice_id.strip()
        return None

    @staticmethod
    def _detect_voice_gender(voice: Any) -> str | None:
        candidates: list[str] = []

        for attr in ("gender", "name", "id"):
            value = getattr(voice, attr, None)
            if isinstance(value, str):
                candidates.append(value.lower())
            elif isinstance(value, bytes):
                candidates.append(value.decode(errors="ignore").lower())

        languages = getattr(voice, "languages", None)
        if isinstance(languages, list):
            for value in languages:
                if isinstance(value, bytes):
                    candidates.append(value.decode(errors="ignore").lower())
                elif isinstance(value, str):
                    candidates.append(value.lower())

        haystack = " ".join(candidates)
        if re.search(r"\bfemale\b", haystack):
            return "female"
        if re.search(r"\bmale\b", haystack):
            return "male"
        return None

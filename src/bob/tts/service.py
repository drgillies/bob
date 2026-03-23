"""Text-to-speech interfaces and shared types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class TextToSpeechError(RuntimeError):
    """Raised when a text-to-speech operation fails."""


@dataclass(frozen=True)
class TTSConfig:
    """Runtime configuration for text-to-speech."""

    speech_rate: int = 150
    voice_id: str | None = None


class SpeechSynthesizer(Protocol):
    """Minimal interface for synchronous speech output."""

    def speak(self, text: str) -> None:
        """Speak text to the configured output device."""

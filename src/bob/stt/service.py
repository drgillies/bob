"""Speech-to-text contracts, results, and default adapter support."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Protocol


class UtteranceStopReason(str, Enum):
    """Reason an utterance recording session ended."""

    END_OF_SPEECH = "END_OF_SPEECH"
    TIMEOUT = "TIMEOUT"


@dataclass(frozen=True)
class RecordedUtterance:
    """PCM utterance data and capture metadata for downstream STT."""

    audio_bytes: bytes
    sample_rate_hz: int
    channels: int
    sample_width_bytes: int
    frame_count: int
    speech_started: bool
    stop_reason: UtteranceStopReason
    speech_frame_count: int = 0

    @property
    def duration_seconds(self) -> float:
        """Return utterance duration derived from raw PCM length."""
        bytes_per_frame = self.channels * self.sample_width_bytes
        if bytes_per_frame == 0:
            return 0.0
        sample_count = len(self.audio_bytes) / bytes_per_frame
        return sample_count / self.sample_rate_hz


class SpeechToTextError(RuntimeError):
    """Base STT failure."""


class SpeechToTextConfigurationError(SpeechToTextError):
    """Raised when the STT engine is misconfigured or cannot be loaded."""


class SpeechToTextTranscriptionError(SpeechToTextError):
    """Raised when transcription fails after the engine was initialized."""


@dataclass(frozen=True)
class TranscriptionResult:
    """Transcribed text and minimal metadata for routing."""

    text: str
    confidence: float | None = None
    language: str | None = None
    engine: str = "unknown"
    utterance_duration_seconds: float = 0.0
    audio_duration_seconds: float = 0.0
    is_final: bool = True


class SpeechToTextService(Protocol):
    """Transcribe one utterance into text plus metadata."""

    def transcribe(self, utterance: RecordedUtterance) -> TranscriptionResult:
        """Return a transcription result for the supplied utterance."""


@dataclass(frozen=True)
class VoskSpeechToTextConfig:
    """Settings for the default Vosk-based STT adapter."""

    model_path: str
    language: str = "en"
    sample_rate_hz: int = 16000
    accept_waveform_chunk_bytes: int = 4000


class VoskSpeechToTextService:
    """Speech-to-text service backed by a Vosk recognizer."""

    def __init__(
        self,
        config: VoskSpeechToTextConfig,
        *,
        model_factory: Any | None = None,
        recognizer_factory: Any | None = None,
    ) -> None:
        self._config = config
        self._model_factory = model_factory
        self._recognizer_factory = recognizer_factory
        self._model: Any | None = None

    def transcribe(self, utterance: RecordedUtterance) -> TranscriptionResult:
        """Transcribe an utterance using Vosk's final-result API."""
        if not utterance.audio_bytes or not utterance.speech_started:
            return TranscriptionResult(
                text="",
                confidence=None,
                language=self._config.language,
                engine="vosk",
                utterance_duration_seconds=utterance.duration_seconds,
                audio_duration_seconds=utterance.duration_seconds,
                is_final=True,
            )

        recognizer = self._build_recognizer()
        try:
            chunk_size = max(1, self._config.accept_waveform_chunk_bytes)
            for offset in range(0, len(utterance.audio_bytes), chunk_size):
                recognizer.AcceptWaveform(
                    utterance.audio_bytes[offset : offset + chunk_size]
                )
            raw_result = recognizer.FinalResult()
        except Exception as exc:
            raise SpeechToTextTranscriptionError(
                f"Vosk transcription failed: {exc}"
            ) from exc

        parsed = self._parse_result(raw_result)
        return TranscriptionResult(
            text=parsed["text"],
            confidence=parsed["confidence"],
            language=self._config.language,
            engine="vosk",
            utterance_duration_seconds=utterance.duration_seconds,
            audio_duration_seconds=utterance.duration_seconds,
            is_final=True,
        )

    def _build_recognizer(self) -> Any:
        model = self._get_model()
        recognizer_factory = self._recognizer_factory
        if recognizer_factory is None:
            try:
                from vosk import KaldiRecognizer
            except ImportError as exc:
                raise SpeechToTextConfigurationError(
                    "vosk is not installed. Install dependencies before using STT."
                ) from exc
            recognizer_factory = KaldiRecognizer

        try:
            return recognizer_factory(model, self._config.sample_rate_hz)
        except Exception as exc:
            raise SpeechToTextConfigurationError(
                f"Failed to create Vosk recognizer: {exc}"
            ) from exc

    def _get_model(self) -> Any:
        if self._model is not None:
            return self._model

        model_factory = self._model_factory
        if model_factory is None:
            try:
                from vosk import Model
            except ImportError as exc:
                raise SpeechToTextConfigurationError(
                    "vosk is not installed. Install dependencies before using STT."
                ) from exc
            model_factory = Model

        try:
            self._model = model_factory(self._config.model_path)
        except Exception as exc:
            raise SpeechToTextConfigurationError(
                f"Failed to load Vosk model from '{self._config.model_path}': {exc}"
            ) from exc
        return self._model

    @staticmethod
    def _parse_result(raw_result: str) -> dict[str, Any]:
        try:
            payload = json.loads(raw_result or "{}")
        except json.JSONDecodeError as exc:
            raise SpeechToTextTranscriptionError(
                f"Vosk returned invalid JSON: {exc}"
            ) from exc

        alternatives = payload.get("alternatives")
        if isinstance(alternatives, list) and alternatives:
            best = alternatives[0] or {}
            return {
                "text": str(best.get("text", "")).strip(),
                "confidence": (
                    float(best["confidence"])
                    if "confidence" in best and best["confidence"] is not None
                    else None
                ),
            }

        return {
            "text": str(payload.get("text", "")).strip(),
            "confidence": None,
        }


def build_speech_to_text_service(
    settings: Mapping[str, object] | None = None,
) -> SpeechToTextService:
    """Build the configured speech-to-text service."""
    config = settings or {}
    engine = str(config.get("engine", "vosk")).strip().lower()

    if engine != "vosk":
        raise SpeechToTextConfigurationError(
            f"Unsupported STT engine '{engine}'. Expected 'vosk'."
        )

    model_path = str(config.get("model_path", "")).strip()
    if not model_path:
        raise SpeechToTextConfigurationError(
            "STT model_path is required for the Vosk engine."
        )

    language = str(config.get("language", "en")).strip() or "en"
    sample_rate_hz = int(config.get("sample_rate_hz", 16000))
    return VoskSpeechToTextService(
        VoskSpeechToTextConfig(
            model_path=model_path,
            language=language,
            sample_rate_hz=sample_rate_hz,
        )
    )

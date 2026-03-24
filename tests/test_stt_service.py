"""Tests for speech-to-text contracts and the Vosk adapter seam."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.stt import (
    build_speech_to_text_service,
    RecordedUtterance,
    SpeechToTextConfigurationError,
    SpeechToTextTranscriptionError,
    TranscriptionResult,
    UtteranceStopReason,
    VoskSpeechToTextConfig,
    VoskSpeechToTextService,
)


def build_utterance(audio_bytes: bytes = b"\x01\x00" * 8) -> RecordedUtterance:
    return RecordedUtterance(
        audio_bytes=audio_bytes,
        sample_rate_hz=16000,
        channels=1,
        sample_width_bytes=2,
        frame_count=1,
        speech_started=bool(audio_bytes),
        stop_reason=UtteranceStopReason.END_OF_SPEECH,
        speech_frame_count=1 if audio_bytes else 0,
    )


class FakeRecognizer:
    def __init__(self, final_result: str, *, fail_accept: bool = False) -> None:
        self.final_result = final_result
        self.fail_accept = fail_accept
        self.chunks: list[bytes] = []

    def AcceptWaveform(self, chunk: bytes) -> bool:
        self.chunks.append(chunk)
        if self.fail_accept:
            raise RuntimeError("waveform failure")
        return True

    def FinalResult(self) -> str:
        return self.final_result


def test_transcription_result_defaults_are_stable() -> None:
    result = TranscriptionResult(text="hello")

    assert result.text == "hello"
    assert result.confidence is None
    assert result.engine == "unknown"
    assert result.is_final is True


def test_vosk_service_returns_empty_result_for_empty_utterance() -> None:
    service = VoskSpeechToTextService(
        VoskSpeechToTextConfig(model_path="fake-model"),
        model_factory=lambda path: object(),
        recognizer_factory=lambda model, sample_rate: None,
    )

    result = service.transcribe(build_utterance(audio_bytes=b""))

    assert result.text == ""
    assert result.engine == "vosk"
    assert result.confidence is None


def test_vosk_service_transcribes_and_parses_alternative_confidence() -> None:
    recognizer = FakeRecognizer(
        json.dumps(
            {
                "alternatives": [
                    {
                        "text": "turn on the light",
                        "confidence": 0.87,
                    }
                ]
            }
        )
    )
    service = VoskSpeechToTextService(
        VoskSpeechToTextConfig(
            model_path="fake-model",
            language="en",
            sample_rate_hz=16000,
            accept_waveform_chunk_bytes=4,
        ),
        model_factory=lambda path: {"path": path},
        recognizer_factory=lambda model, sample_rate: recognizer,
    )

    result = service.transcribe(build_utterance(audio_bytes=b"\x01\x00" * 10))

    assert result.text == "turn on the light"
    assert result.confidence == 0.87
    assert result.engine == "vosk"
    assert len(recognizer.chunks) == 5


def test_vosk_service_wraps_model_load_failure() -> None:
    service = VoskSpeechToTextService(
        VoskSpeechToTextConfig(model_path="missing-model"),
        model_factory=lambda path: (_ for _ in ()).throw(RuntimeError("bad model")),
    )

    try:
        service.transcribe(build_utterance())
        assert False, "Expected SpeechToTextConfigurationError"
    except SpeechToTextConfigurationError as exc:
        assert "missing-model" in str(exc)


def test_vosk_service_wraps_transcription_failure() -> None:
    recognizer = FakeRecognizer("{}", fail_accept=True)
    service = VoskSpeechToTextService(
        VoskSpeechToTextConfig(model_path="fake-model"),
        model_factory=lambda path: object(),
        recognizer_factory=lambda model, sample_rate: recognizer,
    )

    try:
        service.transcribe(build_utterance())
        assert False, "Expected SpeechToTextTranscriptionError"
    except SpeechToTextTranscriptionError as exc:
        assert "Vosk transcription failed" in str(exc)


def test_vosk_service_rejects_invalid_json() -> None:
    service = VoskSpeechToTextService(
        VoskSpeechToTextConfig(model_path="fake-model"),
        model_factory=lambda path: object(),
        recognizer_factory=lambda model, sample_rate: FakeRecognizer("{not-json"),
    )

    try:
        service.transcribe(build_utterance())
        assert False, "Expected SpeechToTextTranscriptionError"
    except SpeechToTextTranscriptionError as exc:
        assert "invalid JSON" in str(exc)


def test_build_speech_to_text_service_uses_vosk_defaults() -> None:
    service = build_speech_to_text_service(
        {
            "engine": "vosk",
            "model_path": "models/vosk-small",
            "language": "en",
            "sample_rate_hz": 16000,
        }
    )

    assert isinstance(service, VoskSpeechToTextService)


def test_build_speech_to_text_service_rejects_missing_model_path() -> None:
    try:
        build_speech_to_text_service({"engine": "vosk"})
        assert False, "Expected SpeechToTextConfigurationError"
    except SpeechToTextConfigurationError as exc:
        assert "model_path" in str(exc)


def test_build_speech_to_text_service_rejects_unsupported_engine() -> None:
    try:
        build_speech_to_text_service(
            {
                "engine": "not-real",
                "model_path": "models/example",
            }
        )
        assert False, "Expected SpeechToTextConfigurationError"
    except SpeechToTextConfigurationError as exc:
        assert "Unsupported STT engine" in str(exc)

"""Tests for transcription-to-intent orchestration."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.data.model import IntentName
from bob.orchestrator import IntentResponseController
from bob.skills import CoreIntentHandler, IntentRouter
from bob.stt import TranscriptionResult


class FakeTranscriptionController:
    def __init__(self, text: str | None) -> None:
        self._text = text

    def process_once(self):
        if self._text is None:
            return None

        class FakeDetection:
            keyword = "hey bob"

        class FakeWakeEvent:
            detection = FakeDetection()

        class FakeEvent:
            wake_event = FakeWakeEvent()
            transcription = TranscriptionResult(
                text=self._text,
                confidence=0.9,
                language="en",
                engine="fake-stt",
                utterance_duration_seconds=0.5,
                audio_duration_seconds=0.5,
            )

        return FakeEvent()


def test_intent_flow_routes_time_request_to_response() -> None:
    controller = IntentResponseController(
        transcription_controller=FakeTranscriptionController("what time is it"),
        router=IntentRouter(),
        handler=CoreIntentHandler(),
    )

    result = controller.process_once()

    assert result is not None
    assert result.intent_match.name == IntentName.GET_TIME
    assert result.response.intent == IntentName.GET_TIME
    assert "time is" in result.response.text.lower()


def test_intent_flow_returns_unknown_fallback_for_unmatched_text() -> None:
    controller = IntentResponseController(
        transcription_controller=FakeTranscriptionController("tell me a joke"),
        router=IntentRouter(),
        handler=CoreIntentHandler(),
    )

    result = controller.process_once()

    assert result is not None
    assert result.intent_match.name == IntentName.UNKNOWN
    assert result.response.handled is False


def test_intent_flow_returns_none_when_transcription_missing() -> None:
    controller = IntentResponseController(
        transcription_controller=FakeTranscriptionController(None),
        router=IntentRouter(),
        handler=CoreIntentHandler(),
    )

    assert controller.process_once() is None

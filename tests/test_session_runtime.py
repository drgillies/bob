"""Tests for session memory and resilient assistant runtime."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.data.model import ErrorComponent, IntentMatch, IntentName, IntentResponse
from bob.orchestrator import SessionAwareAssistantController, SessionMemoryConfig, SessionMemoryStore
from bob.orchestrator.intent_flow import RoutedTranscription
from bob.skills.actions import LocalActionError
from bob.stt import SpeechToTextTranscriptionError, TranscriptionResult
from bob.tts import TextToSpeechError


class FakeIdleLoop:
    def __init__(self) -> None:
        self.acknowledge_calls = 0

    def acknowledge_trigger(self) -> None:
        self.acknowledge_calls += 1


class FakeSynthesizer:
    def __init__(self, *, fail: Exception | None = None) -> None:
        self.fail = fail
        self.spoken: list[str] = []

    def speak(self, text: str) -> None:
        self.spoken.append(text)
        if self.fail is not None:
            raise self.fail


class FakeIntentController:
    def __init__(self, result: RoutedTranscription | None = None, fail: Exception | None = None) -> None:
        self._result = result
        self._fail = fail

    def process_once(self) -> RoutedTranscription | None:
        if self._fail is not None:
            raise self._fail
        return self._result


def build_routed_transcription(
    *,
    user_text: str = "what time is it",
    intent: IntentName = IntentName.GET_TIME,
    response_text: str = "The time is 8:00 PM.",
    handled: bool = True,
) -> RoutedTranscription:
    class FakeDetection:
        keyword = "hey bob"

    class FakeWakeEvent:
        detection = FakeDetection()

    class FakeTranscriptionEvent:
        wake_event = FakeWakeEvent()
        transcription = TranscriptionResult(
            text=user_text,
            confidence=0.9,
            language="en",
            engine="fake-stt",
            utterance_duration_seconds=0.6,
            audio_duration_seconds=0.6,
        )

    return RoutedTranscription(
        transcription_event=FakeTranscriptionEvent(),
        intent_match=IntentMatch(
            name=intent,
            confidence=1.0,
            matched_phrase=user_text,
        ),
        response=IntentResponse(
            intent=intent,
            text=response_text,
            handled=handled,
        ),
    )


def test_session_memory_tracks_recent_turns_and_clears() -> None:
    memory = SessionMemoryStore(SessionMemoryConfig(max_turns=2, max_errors=2))
    memory.record_turn(build_routed_transcription(user_text="first", response_text="one"))
    memory.record_turn(build_routed_transcription(user_text="second", response_text="two"))
    memory.record_turn(build_routed_transcription(user_text="third", response_text="three"))

    snapshot = memory.snapshot()
    assert snapshot.last_user_text == "third"
    assert snapshot.last_response == "three"
    assert snapshot.recent_user_texts == ("second", "third")
    assert len(snapshot.turns) == 2

    memory.clear()
    cleared = memory.snapshot()
    assert cleared.turns == ()
    assert cleared.errors == ()
    assert cleared.last_intent is None


def test_session_aware_controller_records_turn_and_speaks() -> None:
    memory = SessionMemoryStore()
    synthesizer = FakeSynthesizer()
    controller = SessionAwareAssistantController(
        intent_controller=FakeIntentController(build_routed_transcription()),
        synthesizer=synthesizer,
        session_memory=memory,
        idle_loop=FakeIdleLoop(),
    )

    result = controller.process_once()

    assert result is not None
    assert result.routed is not None
    assert result.recovered_error is None
    assert synthesizer.spoken == ["The time is 8:00 PM."]
    assert memory.snapshot().recent_user_texts == ("what time is it",)


def test_session_aware_controller_recovers_from_stt_error() -> None:
    idle_loop = FakeIdleLoop()
    memory = SessionMemoryStore()
    controller = SessionAwareAssistantController(
        intent_controller=FakeIntentController(
            fail=SpeechToTextTranscriptionError("stt boom")
        ),
        synthesizer=FakeSynthesizer(),
        session_memory=memory,
        idle_loop=idle_loop,
    )

    result = controller.process_once()

    assert result is not None
    assert result.routed is None
    assert result.recovered_error is not None
    assert result.recovered_error.component == ErrorComponent.STT
    assert idle_loop.acknowledge_calls == 1
    assert memory.snapshot().errors[-1].message == "stt boom"


def test_session_aware_controller_recovers_from_tts_error() -> None:
    idle_loop = FakeIdleLoop()
    memory = SessionMemoryStore()
    controller = SessionAwareAssistantController(
        intent_controller=FakeIntentController(build_routed_transcription()),
        synthesizer=FakeSynthesizer(fail=TextToSpeechError("tts boom")),
        session_memory=memory,
        idle_loop=idle_loop,
    )

    result = controller.process_once()

    assert result is not None
    assert result.recovered_error is not None
    assert result.recovered_error.component == ErrorComponent.TTS
    assert idle_loop.acknowledge_calls == 1
    assert memory.snapshot().last_user_text == "what time is it"


def test_session_aware_controller_classifies_action_errors() -> None:
    idle_loop = FakeIdleLoop()
    memory = SessionMemoryStore()
    controller = SessionAwareAssistantController(
        intent_controller=FakeIntentController(fail=LocalActionError("action boom")),
        synthesizer=FakeSynthesizer(),
        session_memory=memory,
        idle_loop=idle_loop,
    )

    result = controller.process_once()

    assert result is not None
    assert result.recovered_error is not None
    assert result.recovered_error.component == ErrorComponent.ACTION

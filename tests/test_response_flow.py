"""Tests for deterministic wake-response flow."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.orchestrator import (
    DeterministicResponseConfig,
    DeterministicResponseController,
    IdleLoopOrchestrator,
    ResponseState,
)
from bob.tts import TextToSpeechError
from bob.wakeword import WakeDetectionEvent


class FakeAudioSource:
    def __init__(self, frames: list[bytes] | None = None) -> None:
        self.frames = list(frames or [])
        self.started = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.started = False

    def is_running(self) -> bool:
        return self.started

    def read_frame(self, timeout_seconds: float | None = None) -> bytes | None:  # noqa: ARG002
        if not self.frames:
            return None
        return self.frames.pop(0)


class FakeDetector:
    def __init__(self, detections: list[WakeDetectionEvent | None]) -> None:
        self._detections = list(detections)
        self.reset_calls = 0

    def process_frame(self, frame: bytes) -> WakeDetectionEvent | None:
        del frame
        if not self._detections:
            return None
        return self._detections.pop(0)

    def reset(self) -> None:
        self.reset_calls += 1


class FakeClock:
    def __init__(self, times: list[float]) -> None:
        self._times = list(times)

    def __call__(self) -> float:
        if not self._times:
            raise AssertionError("No more fake times available")
        return self._times.pop(0)


class FakeSynthesizer:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.spoken: list[str] = []

    def speak(self, text: str) -> None:
        self.spoken.append(text)
        if self.fail:
            raise TextToSpeechError("tts failed")


def _build_idle_loop() -> IdleLoopOrchestrator:
    return IdleLoopOrchestrator(
        audio_source=FakeAudioSource([b"frame-1"]),
        detector=FakeDetector([WakeDetectionEvent(keyword="hey bob", score=0.9)]),
        time_fn=FakeClock([10.0]),
    )


def test_response_controller_speaks_and_returns_to_idle() -> None:
    states: list[ResponseState] = []
    synthesizer = FakeSynthesizer()
    controller = DeterministicResponseController(
        idle_loop=_build_idle_loop(),
        synthesizer=synthesizer,
        config=DeterministicResponseConfig(reply_text="Hello, I'm here."),
        state_callback=states.append,
    )

    controller._idle_loop.start()
    detection = controller.process_once()

    assert detection == WakeDetectionEvent(keyword="hey bob", score=0.9)
    assert synthesizer.spoken == ["Hello, I'm here."]
    assert controller._idle_loop.state.value == "IDLE"
    assert states == [
        ResponseState.TRIGGERED,
        ResponseState.SPEAKING,
        ResponseState.IDLE,
    ]


def test_response_controller_returns_to_idle_when_tts_fails() -> None:
    synthesizer = FakeSynthesizer(fail=True)
    controller = DeterministicResponseController(
        idle_loop=_build_idle_loop(),
        synthesizer=synthesizer,
    )

    controller._idle_loop.start()
    try:
        controller.process_once()
        assert False, "Expected TextToSpeechError"
    except TextToSpeechError:
        pass

    assert controller._idle_loop.state.value == "IDLE"

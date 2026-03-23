"""Tests for mute-aware assistant response flow."""

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
    MuteAwareResponseController,
    MuteState,
)
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
    def __init__(self) -> None:
        self.spoken: list[str] = []

    def speak(self, text: str) -> None:
        self.spoken.append(text)


def _build_response_controller() -> DeterministicResponseController:
    idle_loop = IdleLoopOrchestrator(
        audio_source=FakeAudioSource([b"frame-1"]),
        detector=FakeDetector([WakeDetectionEvent(keyword="hey bob", score=1.0)]),
        time_fn=FakeClock([10.0]),
    )
    idle_loop.start()
    return DeterministicResponseController(
        idle_loop=idle_loop,
        synthesizer=FakeSynthesizer(),
        config=DeterministicResponseConfig(reply_text="Hello, I'm here."),
    )


def test_mute_aware_controller_blocks_response_when_muted() -> None:
    controller = MuteAwareResponseController(_build_response_controller())
    controller.set_muted(True)

    detection = controller.process_once()

    assert detection is None


def test_mute_aware_controller_processes_response_when_unmuted() -> None:
    controller = MuteAwareResponseController(_build_response_controller())

    detection = controller.process_once()

    assert detection == WakeDetectionEvent(keyword="hey bob", score=1.0)


def test_mute_state_callback_receives_updates() -> None:
    states: list[MuteState] = []
    controller = MuteAwareResponseController(
        _build_response_controller(),
        mute_state_callback=states.append,
    )

    controller.set_muted(True)
    controller.set_muted(False)

    assert states == [MuteState.MUTED, MuteState.UNMUTED]

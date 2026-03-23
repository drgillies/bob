"""Tests for wake-word idle-loop orchestration."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.orchestrator import AssistantState, IdleLoopConfig, IdleLoopOrchestrator
from bob.wakeword import WakeDetectionEvent


class FakeAudioSource:
    def __init__(self, frames: list[bytes] | None = None) -> None:
        self.frames = list(frames or [])
        self.started = False
        self.stopped = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True
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
        self.frames_seen: list[bytes] = []
        self.reset_calls = 0

    def process_frame(self, frame: bytes) -> WakeDetectionEvent | None:
        self.frames_seen.append(frame)
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


def test_idle_loop_start_emits_idle_state() -> None:
    audio_source = FakeAudioSource()
    detector = FakeDetector([])
    states: list[AssistantState] = []

    orchestrator = IdleLoopOrchestrator(
        audio_source=audio_source,
        detector=detector,
        state_callback=states.append,
    )

    orchestrator.start()

    assert audio_source.started is True
    assert states == [AssistantState.IDLE]
    assert orchestrator.state == AssistantState.IDLE


def test_poll_once_transitions_to_triggered_on_detection() -> None:
    audio_source = FakeAudioSource([b"frame-1"])
    detector = FakeDetector([WakeDetectionEvent(keyword="hey bob", score=0.9)])
    states: list[AssistantState] = []

    orchestrator = IdleLoopOrchestrator(
        audio_source=audio_source,
        detector=detector,
        state_callback=states.append,
        time_fn=FakeClock([10.0]),
    )

    orchestrator.start()
    detection = orchestrator.poll_once()

    assert detection == WakeDetectionEvent(keyword="hey bob", score=0.9)
    assert detector.frames_seen == [b"frame-1"]
    assert detector.reset_calls == 1
    assert orchestrator.state == AssistantState.TRIGGERED
    assert states == [AssistantState.IDLE, AssistantState.TRIGGERED]


def test_poll_once_debounces_repeated_wake_events() -> None:
    audio_source = FakeAudioSource([b"frame-1", b"frame-2"])
    detector = FakeDetector(
        [
            WakeDetectionEvent(keyword="hey bob", score=0.9),
            WakeDetectionEvent(keyword="hey bob", score=0.85),
        ]
    )
    states: list[AssistantState] = []

    orchestrator = IdleLoopOrchestrator(
        audio_source=audio_source,
        detector=detector,
        config=IdleLoopConfig(debounce_seconds=2.0),
        state_callback=states.append,
        time_fn=FakeClock([10.0, 11.0]),
    )

    orchestrator.start()
    first = orchestrator.poll_once()
    second = orchestrator.poll_once()

    assert first is not None
    assert second is None
    assert detector.reset_calls == 1
    assert orchestrator.state == AssistantState.TRIGGERED
    assert states == [AssistantState.IDLE, AssistantState.TRIGGERED]


def test_acknowledge_trigger_returns_to_idle() -> None:
    audio_source = FakeAudioSource([b"frame-1"])
    detector = FakeDetector([WakeDetectionEvent(keyword="hey bob")])
    states: list[AssistantState] = []

    orchestrator = IdleLoopOrchestrator(
        audio_source=audio_source,
        detector=detector,
        state_callback=states.append,
        time_fn=FakeClock([5.0]),
    )

    orchestrator.start()
    orchestrator.poll_once()
    orchestrator.acknowledge_trigger()

    assert orchestrator.state == AssistantState.IDLE
    assert states == [
        AssistantState.IDLE,
        AssistantState.TRIGGERED,
        AssistantState.IDLE,
    ]


def test_poll_once_returns_none_when_no_audio_frame_available() -> None:
    audio_source = FakeAudioSource([])
    detector = FakeDetector([])
    states: list[AssistantState] = []

    orchestrator = IdleLoopOrchestrator(
        audio_source=audio_source,
        detector=detector,
        state_callback=states.append,
    )

    orchestrator.start()
    detection = orchestrator.poll_once()

    assert detection is None
    assert detector.frames_seen == []
    assert states == [AssistantState.IDLE]

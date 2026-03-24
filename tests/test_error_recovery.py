"""Tests for idle-loop recovery behavior on transient runtime failures."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.data.model import ErrorComponent
from bob.orchestrator import AssistantState, IdleLoopOrchestrator


class FailingAudioSource:
    def __init__(self) -> None:
        self.started = False
        self.stop_calls = 0
        self.start_calls = 0

    def start(self) -> None:
        self.started = True
        self.start_calls += 1

    def stop(self) -> None:
        self.started = False
        self.stop_calls += 1

    def is_running(self) -> bool:
        return self.started

    def read_frame(self, timeout_seconds: float | None = None) -> bytes | None:
        del timeout_seconds
        raise RuntimeError("audio read failed")


class FailingDetector:
    def __init__(self) -> None:
        self.reset_calls = 0

    def process_frame(self, frame: bytes):
        del frame
        raise RuntimeError("wake detector failed")

    def reset(self) -> None:
        self.reset_calls += 1


class SingleFrameAudioSource:
    def __init__(self) -> None:
        self.started = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.started = False

    def is_running(self) -> bool:
        return self.started

    def read_frame(self, timeout_seconds: float | None = None) -> bytes | None:
        del timeout_seconds
        return b"frame"


def test_idle_loop_recovers_from_audio_read_error_and_restarts_stream() -> None:
    errors = []
    states: list[AssistantState] = []
    audio_source = FailingAudioSource()
    orchestrator = IdleLoopOrchestrator(
        audio_source=audio_source,
        detector=FailingDetector(),
        state_callback=states.append,
        error_callback=errors.append,
    )

    orchestrator.start()
    detection = orchestrator.poll_once()

    assert detection is None
    assert orchestrator.state == AssistantState.IDLE
    assert audio_source.stop_calls == 1
    assert audio_source.start_calls == 2
    assert errors[-1].component == ErrorComponent.AUDIO
    assert errors[-1].message == "audio read failed"
    assert states == [AssistantState.IDLE]


def test_idle_loop_recovers_from_wakeword_error_without_restarting_audio() -> None:
    errors = []
    states: list[AssistantState] = []
    detector = FailingDetector()
    audio_source = SingleFrameAudioSource()
    orchestrator = IdleLoopOrchestrator(
        audio_source=audio_source,
        detector=detector,
        state_callback=states.append,
        error_callback=errors.append,
    )

    orchestrator.start()
    detection = orchestrator.poll_once()

    assert detection is None
    assert orchestrator.state == AssistantState.IDLE
    assert detector.reset_calls == 1
    assert audio_source.is_running() is True
    assert errors[-1].component == ErrorComponent.WAKEWORD
    assert errors[-1].message == "wake detector failed"
    assert states == [AssistantState.IDLE]

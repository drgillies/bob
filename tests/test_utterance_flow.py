"""Tests for wake-triggered utterance recording flow."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.audio import (
    AudioCaptureConfig,
    EnergyVoiceActivityDetector,
    UtteranceRecorder,
    UtteranceRecorderConfig,
    VoiceActivityConfig,
)
from bob.orchestrator import (
    AssistantState,
    IdleLoopOrchestrator,
    WakeTriggeredUtteranceController,
)
from bob.stt import UtteranceStopReason
from bob.wakeword import WakeDetectionEvent


def pcm_frame(amplitude: int, sample_count: int = 8) -> bytes:
    return b"".join(
        int(amplitude).to_bytes(2, byteorder="little", signed=True)
        for _ in range(sample_count)
    )


class FakeClock:
    def __init__(self) -> None:
        self.current = 0.0

    def advance(self, seconds: float) -> None:
        self.current += seconds

    def __call__(self) -> float:
        return self.current


class SharedAudioSource:
    def __init__(self, frames: list[bytes | None], clock: FakeClock, step: float) -> None:
        self.frames = list(frames)
        self.clock = clock
        self.step = step
        self.started = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.started = False

    def is_running(self) -> bool:
        return self.started

    def read_frame(self, timeout_seconds: float | None = None) -> bytes | None:
        del timeout_seconds
        self.clock.advance(self.step)
        if not self.frames:
            return None
        return self.frames.pop(0)


class SingleWakeDetector:
    def __init__(self) -> None:
        self.reset_calls = 0

    def process_frame(self, frame: bytes) -> WakeDetectionEvent | None:
        del frame
        return WakeDetectionEvent(keyword="hey bob", score=0.95)

    def reset(self) -> None:
        self.reset_calls += 1


def test_wake_triggered_controller_captures_utterance_and_returns_idle() -> None:
    clock = FakeClock()
    capture_config = AudioCaptureConfig(frame_duration_ms=100)
    block_size = capture_config.block_size
    audio_source = SharedAudioSource(
        [
            pcm_frame(100, sample_count=block_size),
            pcm_frame(1000, sample_count=block_size),
            pcm_frame(950, sample_count=block_size),
            pcm_frame(0, sample_count=block_size),
            pcm_frame(0, sample_count=block_size),
        ],
        clock=clock,
        step=0.1,
    )
    states: list[AssistantState] = []
    idle_loop = IdleLoopOrchestrator(
        audio_source=audio_source,
        detector=SingleWakeDetector(),
        state_callback=states.append,
        time_fn=clock,
    )
    recorder = UtteranceRecorder(
        frame_source=audio_source,
        capture_config=capture_config,
        detector=EnergyVoiceActivityDetector(VoiceActivityConfig(energy_threshold=200)),
        config=UtteranceRecorderConfig(
            initial_silence_timeout_seconds=0.5,
            silence_stop_seconds=0.2,
            max_utterance_seconds=2.0,
        ),
        time_fn=clock,
    )
    controller = WakeTriggeredUtteranceController(
        idle_loop=idle_loop,
        recorder=recorder,
    )

    idle_loop.start()
    result = controller.process_once()

    assert result is not None
    assert result.detection == WakeDetectionEvent(keyword="hey bob", score=0.95)
    assert result.utterance.stop_reason == UtteranceStopReason.END_OF_SPEECH
    assert result.utterance.frame_count == 4
    assert idle_loop.state == AssistantState.IDLE
    assert states == [
        AssistantState.IDLE,
        AssistantState.TRIGGERED,
        AssistantState.IDLE,
    ]

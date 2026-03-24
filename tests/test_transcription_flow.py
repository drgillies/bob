"""Tests for wake -> utterance -> transcription orchestration."""

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
    IdleLoopOrchestrator,
    WakeTriggeredTranscriptionController,
    WakeTriggeredUtteranceController,
)
from bob.stt import (
    RecordedUtterance,
    SpeechToTextTranscriptionError,
    TranscriptionResult,
    UtteranceStopReason,
)
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
    def process_frame(self, frame: bytes) -> WakeDetectionEvent | None:
        del frame
        return WakeDetectionEvent(keyword="hey bob", score=0.95)

    def reset(self) -> None:
        return None


class FakeSpeechToTextService:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.utterances: list[RecordedUtterance] = []

    def transcribe(self, utterance: RecordedUtterance) -> TranscriptionResult:
        self.utterances.append(utterance)
        if self.fail:
            raise SpeechToTextTranscriptionError("boom")
        return TranscriptionResult(
            text="open calculator",
            confidence=0.75,
            language="en",
            engine="fake-stt",
            utterance_duration_seconds=utterance.duration_seconds,
            audio_duration_seconds=utterance.duration_seconds,
        )


def build_flow() -> tuple[IdleLoopOrchestrator, WakeTriggeredTranscriptionController]:
    clock = FakeClock()
    capture_config = AudioCaptureConfig(frame_duration_ms=100)
    block_size = capture_config.block_size
    audio_source = SharedAudioSource(
        [
            pcm_frame(100, sample_count=block_size),
            pcm_frame(1000, sample_count=block_size),
            pcm_frame(900, sample_count=block_size),
            pcm_frame(0, sample_count=block_size),
            pcm_frame(0, sample_count=block_size),
        ],
        clock=clock,
        step=0.1,
    )
    idle_loop = IdleLoopOrchestrator(
        audio_source=audio_source,
        detector=SingleWakeDetector(),
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
    utterance_controller = WakeTriggeredUtteranceController(
        idle_loop=idle_loop,
        recorder=recorder,
    )
    transcription_controller = WakeTriggeredTranscriptionController(
        utterance_controller=utterance_controller,
        stt_service=FakeSpeechToTextService(),
    )
    return idle_loop, transcription_controller


def test_transcription_flow_returns_wake_event_and_transcript() -> None:
    idle_loop, controller = build_flow()

    idle_loop.start()
    result = controller.process_once()

    assert result is not None
    assert result.wake_event.detection == WakeDetectionEvent(
        keyword="hey bob",
        score=0.95,
    )
    assert result.wake_event.utterance.stop_reason == UtteranceStopReason.END_OF_SPEECH
    assert result.transcription.text == "open calculator"
    assert result.transcription.engine == "fake-stt"
    assert idle_loop.state.value == "IDLE"


def test_transcription_flow_propagates_stt_error_after_returning_idle() -> None:
    clock = FakeClock()
    capture_config = AudioCaptureConfig(frame_duration_ms=100)
    block_size = capture_config.block_size
    audio_source = SharedAudioSource(
        [
            pcm_frame(100, sample_count=block_size),
            pcm_frame(1000, sample_count=block_size),
            pcm_frame(900, sample_count=block_size),
            pcm_frame(0, sample_count=block_size),
            pcm_frame(0, sample_count=block_size),
        ],
        clock=clock,
        step=0.1,
    )
    idle_loop = IdleLoopOrchestrator(
        audio_source=audio_source,
        detector=SingleWakeDetector(),
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
    utterance_controller = WakeTriggeredUtteranceController(
        idle_loop=idle_loop,
        recorder=recorder,
    )
    controller = WakeTriggeredTranscriptionController(
        utterance_controller=utterance_controller,
        stt_service=FakeSpeechToTextService(fail=True),
    )

    idle_loop.start()
    try:
        controller.process_once()
        assert False, "Expected SpeechToTextTranscriptionError"
    except SpeechToTextTranscriptionError:
        pass

    assert idle_loop.state.value == "IDLE"

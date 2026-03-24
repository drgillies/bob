"""Tests for utterance recording and energy-based VAD."""

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
from bob.stt import UtteranceStopReason


def pcm_frame(amplitude: int, sample_count: int = 8) -> bytes:
    """Build a little-endian int16 PCM frame with repeated amplitude."""
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


class FakeFrameSource:
    def __init__(self, frames: list[bytes | None], clock: FakeClock, step: float) -> None:
        self.frames = list(frames)
        self.clock = clock
        self.step = step

    def read_frame(self, timeout_seconds: float | None = None) -> bytes | None:
        del timeout_seconds
        self.clock.advance(self.step)
        if not self.frames:
            return None
        return self.frames.pop(0)


def test_energy_vad_detects_speech_only_above_threshold() -> None:
    detector = EnergyVoiceActivityDetector(VoiceActivityConfig(energy_threshold=200))

    assert detector.is_speech(pcm_frame(50)) is False
    assert detector.is_speech(pcm_frame(600)) is True


def test_recorder_stops_on_end_of_speech_and_keeps_trailing_buffer() -> None:
    clock = FakeClock()
    capture_config = AudioCaptureConfig(frame_duration_ms=100)
    block_size = capture_config.block_size
    frame_source = FakeFrameSource(
        [
            pcm_frame(1000, sample_count=block_size),
            pcm_frame(900, sample_count=block_size),
            pcm_frame(0, sample_count=block_size),
            pcm_frame(0, sample_count=block_size),
        ],
        clock=clock,
        step=0.1,
    )
    recorder = UtteranceRecorder(
        frame_source=frame_source,
        capture_config=capture_config,
        detector=EnergyVoiceActivityDetector(VoiceActivityConfig(energy_threshold=200)),
        config=UtteranceRecorderConfig(
            initial_silence_timeout_seconds=0.5,
            silence_stop_seconds=0.2,
            max_utterance_seconds=2.0,
        ),
        time_fn=clock,
    )

    result = recorder.record()

    assert result.stop_reason == UtteranceStopReason.END_OF_SPEECH
    assert result.speech_started is True
    assert result.frame_count == 4
    assert result.speech_frame_count == 2
    assert result.duration_seconds == 0.4
    assert result.audio_bytes == (
        pcm_frame(1000, sample_count=block_size)
        + pcm_frame(900, sample_count=block_size)
        + pcm_frame(0, sample_count=block_size)
        + pcm_frame(0, sample_count=block_size)
    )


def test_recorder_times_out_when_no_speech_starts() -> None:
    clock = FakeClock()
    capture_config = AudioCaptureConfig(frame_duration_ms=100)
    block_size = capture_config.block_size
    frame_source = FakeFrameSource(
        [
            pcm_frame(0, sample_count=block_size),
            pcm_frame(0, sample_count=block_size),
            None,
            None,
        ],
        clock=clock,
        step=0.1,
    )
    recorder = UtteranceRecorder(
        frame_source=frame_source,
        capture_config=capture_config,
        detector=EnergyVoiceActivityDetector(VoiceActivityConfig(energy_threshold=200)),
        config=UtteranceRecorderConfig(
            initial_silence_timeout_seconds=0.2,
            silence_stop_seconds=0.2,
            max_utterance_seconds=1.0,
        ),
        time_fn=clock,
    )

    result = recorder.record()

    assert result.stop_reason == UtteranceStopReason.TIMEOUT
    assert result.speech_started is False
    assert result.frame_count == 0
    assert result.audio_bytes == b""
    assert result.duration_seconds == 0.0


def test_recorder_times_out_after_max_utterance_duration() -> None:
    clock = FakeClock()
    capture_config = AudioCaptureConfig(frame_duration_ms=100)
    block_size = capture_config.block_size
    frame_source = FakeFrameSource(
        [
            pcm_frame(900, sample_count=block_size),
            pcm_frame(900, sample_count=block_size),
            pcm_frame(900, sample_count=block_size),
            pcm_frame(900, sample_count=block_size),
        ],
        clock=clock,
        step=0.1,
    )
    recorder = UtteranceRecorder(
        frame_source=frame_source,
        capture_config=capture_config,
        detector=EnergyVoiceActivityDetector(VoiceActivityConfig(energy_threshold=200)),
        config=UtteranceRecorderConfig(
            initial_silence_timeout_seconds=0.2,
            silence_stop_seconds=0.3,
            max_utterance_seconds=0.25,
        ),
        time_fn=clock,
    )

    result = recorder.record()

    assert result.stop_reason == UtteranceStopReason.TIMEOUT
    assert result.speech_started is True
    assert result.frame_count == 3
    assert result.speech_frame_count == 3

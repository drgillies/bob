"""Utterance recording with lightweight energy-based voice activity detection."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from time import monotonic
from typing import Callable, Protocol

from bob.audio.capture import AudioCaptureConfig
from bob.stt import RecordedUtterance, UtteranceStopReason


class AudioFrameSource(Protocol):
    """Minimal frame source interface for utterance recording."""

    def read_frame(self, timeout_seconds: float | None = None) -> bytes | None:
        """Return the next PCM frame if one is available."""


class VoiceActivityDetector(Protocol):
    """Detect whether a PCM frame contains speech-like energy."""

    def is_speech(self, frame: bytes) -> bool:
        """Return True when the frame should count as active speech."""


@dataclass(frozen=True)
class VoiceActivityConfig:
    """Configuration for frame-level speech detection."""

    energy_threshold: int = 350


class EnergyVoiceActivityDetector:
    """Simple RMS-energy detector for int16 mono PCM frames."""

    def __init__(self, config: VoiceActivityConfig | None = None) -> None:
        self._config = config or VoiceActivityConfig()

    def is_speech(self, frame: bytes) -> bool:
        if len(frame) < 2:
            return False

        sample_total = 0
        for index in range(0, len(frame) - 1, 2):
            sample = int.from_bytes(
                frame[index : index + 2],
                byteorder="little",
                signed=True,
            )
            sample_total += sample * sample

        sample_count = len(frame) // 2
        if sample_count == 0:
            return False

        mean_square = sample_total / sample_count
        rms = mean_square ** 0.5
        return rms >= self._config.energy_threshold


@dataclass(frozen=True)
class UtteranceRecorderConfig:
    """Capture settings for post-wake utterance collection."""

    read_timeout_seconds: float = 0.1
    initial_silence_timeout_seconds: float = 2.0
    silence_stop_seconds: float = 0.8
    max_utterance_seconds: float = 8.0


class UtteranceRecorder:
    """Record an utterance until end-of-speech or timeout."""

    def __init__(
        self,
        frame_source: AudioFrameSource,
        capture_config: AudioCaptureConfig,
        detector: VoiceActivityDetector | None = None,
        config: UtteranceRecorderConfig | None = None,
        *,
        time_fn: Callable[[], float] = monotonic,
    ) -> None:
        self._frame_source = frame_source
        self._capture_config = capture_config
        self._detector = detector or EnergyVoiceActivityDetector()
        self._config = config or UtteranceRecorderConfig()
        self._time_fn = time_fn

    def record(self) -> RecordedUtterance:
        """Capture one utterance and stop on silence or timeout."""
        start_time = self._time_fn()
        frame_duration_seconds = self._capture_config.frame_duration_seconds
        silence_frames_required = max(
            1,
            ceil(self._config.silence_stop_seconds / frame_duration_seconds),
        )

        recorded_frames: list[bytes] = []
        trailing_frames: list[bytes] = []
        speech_started = False
        speech_frame_count = 0

        while True:
            elapsed_seconds = self._time_fn() - start_time
            if elapsed_seconds >= self._config.max_utterance_seconds:
                if speech_started and trailing_frames:
                    recorded_frames.extend(trailing_frames)
                return self._build_result(
                    recorded_frames=recorded_frames,
                    speech_started=speech_started,
                    speech_frame_count=speech_frame_count,
                    stop_reason=UtteranceStopReason.TIMEOUT,
                )

            frame = self._frame_source.read_frame(
                timeout_seconds=self._config.read_timeout_seconds
            )
            if frame is None:
                if (
                    not speech_started
                    and elapsed_seconds >= self._config.initial_silence_timeout_seconds
                ):
                    return self._build_result(
                        recorded_frames=recorded_frames,
                        speech_started=False,
                        speech_frame_count=0,
                        stop_reason=UtteranceStopReason.TIMEOUT,
                    )
                continue

            if self._detector.is_speech(frame):
                if trailing_frames:
                    recorded_frames.extend(trailing_frames)
                    trailing_frames.clear()
                recorded_frames.append(frame)
                speech_started = True
                speech_frame_count += 1
                continue

            if not speech_started:
                if elapsed_seconds >= self._config.initial_silence_timeout_seconds:
                    return self._build_result(
                        recorded_frames=recorded_frames,
                        speech_started=False,
                        speech_frame_count=0,
                        stop_reason=UtteranceStopReason.TIMEOUT,
                    )
                continue

            trailing_frames.append(frame)
            if len(trailing_frames) >= silence_frames_required:
                recorded_frames.extend(trailing_frames)
                return self._build_result(
                    recorded_frames=recorded_frames,
                    speech_started=True,
                    speech_frame_count=speech_frame_count,
                    stop_reason=UtteranceStopReason.END_OF_SPEECH,
                )

    def _build_result(
        self,
        *,
        recorded_frames: list[bytes],
        speech_started: bool,
        speech_frame_count: int,
        stop_reason: UtteranceStopReason,
    ) -> RecordedUtterance:
        return RecordedUtterance(
            audio_bytes=b"".join(recorded_frames),
            sample_rate_hz=self._capture_config.sample_rate_hz,
            channels=self._capture_config.channels,
            sample_width_bytes=self._capture_config.sample_width_bytes,
            frame_count=len(recorded_frames),
            speech_started=speech_started,
            stop_reason=stop_reason,
            speech_frame_count=speech_frame_count,
        )

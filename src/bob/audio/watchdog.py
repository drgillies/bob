"""Audio watchdog helpers for stalled-stream detection."""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Callable, Protocol


class RecoverableAudioSource(Protocol):
    """Minimal audio source interface used by the watchdog."""

    def is_running(self) -> bool:
        """Return whether the audio source is active."""

    def recover_stream(self) -> bool:
        """Attempt to recover the audio stream."""


@dataclass(frozen=True)
class AudioWatchdogConfig:
    """Settings for no-audio watchdog behavior."""

    no_audio_timeout_seconds: float = 5.0


class AudioWatchdog:
    """Track the last audio frame time and reset a stalled stream."""

    def __init__(
        self,
        audio_source: RecoverableAudioSource,
        config: AudioWatchdogConfig | None = None,
        *,
        time_fn: Callable[[], float] = monotonic,
    ) -> None:
        self._audio_source = audio_source
        self._config = config or AudioWatchdogConfig()
        self._time_fn = time_fn
        self._last_frame_time: float | None = None
        self._last_reset_time: float | None = None

    @property
    def last_frame_time(self) -> float | None:
        """Return the last observed audio-frame timestamp."""
        return self._last_frame_time

    @property
    def last_reset_time(self) -> float | None:
        """Return the last watchdog-triggered reset timestamp."""
        return self._last_reset_time

    def record_frame(self) -> None:
        """Record that an audio frame was observed now."""
        self._last_frame_time = self._time_fn()

    def poll(self) -> bool:
        """Return True when the watchdog triggered a stream recovery."""
        if not self._audio_source.is_running():
            return False
        if self._last_frame_time is None:
            return False

        now = self._time_fn()
        if now - self._last_frame_time < self._config.no_audio_timeout_seconds:
            return False

        recovered = self._audio_source.recover_stream()
        if recovered:
            self._last_reset_time = now
            self._last_frame_time = now
        return recovered

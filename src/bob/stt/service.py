"""Speech-to-text data contracts shared with audio recording."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class UtteranceStopReason(str, Enum):
    """Reason an utterance recording session ended."""

    END_OF_SPEECH = "END_OF_SPEECH"
    TIMEOUT = "TIMEOUT"


@dataclass(frozen=True)
class RecordedUtterance:
    """PCM utterance data and capture metadata for downstream STT."""

    audio_bytes: bytes
    sample_rate_hz: int
    channels: int
    sample_width_bytes: int
    frame_count: int
    speech_started: bool
    stop_reason: UtteranceStopReason
    speech_frame_count: int = 0

    @property
    def duration_seconds(self) -> float:
        """Return utterance duration derived from raw PCM length."""
        bytes_per_frame = self.channels * self.sample_width_bytes
        if bytes_per_frame == 0:
            return 0.0
        sample_count = len(self.audio_bytes) / bytes_per_frame
        return sample_count / self.sample_rate_hz

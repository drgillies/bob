"""Wake-word detector interfaces and shared types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class WakeDetectionEvent:
    """Represents a single wake-word detection."""

    keyword: str
    score: float | None = None


class WakeWordDetector(Protocol):
    """Minimal detector interface for idle-loop wake-word processing."""

    def process_frame(self, frame: bytes) -> WakeDetectionEvent | None:
        """Inspect an audio frame and return a detection event if triggered."""

    def reset(self) -> None:
        """Reset any internal detector state after a handled wake event."""

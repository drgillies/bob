"""Intent routing models shared across router and handlers."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class IntentName(str, Enum):
    """Supported MVP intent identifiers."""

    GET_TIME = "GET_TIME"
    GET_DATE = "GET_DATE"
    STATUS = "STATUS"
    CAPABILITIES = "CAPABILITIES"
    LISTENING_STATUS = "LISTENING_STATUS"
    OPEN_APP = "OPEN_APP"
    PLAY_MEDIA = "PLAY_MEDIA"
    PAUSE_MEDIA = "PAUSE_MEDIA"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class IntentRequest:
    """Normalized intent request derived from transcription text."""

    raw_text: str
    normalized_text: str


@dataclass(frozen=True)
class IntentMatch:
    """Resolved intent and any extracted slots."""

    name: IntentName
    confidence: float
    matched_phrase: str
    slots: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class IntentResponse:
    """Response text and routing metadata for downstream TTS/action layers."""

    intent: IntentName
    text: str
    handled: bool = True
    metadata: dict[str, str] = field(default_factory=dict)

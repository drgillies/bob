"""Session-memory and recovery-event models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from bob.data.model.intent import IntentName


class ErrorComponent(str, Enum):
    """Runtime component categories used for recovery bookkeeping."""

    AUDIO = "AUDIO"
    WAKEWORD = "WAKEWORD"
    STT = "STT"
    ROUTER = "ROUTER"
    HANDLER = "HANDLER"
    TTS = "TTS"
    ACTION = "ACTION"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class SessionTurn:
    """Single in-memory interaction captured for the current runtime."""

    user_text: str
    intent: IntentName
    response_text: str
    handled: bool


@dataclass(frozen=True)
class RecoveryEvent:
    """Recovered runtime error recorded in session memory."""

    component: ErrorComponent
    message: str


@dataclass(frozen=True)
class SessionMemorySnapshot:
    """Read-only view of current session memory state."""

    turns: tuple[SessionTurn, ...] = ()
    errors: tuple[RecoveryEvent, ...] = ()
    last_intent: IntentName | None = None
    last_response: str | None = None
    last_user_text: str | None = None
    recent_user_texts: tuple[str, ...] = field(default_factory=tuple)

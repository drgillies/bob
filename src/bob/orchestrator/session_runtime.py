"""Session-memory and resilient runtime orchestration."""

from __future__ import annotations

from dataclasses import dataclass

from bob.data.model import (
    ErrorComponent,
    RecoveryEvent,
    SessionMemorySnapshot,
    SessionTurn,
)
from bob.orchestrator.idle_loop import IdleLoopOrchestrator
from bob.orchestrator.intent_flow import IntentResponseController, RoutedTranscription
from bob.skills.actions import LocalActionError
from bob.stt import SpeechToTextError
from bob.tts import SpeechSynthesizer, TextToSpeechError


@dataclass(frozen=True)
class SessionMemoryConfig:
    """Retention limits for runtime-only session memory."""

    max_turns: int = 5
    max_errors: int = 10


class SessionMemoryStore:
    """Store recent turns and recovered errors for the current process only."""

    def __init__(self, config: SessionMemoryConfig | None = None) -> None:
        self._config = config or SessionMemoryConfig()
        self._turns: list[SessionTurn] = []
        self._errors: list[RecoveryEvent] = []

    def record_turn(self, routed: RoutedTranscription) -> None:
        """Add a completed turn to the current session buffer."""
        turn = SessionTurn(
            user_text=routed.transcription_event.transcription.text,
            intent=routed.intent_match.name,
            response_text=routed.response.text,
            handled=routed.response.handled,
        )
        self._turns.append(turn)
        self._turns = self._turns[-self._config.max_turns :]

    def record_error(self, component: ErrorComponent, message: str) -> RecoveryEvent:
        """Add a recovered runtime error to the session buffer."""
        event = RecoveryEvent(component=component, message=message)
        self._errors.append(event)
        self._errors = self._errors[-self._config.max_errors :]
        return event

    def clear(self) -> None:
        """Drop all runtime-only session state."""
        self._turns.clear()
        self._errors.clear()

    def snapshot(self) -> SessionMemorySnapshot:
        """Return a read-only memory snapshot."""
        last_turn = self._turns[-1] if self._turns else None
        return SessionMemorySnapshot(
            turns=tuple(self._turns),
            errors=tuple(self._errors),
            last_intent=last_turn.intent if last_turn is not None else None,
            last_response=last_turn.response_text if last_turn is not None else None,
            last_user_text=last_turn.user_text if last_turn is not None else None,
            recent_user_texts=tuple(turn.user_text for turn in self._turns),
        )


@dataclass(frozen=True)
class AssistantCycleResult:
    """Outcome of one top-level assistant cycle."""

    routed: RoutedTranscription | None = None
    recovered_error: RecoveryEvent | None = None


class SessionAwareAssistantController:
    """Run intent response + TTS with session memory and recovery behavior."""

    def __init__(
        self,
        intent_controller: IntentResponseController,
        synthesizer: SpeechSynthesizer,
        session_memory: SessionMemoryStore,
        *,
        idle_loop: IdleLoopOrchestrator | None = None,
    ) -> None:
        self._intent_controller = intent_controller
        self._synthesizer = synthesizer
        self._session_memory = session_memory
        self._idle_loop = idle_loop

    def process_once(self) -> AssistantCycleResult | None:
        """Run one assistant cycle and recover cleanly from transient failures."""
        try:
            routed = self._intent_controller.process_once()
            if routed is None:
                return None

            self._session_memory.record_turn(routed)
            self._synthesizer.speak(routed.response.text)
            return AssistantCycleResult(routed=routed)
        except Exception as exc:
            recovered = self._recover_from_error(exc)
            return AssistantCycleResult(recovered_error=recovered)

    def _recover_from_error(self, exc: Exception) -> RecoveryEvent:
        component = classify_runtime_error(exc)
        if self._idle_loop is not None:
            self._idle_loop.acknowledge_trigger()
        return self._session_memory.record_error(component, str(exc))


def classify_runtime_error(exc: Exception) -> ErrorComponent:
    """Map runtime exceptions to the component that should own recovery."""
    if isinstance(exc, SpeechToTextError):
        return ErrorComponent.STT
    if isinstance(exc, TextToSpeechError):
        return ErrorComponent.TTS
    if isinstance(exc, LocalActionError):
        return ErrorComponent.ACTION
    return ErrorComponent.UNKNOWN

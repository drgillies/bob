"""Deterministic wake-response orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from bob.orchestrator.idle_loop import AssistantState, IdleLoopOrchestrator
from bob.tts import SpeechSynthesizer
from bob.wakeword import WakeDetectionEvent


class ResponseState(str, Enum):
    """Observable states for deterministic response flow."""

    IDLE = "IDLE"
    TRIGGERED = "TRIGGERED"
    SPEAKING = "SPEAKING"


@dataclass(frozen=True)
class DeterministicResponseConfig:
    """Config for response text after wake detection."""

    reply_text: str = "Hello, I'm here."


class DeterministicResponseController:
    """Speak a deterministic reply after wake detection and return to idle."""

    def __init__(
        self,
        idle_loop: IdleLoopOrchestrator,
        synthesizer: SpeechSynthesizer,
        config: DeterministicResponseConfig | None = None,
        *,
        state_callback: Callable[[ResponseState], None] | None = None,
    ) -> None:
        self._idle_loop = idle_loop
        self._synthesizer = synthesizer
        self._config = config or DeterministicResponseConfig()
        self._state_callback = state_callback

    def process_once(self) -> WakeDetectionEvent | None:
        """Process one wake-word polling cycle and speak if triggered."""
        detection = self._idle_loop.poll_once()
        if detection is None:
            return None

        self._emit_state(ResponseState.TRIGGERED)
        try:
            self._emit_state(ResponseState.SPEAKING)
            self._synthesizer.speak(self._config.reply_text)
        finally:
            self._idle_loop.acknowledge_trigger()
            self._emit_state(ResponseState.IDLE)
        return detection

    @staticmethod
    def map_assistant_state(state: AssistantState) -> ResponseState:
        """Map idle-loop state to response-flow state names."""
        if state == AssistantState.TRIGGERED:
            return ResponseState.TRIGGERED
        return ResponseState.IDLE

    def _emit_state(self, state: ResponseState) -> None:
        if self._state_callback is not None:
            self._state_callback(state)

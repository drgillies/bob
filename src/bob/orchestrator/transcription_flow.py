"""Wake-to-transcription orchestration built on utterance recording."""

from __future__ import annotations

from dataclasses import dataclass

from bob.orchestrator.utterance_flow import (
    WakeTriggeredUtterance,
    WakeTriggeredUtteranceController,
)
from bob.stt import SpeechToTextService, TranscriptionResult


@dataclass(frozen=True)
class WakeTriggeredTranscription:
    """A wake event, the recorded utterance, and its transcription."""

    wake_event: WakeTriggeredUtterance
    transcription: TranscriptionResult


class WakeTriggeredTranscriptionController:
    """Record and transcribe one utterance after a wake event."""

    def __init__(
        self,
        utterance_controller: WakeTriggeredUtteranceController,
        stt_service: SpeechToTextService,
    ) -> None:
        self._utterance_controller = utterance_controller
        self._stt_service = stt_service

    def process_once(self) -> WakeTriggeredTranscription | None:
        """Run one wake cycle through utterance capture and STT."""
        wake_event = self._utterance_controller.process_once()
        if wake_event is None:
            return None

        transcription = self._stt_service.transcribe(wake_event.utterance)
        return WakeTriggeredTranscription(
            wake_event=wake_event,
            transcription=transcription,
        )

"""Transcription-to-intent orchestration."""

from __future__ import annotations

from dataclasses import dataclass

from bob.data.model import IntentMatch, IntentResponse
from bob.orchestrator.transcription_flow import (
    WakeTriggeredTranscription,
    WakeTriggeredTranscriptionController,
)
from bob.skills import IntentRouter
from bob.skills.handlers import CoreIntentHandler


@dataclass(frozen=True)
class RoutedTranscription:
    """Transcription plus the routed intent and response."""

    transcription_event: WakeTriggeredTranscription
    intent_match: IntentMatch
    response: IntentResponse


class IntentResponseController:
    """Route transcriptions into deterministic MVP responses."""

    def __init__(
        self,
        transcription_controller: WakeTriggeredTranscriptionController,
        router: IntentRouter,
        handler: CoreIntentHandler,
    ) -> None:
        self._transcription_controller = transcription_controller
        self._router = router
        self._handler = handler

    def process_once(self) -> RoutedTranscription | None:
        """Run wake -> transcription -> intent response."""
        transcription_event = self._transcription_controller.process_once()
        if transcription_event is None:
            return None

        intent_match = self._router.route_text(transcription_event.transcription.text)
        response = self._handler.handle(intent_match)
        return RoutedTranscription(
            transcription_event=transcription_event,
            intent_match=intent_match,
            response=response,
        )

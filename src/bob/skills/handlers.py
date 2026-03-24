"""Core MVP intent handlers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from bob.data.model import IntentMatch, IntentName, IntentResponse
from bob.skills.actions import LocalActionError, OpenAppAction


@dataclass(frozen=True)
class CoreIntentHandlerConfig:
    """Config for default handler response text."""

    capabilities_summary: str = (
        "I can tell you the time, tell you the date, confirm I'm listening, "
        "and get ready to open apps or control media once those actions are enabled."
    )
    status_response: str = "Yes, I'm here."
    listening_response: str = "Yes, I'm listening."
    unknown_response: str = (
        "I didn't catch a supported command yet. You can ask for the time, date, "
        "or what I can do."
    )


class CoreIntentHandler:
    """Resolve routed intents into user-facing responses."""

    def __init__(
        self,
        config: CoreIntentHandlerConfig | None = None,
        *,
        now_fn: Callable[[], datetime] = datetime.now,
        open_app_action: OpenAppAction | None = None,
    ) -> None:
        self._config = config or CoreIntentHandlerConfig()
        self._now_fn = now_fn
        self._open_app_action = open_app_action

    def handle(self, match: IntentMatch) -> IntentResponse:
        """Return the response for a matched intent."""
        if match.name == IntentName.GET_TIME:
            return IntentResponse(
                intent=IntentName.GET_TIME,
                text=f"The time is {self._now_fn().strftime('%I:%M %p').lstrip('0')}.",
            )

        if match.name == IntentName.GET_DATE:
            return IntentResponse(
                intent=IntentName.GET_DATE,
                text=f"Today's date is {self._now_fn().strftime('%A, %B %d, %Y')}.",
            )

        if match.name == IntentName.STATUS:
            return IntentResponse(
                intent=IntentName.STATUS,
                text=self._config.status_response,
            )

        if match.name == IntentName.CAPABILITIES:
            return IntentResponse(
                intent=IntentName.CAPABILITIES,
                text=self._config.capabilities_summary,
            )

        if match.name == IntentName.LISTENING_STATUS:
            return IntentResponse(
                intent=IntentName.LISTENING_STATUS,
                text=self._config.listening_response,
            )

        if match.name == IntentName.OPEN_APP:
            app_name = match.slots.get("app_name", "that app")
            if self._open_app_action is None:
                return IntentResponse(
                    intent=IntentName.OPEN_APP,
                    text=f"I heard open {app_name}, but app launching is not enabled yet.",
                    metadata={"app_name": app_name},
                )

            try:
                result = self._open_app_action.execute(app_name)
            except LocalActionError:
                return IntentResponse(
                    intent=IntentName.OPEN_APP,
                    text=f"I tried to open {app_name}, but the launch failed.",
                    handled=False,
                    metadata={"app_name": app_name},
                )

            return IntentResponse(
                intent=IntentName.OPEN_APP,
                text=result.message,
                handled=result.succeeded,
                metadata=result.metadata,
            )

        if match.name == IntentName.PLAY_MEDIA:
            return IntentResponse(
                intent=IntentName.PLAY_MEDIA,
                text="I heard play music, but media controls are not enabled yet.",
            )

        if match.name == IntentName.PAUSE_MEDIA:
            return IntentResponse(
                intent=IntentName.PAUSE_MEDIA,
                text="I heard pause music, but media controls are not enabled yet.",
            )

        return IntentResponse(
            intent=IntentName.UNKNOWN,
            text=self._config.unknown_response,
            handled=False,
        )

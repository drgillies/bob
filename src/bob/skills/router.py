"""Deterministic intent routing for MVP commands."""

from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher

from bob.data.model import IntentMatch, IntentName, IntentRequest


def normalize_text(text: str) -> str:
    """Normalize user text for deterministic matching."""
    lowered = text.lower().strip()
    lowered = re.sub(r"[^a-z0-9\s]", " ", lowered)
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered.strip()


@dataclass(frozen=True)
class IntentRouterConfig:
    """Config for deterministic routing behavior."""

    fuzzy_match_threshold: float = 0.86


class IntentRouter:
    """Route normalized text into one of the MVP intents."""

    def __init__(self, config: IntentRouterConfig | None = None) -> None:
        self._config = config or IntentRouterConfig()
        self._exact_phrases: dict[str, IntentName] = {
            "what time is it": IntentName.GET_TIME,
            "what is the time": IntentName.GET_TIME,
            "tell me the time": IntentName.GET_TIME,
            "what date is it": IntentName.GET_DATE,
            "what day is it": IntentName.GET_DATE,
            "what is todays date": IntentName.GET_DATE,
            "what is today s date": IntentName.GET_DATE,
            "what is the date": IntentName.GET_DATE,
            "tell me the date": IntentName.GET_DATE,
            "are you there": IntentName.STATUS,
            "what can you do": IntentName.CAPABILITIES,
            "are you listening": IntentName.LISTENING_STATUS,
            "play music": IntentName.PLAY_MEDIA,
            "pause music": IntentName.PAUSE_MEDIA,
        }

    def route_text(self, text: str) -> IntentMatch:
        """Normalize and route freeform text."""
        request = IntentRequest(raw_text=text, normalized_text=normalize_text(text))
        return self.route_request(request)

    def route_request(self, request: IntentRequest) -> IntentMatch:
        """Route a normalized request."""
        if not request.normalized_text:
            return IntentMatch(
                name=IntentName.UNKNOWN,
                confidence=0.0,
                matched_phrase="",
            )

        open_app_match = self._match_open_app(request.normalized_text)
        if open_app_match is not None:
            return open_app_match

        if request.normalized_text in self._exact_phrases:
            matched_name = self._exact_phrases[request.normalized_text]
            return IntentMatch(
                name=matched_name,
                confidence=1.0,
                matched_phrase=request.normalized_text,
            )

        fuzzy_match = self._match_fuzzy(request.normalized_text)
        if fuzzy_match is not None:
            return fuzzy_match

        return IntentMatch(
            name=IntentName.UNKNOWN,
            confidence=0.0,
            matched_phrase=request.normalized_text,
        )

    def _match_open_app(self, normalized_text: str) -> IntentMatch | None:
        if not normalized_text.startswith("open "):
            return None

        app_name = normalized_text[5:].strip()
        if not app_name:
            return IntentMatch(
                name=IntentName.UNKNOWN,
                confidence=0.0,
                matched_phrase=normalized_text,
            )

        return IntentMatch(
            name=IntentName.OPEN_APP,
            confidence=1.0,
            matched_phrase="open <app>",
            slots={"app_name": app_name},
        )

    def _match_fuzzy(self, normalized_text: str) -> IntentMatch | None:
        best_phrase = ""
        best_name = IntentName.UNKNOWN
        best_score = 0.0

        for phrase, intent_name in self._exact_phrases.items():
            score = SequenceMatcher(a=normalized_text, b=phrase).ratio()
            if score > best_score:
                best_phrase = phrase
                best_name = intent_name
                best_score = score

        if best_score < self._config.fuzzy_match_threshold:
            return None

        return IntentMatch(
            name=best_name,
            confidence=best_score,
            matched_phrase=best_phrase,
        )

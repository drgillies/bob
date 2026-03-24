"""Tests for core MVP intent handlers."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.data.model import IntentMatch, IntentName
from bob.skills import CoreIntentHandler, OpenAppAction, OpenAppActionConfig


def test_time_handler_returns_formatted_time() -> None:
    handler = CoreIntentHandler(now_fn=lambda: datetime(2026, 3, 24, 9, 5))

    response = handler.handle(IntentMatch(IntentName.GET_TIME, 1.0, "what time is it"))

    assert response.intent == IntentName.GET_TIME
    assert response.text == "The time is 9:05 AM."


def test_date_handler_returns_formatted_date() -> None:
    handler = CoreIntentHandler(now_fn=lambda: datetime(2026, 3, 24, 9, 5))

    response = handler.handle(IntentMatch(IntentName.GET_DATE, 1.0, "what is the date"))

    assert response.intent == IntentName.GET_DATE
    assert response.text == "Today's date is Tuesday, March 24, 2026."


def test_open_app_handler_returns_safe_placeholder_response() -> None:
    handler = CoreIntentHandler()

    response = handler.handle(
        IntentMatch(
            IntentName.OPEN_APP,
            1.0,
            "open <app>",
            slots={"app_name": "calculator"},
        )
    )

    assert response.intent == IntentName.OPEN_APP
    assert "calculator" in response.text
    assert response.metadata["app_name"] == "calculator"


def test_open_app_handler_uses_action_result_when_action_is_configured() -> None:
    launched: list[str] = []

    def fake_launcher(command: str) -> object:
        launched.append(command)
        return object()

    handler = CoreIntentHandler(
        open_app_action=OpenAppAction(
            OpenAppActionConfig(enabled=True, aliases={"calculator": "calc.exe"}),
            launcher=fake_launcher,
        )
    )

    response = handler.handle(
        IntentMatch(
            IntentName.OPEN_APP,
            1.0,
            "open <app>",
            slots={"app_name": "calculator"},
        )
    )

    assert response.intent == IntentName.OPEN_APP
    assert response.handled is True
    assert response.text == "Opening calculator."
    assert launched == ["calc.exe"]


def test_unknown_handler_returns_fallback_response() -> None:
    handler = CoreIntentHandler()

    response = handler.handle(IntentMatch(IntentName.UNKNOWN, 0.0, ""))

    assert response.intent == IntentName.UNKNOWN
    assert response.handled is False
    assert "time" in response.text.lower()

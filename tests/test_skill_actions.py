"""Tests for local action dispatch."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.skills import (
    LocalActionError,
    OpenAppAction,
    OpenAppActionConfig,
    build_open_app_action,
    normalize_app_name,
)


def test_normalize_app_name_collapses_spacing_and_case() -> None:
    assert normalize_app_name("  Visual   Studio Code  ") == "visual studio code"


def test_open_app_action_launches_known_alias() -> None:
    launched: list[str] = []

    def fake_launcher(command: str) -> object:
        launched.append(command)
        return object()

    action = OpenAppAction(
        OpenAppActionConfig(enabled=True, aliases={"calculator": "calc.exe"}),
        launcher=fake_launcher,
    )

    result = action.execute("Calculator")

    assert result.succeeded is True
    assert result.message == "Opening calculator."
    assert launched == ["calc.exe"]


def test_open_app_action_returns_unknown_for_missing_alias() -> None:
    action = OpenAppAction(OpenAppActionConfig(enabled=True, aliases={}))

    result = action.execute("calculator")

    assert result.succeeded is False
    assert "don't know" in result.message


def test_open_app_action_returns_disabled_message() -> None:
    action = OpenAppAction(OpenAppActionConfig(enabled=False, aliases={"calculator": "calc.exe"}))

    result = action.execute("calculator")

    assert result.succeeded is False
    assert "disabled" in result.message.lower()


def test_open_app_action_wraps_launcher_failure() -> None:
    def fake_launcher(command: str) -> object:
        raise RuntimeError("boom")

    action = OpenAppAction(
        OpenAppActionConfig(enabled=True, aliases={"calculator": "calc.exe"}),
        launcher=fake_launcher,
    )

    try:
        action.execute("calculator")
        assert False, "Expected LocalActionError"
    except LocalActionError as exc:
        assert "calc.exe" in str(exc)


def test_build_open_app_action_reads_aliases_from_settings() -> None:
    launched: list[str] = []

    def fake_launcher(command: str) -> object:
        launched.append(command)
        return object()

    action = build_open_app_action(
        {
            "enabled": True,
            "aliases": {
                "Calculator": "calc.exe",
            },
        },
        launcher=fake_launcher,
    )

    result = action.execute("calculator")

    assert result.succeeded is True
    assert result.message == "Opening calculator."
    assert launched == ["calc.exe"]

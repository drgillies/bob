"""Tests for deterministic intent routing."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.data.model import IntentName, IntentRequest
from bob.skills import IntentRouter, IntentRouterConfig, normalize_text


def test_normalize_text_strips_case_punctuation_and_spacing() -> None:
    assert normalize_text("  What TIME is it?!  ") == "what time is it"


def test_router_matches_exact_time_phrase() -> None:
    router = IntentRouter()

    match = router.route_text("What time is it?")

    assert match.name == IntentName.GET_TIME
    assert match.confidence == 1.0


def test_router_matches_exact_date_variants() -> None:
    router = IntentRouter()

    first = router.route_text("what date is it")
    second = router.route_text("what day is it")

    assert first.name == IntentName.GET_DATE
    assert first.confidence == 1.0
    assert second.name == IntentName.GET_DATE
    assert second.confidence == 1.0


def test_router_matches_fuzzy_phrase_above_threshold() -> None:
    router = IntentRouter(IntentRouterConfig(fuzzy_match_threshold=0.8))

    match = router.route_request(
        IntentRequest(raw_text="what can you doo", normalized_text="what can you doo")
    )

    assert match.name == IntentName.CAPABILITIES
    assert match.confidence < 1.0
    assert match.confidence >= 0.8


def test_router_extracts_open_app_slot() -> None:
    router = IntentRouter()

    match = router.route_text("Open Calculator")

    assert match.name == IntentName.OPEN_APP
    assert match.slots == {"app_name": "calculator"}


def test_router_returns_unknown_for_unmatched_text() -> None:
    router = IntentRouter()

    match = router.route_text("tell me a joke")

    assert match.name == IntentName.UNKNOWN


def test_router_does_not_cross_match_date_phrase_to_time() -> None:
    router = IntentRouter()

    match = router.route_text("what date is it")

    assert match.name != IntentName.GET_TIME

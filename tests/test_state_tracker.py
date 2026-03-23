"""Tests for assistant state tracking."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.observability import StateTracker


def test_state_tracker_records_distinct_states() -> None:
    tracker = StateTracker(initial_state="IDLE")

    tracker.record("TRIGGERED")
    tracker.record("SPEAKING")
    tracker.record("IDLE")

    assert tracker.current_state == "IDLE"
    assert tracker.states == ["IDLE", "TRIGGERED", "SPEAKING", "IDLE"]


def test_state_tracker_ignores_duplicate_state() -> None:
    tracker = StateTracker(initial_state="IDLE")

    tracker.record("IDLE")

    assert tracker.states == ["IDLE"]

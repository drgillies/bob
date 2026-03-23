"""Tests for the openWakeWord detector adapter."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.wakeword import OpenWakeWordConfig, OpenWakeWordDetector, WakeWordError


class FakeModel:
    def __init__(self, predictions: list[dict[str, float]]) -> None:
        self._predictions = list(predictions)
        self.frames_seen: list[bytes] = []
        self.reset_calls = 0

    def predict(self, frame: bytes) -> dict[str, float]:
        self.frames_seen.append(frame)
        if not self._predictions:
            return {}
        return self._predictions.pop(0)

    def reset(self) -> None:
        self.reset_calls += 1


def test_openwakeword_detector_returns_detection_above_threshold() -> None:
    model = FakeModel([{"hey_bob": 0.91}])
    detector = OpenWakeWordDetector(
        OpenWakeWordConfig(keyword="hey_bob", threshold=0.5),
        model_factory=lambda **_: model,
    )

    detection = detector.process_frame(b"frame-1")

    assert detection is not None
    assert detection.keyword == "hey_bob"
    assert detection.score == 0.91
    assert model.frames_seen == [b"frame-1"]


def test_openwakeword_detector_returns_none_below_threshold() -> None:
    model = FakeModel([{"hey_bob": 0.2}])
    detector = OpenWakeWordDetector(
        OpenWakeWordConfig(keyword="hey_bob", threshold=0.5),
        model_factory=lambda **_: model,
    )

    detection = detector.process_frame(b"frame-1")

    assert detection is None


def test_openwakeword_detector_returns_none_when_keyword_missing() -> None:
    model = FakeModel([{"other_keyword": 0.9}])
    detector = OpenWakeWordDetector(
        OpenWakeWordConfig(keyword="hey_bob"),
        model_factory=lambda **_: model,
    )

    detection = detector.process_frame(b"frame-1")

    assert detection is None


def test_openwakeword_detector_reset_delegates_to_model() -> None:
    model = FakeModel([])
    detector = OpenWakeWordDetector(
        OpenWakeWordConfig(keyword="hey_bob"),
        model_factory=lambda **_: model,
    )

    detector.reset()

    assert model.reset_calls == 1


def test_openwakeword_detector_init_raises_when_factory_fails() -> None:
    def failing_factory(**_: object) -> FakeModel:
        raise RuntimeError("bad model")

    try:
        OpenWakeWordDetector(
            OpenWakeWordConfig(keyword="hey_bob"),
            model_factory=failing_factory,
        )
        assert False, "Expected WakeWordError"
    except WakeWordError:
        pass

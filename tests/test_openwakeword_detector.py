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
    def __init__(
        self,
        predictions: list[dict[str, float]],
        *,
        class_mapping: dict[str, dict[str, str]] | None = None,
        models: dict[str, object] | None = None,
    ) -> None:
        self._predictions = list(predictions)
        self.frames_seen: list[bytes] = []
        self.reset_calls = 0
        self.class_mapping = class_mapping or {}
        self.models = models or {}

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


def test_openwakeword_detector_available_keywords_reads_class_mapping() -> None:
    model = FakeModel(
        [],
        class_mapping={"hey_bob": {"0": "hey_bob"}},
    )
    detector = OpenWakeWordDetector(
        OpenWakeWordConfig(keyword="hey_bob"),
        model_factory=lambda **_: model,
    )

    keywords = detector.available_keywords()

    assert keywords == ["hey_bob"]


def test_openwakeword_detector_passes_custom_model_kwargs(tmp_path: Path) -> None:
    model_path = tmp_path / "hey_bob.onnx"
    model_path.write_bytes(b"fake-model")
    captured: dict[str, object] = {}
    model = FakeModel([], models={"hey_bob": object()})

    def factory(**kwargs: object) -> FakeModel:
        captured.update(kwargs)
        return model

    OpenWakeWordDetector(
        OpenWakeWordConfig(
            keyword="hey_bob",
            model_path=str(model_path),
            inference_framework="onnx",
            model_kwargs={"vad_threshold": 0.2},
        ),
        model_factory=factory,
    )

    assert captured["wakeword_models"] == [str(model_path)]
    assert captured["inference_framework"] == "onnx"
    assert captured["vad_threshold"] == 0.2


def test_openwakeword_detector_raises_for_missing_configured_model() -> None:
    try:
        OpenWakeWordDetector(OpenWakeWordConfig(keyword="hey_bob", model_path="missing.onnx"))
        assert False, "Expected WakeWordError"
    except WakeWordError as exc:
        assert "does not exist" in str(exc)

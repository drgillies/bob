"""openWakeWord-backed wake-word detector."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import numpy as np

from bob.wakeword.service import WakeDetectionEvent


class WakeWordError(RuntimeError):
    """Raised when a wake-word detector cannot be initialized."""


@dataclass(frozen=True)
class OpenWakeWordConfig:
    """Configuration for the openWakeWord detector adapter."""

    keyword: str
    threshold: float = 0.5
    model_path: str | None = None
    inference_framework: str | None = None
    model_kwargs: dict[str, Any] = field(default_factory=dict)


class OpenWakeWordDetector:
    """Adapt openWakeWord model predictions to Bob's detector interface."""

    def __init__(
        self,
        config: OpenWakeWordConfig,
        model_factory: Callable[..., Any] | None = None,
    ) -> None:
        self._config = config
        self._model = self._build_model(model_factory)

    def process_frame(self, frame: bytes) -> WakeDetectionEvent | None:
        predictions = self._model.predict(self._prepare_frame(frame))
        score = predictions.get(self._config.keyword)
        if score is None:
            return None
        if score < self._config.threshold:
            return None
        return WakeDetectionEvent(keyword=self._config.keyword, score=float(score))

    def reset(self) -> None:
        reset_fn = getattr(self._model, "reset", None)
        if callable(reset_fn):
            reset_fn()

    def available_keywords(self) -> list[str]:
        class_mapping = getattr(self._model, "class_mapping", {})
        if isinstance(class_mapping, dict) and class_mapping:
            keywords: set[str] = set()
            for model_name, labels in class_mapping.items():
                keywords.add(str(model_name))
                if isinstance(labels, dict):
                    keywords.update(str(value) for value in labels.values())
            return sorted(keywords)

        models = getattr(self._model, "models", {})
        if isinstance(models, dict):
            return sorted(str(name) for name in models.keys())

        return []

    @staticmethod
    def _prepare_frame(frame: bytes | bytearray | memoryview | np.ndarray) -> np.ndarray:
        if isinstance(frame, np.ndarray):
            return frame.astype(np.int16, copy=False)
        if isinstance(frame, (bytes, bytearray, memoryview)):
            return np.frombuffer(frame, dtype=np.int16)
        raise WakeWordError(f"Unsupported frame type for openWakeWord: {type(frame)!r}")

    def _build_model(self, model_factory: Callable[..., Any] | None) -> Any:
        model_kwargs = dict(self._config.model_kwargs)
        if self._config.model_path:
            model_path = Path(self._config.model_path)
            if not model_path.exists():
                raise WakeWordError(
                    f"Configured wake-word model does not exist: '{model_path}'"
                )
            model_kwargs["wakeword_models"] = [str(model_path)]
        if self._config.inference_framework:
            model_kwargs["inference_framework"] = self._config.inference_framework

        if model_factory is not None:
            try:
                return model_factory(**model_kwargs)
            except Exception as exc:
                raise WakeWordError(
                    f"Failed to initialize openWakeWord model: {exc}"
                ) from exc

        try:
            from openwakeword.model import Model
        except ImportError as exc:
            raise WakeWordError(
                "openwakeword is not installed. Install it before using the openWakeWord detector."
            ) from exc

        try:
            return Model(**model_kwargs)
        except Exception as exc:  # pragma: no cover - depends on local setup
            raise WakeWordError(f"Failed to initialize openWakeWord model: {exc}") from exc

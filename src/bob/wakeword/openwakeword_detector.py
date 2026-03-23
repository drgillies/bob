"""openWakeWord-backed wake-word detector."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from bob.wakeword.service import WakeDetectionEvent


class WakeWordError(RuntimeError):
    """Raised when a wake-word detector cannot be initialized."""


@dataclass(frozen=True)
class OpenWakeWordConfig:
    """Configuration for the openWakeWord detector adapter."""

    keyword: str
    threshold: float = 0.5
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
        predictions = self._model.predict(frame)
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

    def _build_model(self, model_factory: Callable[..., Any] | None) -> Any:
        if model_factory is not None:
            try:
                return model_factory(**self._config.model_kwargs)
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
            return Model(**self._config.model_kwargs)
        except Exception as exc:  # pragma: no cover - depends on local setup
            raise WakeWordError(f"Failed to initialize openWakeWord model: {exc}") from exc

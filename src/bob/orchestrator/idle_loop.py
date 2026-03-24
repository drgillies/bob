"""Idle-loop orchestration for wake-word driven activation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from time import monotonic
from typing import Callable, Protocol

from bob.data.model import ErrorComponent, RecoveryEvent
from bob.wakeword import WakeDetectionEvent, WakeWordDetector


class AudioFrameSource(Protocol):
    """Minimal audio source interface used by the idle loop."""

    def start(self) -> None:
        """Start streaming audio frames."""

    def stop(self) -> None:
        """Stop streaming audio frames."""

    def is_running(self) -> bool:
        """Return whether the audio source is currently active."""

    def read_frame(self, timeout_seconds: float | None = None) -> bytes | None:
        """Return the next frame if available."""


class AssistantState(str, Enum):
    """Observable runtime state for the assistant idle loop."""

    IDLE = "IDLE"
    TRIGGERED = "TRIGGERED"


@dataclass(frozen=True)
class IdleLoopConfig:
    """Configuration for wake-word processing in the idle loop."""

    read_timeout_seconds: float = 0.1
    debounce_seconds: float = 1.0


class IdleLoopOrchestrator:
    """Coordinate audio frames and wake detection without invoking STT."""

    def __init__(
        self,
        audio_source: AudioFrameSource,
        detector: WakeWordDetector,
        config: IdleLoopConfig | None = None,
        *,
        time_fn: Callable[[], float] = monotonic,
        state_callback: Callable[[AssistantState], None] | None = None,
        error_callback: Callable[[RecoveryEvent], None] | None = None,
    ) -> None:
        self._audio_source = audio_source
        self._detector = detector
        self._config = config or IdleLoopConfig()
        self._time_fn = time_fn
        self._state_callback = state_callback
        self._error_callback = error_callback
        self._state = AssistantState.IDLE
        self._last_trigger_time: float | None = None

    @property
    def state(self) -> AssistantState:
        """Return the current assistant state."""
        return self._state

    def start(self) -> None:
        """Start idle-loop processing."""
        self._audio_source.start()
        if self._state_callback is not None:
            self._state_callback(AssistantState.IDLE)

    def stop(self) -> None:
        """Stop idle-loop processing."""
        self._audio_source.stop()
        self._set_state(AssistantState.IDLE)

    def poll_once(self) -> WakeDetectionEvent | None:
        """Process one frame from the audio source."""
        try:
            frame = self._audio_source.read_frame(
                timeout_seconds=self._config.read_timeout_seconds
            )
        except Exception as exc:
            self._recover_from_error(ErrorComponent.AUDIO, exc, restart_audio=True)
            return None
        if frame is None:
            return None

        try:
            detection = self._detector.process_frame(frame)
        except Exception as exc:
            self._recover_from_error(ErrorComponent.WAKEWORD, exc, restart_audio=False)
            return None
        if detection is None:
            return None

        now = self._time_fn()
        if self._last_trigger_time is not None:
            if now - self._last_trigger_time < self._config.debounce_seconds:
                return None

        self._last_trigger_time = now
        self._detector.reset()
        self._set_state(AssistantState.TRIGGERED)
        return detection

    def acknowledge_trigger(self) -> None:
        """Return the assistant to idle after wake handling completes."""
        self._set_state(AssistantState.IDLE)

    def recover_to_idle(self, *, restart_audio: bool = False) -> None:
        """Best-effort recovery path that returns the runtime to IDLE."""
        if restart_audio and self._audio_source.is_running():
            try:
                self._audio_source.stop()
            except Exception:
                pass
            try:
                self._audio_source.start()
            except Exception:
                pass
        try:
            self._detector.reset()
        except Exception:
            pass
        self._set_state(AssistantState.IDLE)

    def _set_state(self, state: AssistantState) -> None:
        if self._state == state:
            return
        self._state = state
        if self._state_callback is not None:
            self._state_callback(state)

    def _recover_from_error(
        self,
        component: ErrorComponent,
        exc: Exception,
        *,
        restart_audio: bool,
    ) -> None:
        self.recover_to_idle(restart_audio=restart_audio)
        if self._error_callback is not None:
            self._error_callback(RecoveryEvent(component=component, message=str(exc)))

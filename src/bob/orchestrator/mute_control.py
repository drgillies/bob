"""Mute-aware response flow helpers."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from bob.orchestrator.response_flow import DeterministicResponseController
from bob.wakeword import WakeDetectionEvent


class MuteState(str, Enum):
    """Mute status for the assistant runtime."""

    UNMUTED = "UNMUTED"
    MUTED = "MUTED"


@dataclass
class MuteController:
    """Track whether wake handling is currently muted."""

    muted: bool = False

    def set_muted(self, value: bool) -> None:
        self.muted = value

    @property
    def state(self) -> MuteState:
        return MuteState.MUTED if self.muted else MuteState.UNMUTED


class MuteAwareResponseController:
    """Wrap deterministic response flow with config-style mute behavior."""

    def __init__(
        self,
        response_controller: DeterministicResponseController,
        mute_controller: MuteController | None = None,
        *,
        mute_state_callback: Callable[[MuteState], None] | None = None,
    ) -> None:
        self._response_controller = response_controller
        self._mute_controller = mute_controller or MuteController()
        self._mute_state_callback = mute_state_callback

    @property
    def mute_controller(self) -> MuteController:
        return self._mute_controller

    def set_muted(self, value: bool) -> None:
        self._mute_controller.set_muted(value)
        if self._mute_state_callback is not None:
            self._mute_state_callback(self._mute_controller.state)

    def process_once(self) -> WakeDetectionEvent | None:
        """Run response flow unless muted."""
        if self._mute_controller.muted:
            return None
        return self._response_controller.process_once()

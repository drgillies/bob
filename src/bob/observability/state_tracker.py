"""Lightweight assistant state tracking utilities."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class StateTracker:
    """Record and expose assistant state transitions for MVP observability."""

    initial_state: str = "IDLE"
    _states: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._states.append(self.initial_state)

    @property
    def current_state(self) -> str:
        """Return the latest known assistant state."""
        return self._states[-1]

    @property
    def states(self) -> list[str]:
        """Return a copy of all recorded states."""
        return list(self._states)

    def record(self, state: str) -> None:
        """Record a new state if it differs from the current one."""
        if state == self.current_state:
            return
        self._states.append(state)

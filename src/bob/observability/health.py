"""Runtime health metric collection helpers."""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Any, Callable


@dataclass(frozen=True)
class HealthConfig:
    """Settings for periodic health summaries."""

    summary_interval_seconds: int = 300


@dataclass(frozen=True)
class HealthSnapshot:
    """Point-in-time runtime health summary."""

    uptime_seconds: float
    cpu_percent: float
    rss_bytes: int


class HealthMonitor:
    """Collect CPU, memory, and uptime metrics for local diagnostics."""

    def __init__(
        self,
        *,
        start_time: float | None = None,
        time_fn: Callable[[], float] = monotonic,
        process_factory: Callable[[], Any] | None = None,
    ) -> None:
        self._time_fn = time_fn
        self._start_time = start_time if start_time is not None else time_fn()
        self._process_factory = process_factory or self._default_process_factory
        self._process = self._process_factory()

    @staticmethod
    def _default_process_factory() -> Any:
        import psutil

        return psutil.Process()

    def snapshot(self) -> HealthSnapshot:
        """Return the current local runtime health snapshot."""
        cpu_percent = float(self._process.cpu_percent(interval=None))
        rss_bytes = int(self._process.memory_info().rss)
        uptime_seconds = max(0.0, self._time_fn() - self._start_time)
        return HealthSnapshot(
            uptime_seconds=uptime_seconds,
            cpu_percent=cpu_percent,
            rss_bytes=rss_bytes,
        )

    @staticmethod
    def format_snapshot(snapshot: HealthSnapshot) -> str:
        """Render a compact single-line summary for logging."""
        return (
            "health uptime_seconds="
            f"{snapshot.uptime_seconds:.1f} cpu_percent={snapshot.cpu_percent:.1f} "
            f"rss_bytes={snapshot.rss_bytes}"
        )

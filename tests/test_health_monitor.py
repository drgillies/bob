"""Tests for runtime health metric collection."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.observability import HealthMonitor


class FakeMemoryInfo:
    def __init__(self, rss: int) -> None:
        self.rss = rss


class FakeProcess:
    def __init__(self, cpu_percent: float, rss: int) -> None:
        self._cpu_percent = cpu_percent
        self._rss = rss

    def cpu_percent(self, interval=None) -> float:
        del interval
        return self._cpu_percent

    def memory_info(self) -> FakeMemoryInfo:
        return FakeMemoryInfo(self._rss)


def test_health_monitor_collects_snapshot_and_formats_summary() -> None:
    monitor = HealthMonitor(
        start_time=10.0,
        time_fn=lambda: 15.5,
        process_factory=lambda: FakeProcess(12.5, 42_000_000),
    )

    snapshot = monitor.snapshot()

    assert snapshot.uptime_seconds == 5.5
    assert snapshot.cpu_percent == 12.5
    assert snapshot.rss_bytes == 42_000_000
    assert "cpu_percent=12.5" in monitor.format_snapshot(snapshot)

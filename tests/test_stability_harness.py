"""Tests for long-session stability harness behavior."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.observability import StabilityHarness, StabilityHarnessConfig


class FakeClock:
    def __init__(self) -> None:
        self.current = 0.0

    def __call__(self) -> float:
        return self.current

    def sleep(self, seconds: float) -> None:
        self.current += seconds


class FakeHealthMonitor:
    def __init__(self, rss_values: list[int], cpu_values: list[float]) -> None:
        self._rss_values = list(rss_values)
        self._cpu_values = list(cpu_values)

    def snapshot(self):
        class Snapshot:
            def __init__(self, cpu_percent: float, rss_bytes: int) -> None:
                self.cpu_percent = cpu_percent
                self.rss_bytes = rss_bytes

        index = 0 if len(self._rss_values) == 1 else min(
            len(self._cpu_values) - 1,
            len(self._cpu_values) - len(self._cpu_values),
        )
        cpu = self._cpu_values.pop(0) if self._cpu_values else 0.0
        rss = self._rss_values.pop(0) if self._rss_values else self._rss_values[-1]
        return Snapshot(cpu, rss)


class SequenceHealthMonitor:
    def __init__(self, rss_values: list[int], cpu_values: list[float]) -> None:
        self._rss_values = rss_values
        self._cpu_values = cpu_values
        self._index = 0

    def snapshot(self):
        class Snapshot:
            def __init__(self, cpu_percent: float, rss_bytes: int) -> None:
                self.cpu_percent = cpu_percent
                self.rss_bytes = rss_bytes

        idx = min(self._index, len(self._rss_values) - 1)
        snapshot = Snapshot(self._cpu_values[idx], self._rss_values[idx])
        self._index += 1
        return snapshot


class FakeWatchdog:
    def __init__(self, polls: list[bool]) -> None:
        self.polls = list(polls)

    def poll(self) -> bool:
        if not self.polls:
            return False
        return self.polls.pop(0)


def test_stability_harness_collects_samples_and_recoveries() -> None:
    clock = FakeClock()
    harness = StabilityHarness(
        SequenceHealthMonitor(
            rss_values=[100, 110, 120],
            cpu_values=[5.0, 6.0, 7.0],
        ),
        StabilityHarnessConfig(
            duration_seconds=120,
            sample_interval_seconds=60,
            max_allowed_rss_drift_bytes=50,
        ),
        watchdog=FakeWatchdog([False, True, False]),
        time_fn=clock,
        sleep_fn=clock.sleep,
    )

    result = harness.run()

    assert result.sample_count == 3
    assert result.recovery_count == 1
    assert result.initial_rss_bytes == 100
    assert result.max_rss_bytes == 120
    assert result.rss_drift_bytes == 20
    assert result.passed is True


def test_stability_harness_writes_json_artifact(tmp_path: Path) -> None:
    clock = FakeClock()
    harness = StabilityHarness(
        SequenceHealthMonitor(
            rss_values=[100, 200],
            cpu_values=[5.0, 8.0],
        ),
        StabilityHarnessConfig(
            duration_seconds=60,
            sample_interval_seconds=60,
            max_allowed_rss_drift_bytes=20,
        ),
        time_fn=clock,
        sleep_fn=clock.sleep,
    )

    output_path = tmp_path / "artifacts" / "stability.json"
    result = harness.write_result(output_path)
    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert output_path.exists() is True
    assert payload["sample_count"] == result.sample_count
    assert payload["passed"] is False
    assert len(payload["samples"]) == 2

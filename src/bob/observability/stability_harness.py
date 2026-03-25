"""Long-session stability harness for repeatable local validation."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from time import monotonic, sleep
from typing import Callable, Protocol

from bob.observability.health import HealthMonitor, HealthSnapshot


class WatchdogLike(Protocol):
    """Minimal watchdog interface used by the stability harness."""

    def poll(self) -> bool:
        """Return True when a recovery was triggered."""


@dataclass(frozen=True)
class StabilityHarnessConfig:
    """Settings for a repeatable stability run."""

    duration_seconds: int = 14_400
    sample_interval_seconds: int = 60
    max_allowed_rss_drift_bytes: int = 134_217_728


@dataclass(frozen=True)
class StabilitySample:
    """One sampled health point during a stability run."""

    elapsed_seconds: float
    cpu_percent: float
    rss_bytes: int


@dataclass(frozen=True)
class StabilityRunResult:
    """Summary of a stability harness execution."""

    duration_seconds: int
    sample_interval_seconds: int
    sample_count: int
    recovery_count: int
    initial_rss_bytes: int
    final_rss_bytes: int
    max_rss_bytes: int
    rss_drift_bytes: int
    passed: bool
    samples: tuple[StabilitySample, ...] = field(default_factory=tuple)

    def to_json(self) -> str:
        """Serialize the result in a repo-friendly JSON shape."""
        payload = asdict(self)
        return json.dumps(payload, indent=2)


class StabilityHarness:
    """Run periodic health sampling and optional watchdog polling."""

    def __init__(
        self,
        health_monitor: HealthMonitor,
        config: StabilityHarnessConfig | None = None,
        *,
        watchdog: WatchdogLike | None = None,
        time_fn: Callable[[], float] = monotonic,
        sleep_fn: Callable[[float], None] = sleep,
    ) -> None:
        self._health_monitor = health_monitor
        self._config = config or StabilityHarnessConfig()
        self._watchdog = watchdog
        self._time_fn = time_fn
        self._sleep_fn = sleep_fn

    def run(self) -> StabilityRunResult:
        """Run the harness and return the collected stability summary."""
        if self._config.duration_seconds <= 0:
            raise ValueError("duration_seconds must be positive")
        if self._config.sample_interval_seconds <= 0:
            raise ValueError("sample_interval_seconds must be positive")

        start_time = self._time_fn()
        elapsed_seconds = 0.0
        recoveries = 0
        samples: list[StabilitySample] = []

        while elapsed_seconds < self._config.duration_seconds:
            snapshot = self._health_monitor.snapshot()
            elapsed_seconds = max(0.0, self._time_fn() - start_time)
            samples.append(
                StabilitySample(
                    elapsed_seconds=elapsed_seconds,
                    cpu_percent=snapshot.cpu_percent,
                    rss_bytes=snapshot.rss_bytes,
                )
            )

            if self._watchdog is not None and self._watchdog.poll():
                recoveries += 1

            if elapsed_seconds >= self._config.duration_seconds:
                break

            remaining = self._config.duration_seconds - elapsed_seconds
            self._sleep_fn(min(self._config.sample_interval_seconds, remaining))

        return _summarize_result(
            config=self._config,
            recoveries=recoveries,
            samples=samples,
        )

    def write_result(self, output_path: str | Path) -> StabilityRunResult:
        """Run the harness and write the JSON artifact to disk."""
        result = self.run()
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(result.to_json(), encoding="utf-8")
        return result


def _summarize_result(
    *,
    config: StabilityHarnessConfig,
    recoveries: int,
    samples: list[StabilitySample],
) -> StabilityRunResult:
    if not samples:
        raise ValueError("stability harness did not collect any samples")

    initial_rss = samples[0].rss_bytes
    final_rss = samples[-1].rss_bytes
    max_rss = max(sample.rss_bytes for sample in samples)
    rss_drift = max_rss - initial_rss
    passed = rss_drift <= config.max_allowed_rss_drift_bytes

    return StabilityRunResult(
        duration_seconds=config.duration_seconds,
        sample_interval_seconds=config.sample_interval_seconds,
        sample_count=len(samples),
        recovery_count=recoveries,
        initial_rss_bytes=initial_rss,
        final_rss_bytes=final_rss,
        max_rss_bytes=max_rss,
        rss_drift_bytes=rss_drift,
        passed=passed,
        samples=tuple(samples),
    )

"""Tests for audio watchdog stalled-stream recovery."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.audio import AudioWatchdog, AudioWatchdogConfig


class FakeAudioSource:
    def __init__(self, *, running: bool = True, recover_result: bool = True) -> None:
        self.running = running
        self.recover_result = recover_result
        self.recover_calls = 0

    def is_running(self) -> bool:
        return self.running

    def recover_stream(self) -> bool:
        self.recover_calls += 1
        return self.recover_result


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.current = start

    def __call__(self) -> float:
        return self.current


def test_audio_watchdog_does_not_trigger_before_timeout() -> None:
    clock = FakeClock(10.0)
    source = FakeAudioSource()
    watchdog = AudioWatchdog(
        source,
        AudioWatchdogConfig(no_audio_timeout_seconds=5.0),
        time_fn=clock,
    )

    watchdog.record_frame()
    clock.current = 14.0

    assert watchdog.poll() is False
    assert source.recover_calls == 0


def test_audio_watchdog_triggers_recovery_after_timeout() -> None:
    clock = FakeClock(10.0)
    source = FakeAudioSource()
    watchdog = AudioWatchdog(
        source,
        AudioWatchdogConfig(no_audio_timeout_seconds=5.0),
        time_fn=clock,
    )

    watchdog.record_frame()
    clock.current = 16.0

    assert watchdog.poll() is True
    assert source.recover_calls == 1
    assert watchdog.last_reset_time == 16.0


def test_audio_watchdog_ignores_non_running_source() -> None:
    clock = FakeClock(10.0)
    source = FakeAudioSource(running=False)
    watchdog = AudioWatchdog(source, time_fn=clock)
    watchdog.record_frame()
    clock.current = 20.0

    assert watchdog.poll() is False
    assert source.recover_calls == 0

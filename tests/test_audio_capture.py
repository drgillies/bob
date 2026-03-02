"""Tests for audio capture queueing and recovery behavior."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.audio.capture import AudioCaptureConfig, AudioCaptureError, AudioCaptureService


class FakeStream:
    def __init__(self, callback, fail_start: bool = False) -> None:
        self.callback = callback
        self.fail_start = fail_start
        self.started = False
        self.closed = False

    def start(self) -> None:
        if self.fail_start:
            raise RuntimeError("stream start failed")
        self.started = True

    def stop(self) -> None:
        self.started = False

    def close(self) -> None:
        self.closed = True


def test_audio_callback_queue_non_blocking_with_drop_oldest() -> None:
    config = AudioCaptureConfig(max_queue_size=1)
    service = AudioCaptureService(config=config, stream_factory=lambda **_: FakeStream(None))

    service._audio_callback(b"\x01\x00", 1, None, None)
    service._audio_callback(b"\x02\x00", 1, None, None)

    frame = service.read_frame(timeout_seconds=0.01)
    assert frame == b"\x02\x00"


def test_start_and_stop_stream() -> None:
    created = {}

    def fake_factory(**kwargs):
        stream = FakeStream(kwargs["callback"])
        created["stream"] = stream
        return stream

    service = AudioCaptureService(stream_factory=fake_factory)
    service.start()
    assert service.is_running()
    assert created["stream"].started is True

    service.stop()
    assert service.is_running() is False
    assert created["stream"].closed is True


def test_start_failure_raises_audio_capture_error() -> None:
    def fake_factory(**kwargs):
        return FakeStream(kwargs["callback"], fail_start=True)

    service = AudioCaptureService(stream_factory=fake_factory)
    try:
        service.start()
        assert False, "Expected AudioCaptureError"
    except AudioCaptureError:
        pass


def test_recover_stream_eventual_success() -> None:
    attempts = {"count": 0}

    def fake_factory(**kwargs):
        attempts["count"] += 1
        fail = attempts["count"] < 3
        return FakeStream(kwargs["callback"], fail_start=fail)

    config = AudioCaptureConfig(max_recovery_attempts=5, recovery_wait_seconds=0.0)
    service = AudioCaptureService(config=config, stream_factory=fake_factory)

    assert service.recover_stream() is True
    assert attempts["count"] == 3


def test_recover_stream_failure_after_max_attempts() -> None:
    def fake_factory(**kwargs):
        return FakeStream(kwargs["callback"], fail_start=True)

    config = AudioCaptureConfig(max_recovery_attempts=3, recovery_wait_seconds=0.0)
    service = AudioCaptureService(config=config, stream_factory=fake_factory)

    assert service.recover_stream() is False

"""Optional hardware test for microphone capture.

This test is skipped by default. Enable with:
    RUN_AUDIO_HW_TESTS=1
"""

from __future__ import annotations

import os
import sys
import time
import wave
from pathlib import Path

import pytest


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.audio.capture import AudioCaptureService


@pytest.mark.hardware
@pytest.mark.skipif(
    os.getenv("RUN_AUDIO_HW_TESTS") != "1",
    reason="Set RUN_AUDIO_HW_TESTS=1 to run microphone hardware tests.",
)
def test_audio_capture_can_write_wav(tmp_path: Path) -> None:
    service = AudioCaptureService()
    frames: list[bytes] = []

    service.start()
    try:
        end = time.time() + 2.0
        while time.time() < end:
            frame = service.read_frame(timeout_seconds=0.2)
            if frame is not None:
                frames.append(frame)
    finally:
        service.stop()

    assert frames, "No audio frames captured from microphone."

    output = tmp_path / "hardware_capture.wav"
    with wave.open(str(output), "wb") as wf:
        wf.setnchannels(service.config.channels)
        wf.setsampwidth(2)  # int16
        wf.setframerate(service.config.sample_rate_hz)
        wf.writeframes(b"".join(frames))

    assert output.exists()
    assert output.stat().st_size > 44  # WAV header size

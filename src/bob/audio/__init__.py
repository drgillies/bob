"""Audio capture and device discovery APIs."""

from bob.audio.capture import AudioCaptureConfig, AudioCaptureError, AudioCaptureService
from bob.audio.utterance import (
    EnergyVoiceActivityDetector,
    UtteranceRecorder,
    UtteranceRecorderConfig,
    VoiceActivityConfig,
)
from bob.audio.watchdog import AudioWatchdog, AudioWatchdogConfig

__all__ = [
    "AudioCaptureConfig",
    "AudioCaptureError",
    "AudioCaptureService",
    "AudioWatchdog",
    "AudioWatchdogConfig",
    "EnergyVoiceActivityDetector",
    "UtteranceRecorder",
    "UtteranceRecorderConfig",
    "VoiceActivityConfig",
]

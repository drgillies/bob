"""Wake-word detection interfaces and services."""

from bob.wakeword.openwakeword_detector import (
    OpenWakeWordConfig,
    OpenWakeWordDetector,
    WakeWordError,
)
from bob.wakeword.service import WakeDetectionEvent, WakeWordDetector

__all__ = [
    "OpenWakeWordConfig",
    "OpenWakeWordDetector",
    "WakeDetectionEvent",
    "WakeWordDetector",
    "WakeWordError",
]

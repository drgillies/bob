"""Wake-triggered utterance capture orchestration."""

from __future__ import annotations

from dataclasses import dataclass

from bob.audio import UtteranceRecorder
from bob.orchestrator.idle_loop import IdleLoopOrchestrator
from bob.stt import RecordedUtterance
from bob.wakeword import WakeDetectionEvent


@dataclass(frozen=True)
class WakeTriggeredUtterance:
    """Wake detection paired with the captured post-wake utterance."""

    detection: WakeDetectionEvent
    utterance: RecordedUtterance


class WakeTriggeredUtteranceController:
    """Capture one utterance immediately after wake detection."""

    def __init__(
        self,
        idle_loop: IdleLoopOrchestrator,
        recorder: UtteranceRecorder,
    ) -> None:
        self._idle_loop = idle_loop
        self._recorder = recorder

    def process_once(self) -> WakeTriggeredUtterance | None:
        """Run one wake check and capture the following utterance."""
        detection = self._idle_loop.poll_once()
        if detection is None:
            return None

        try:
            utterance = self._recorder.record()
        finally:
            self._idle_loop.acknowledge_trigger()

        return WakeTriggeredUtterance(detection=detection, utterance=utterance)

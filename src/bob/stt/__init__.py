"""Speech-to-text contracts and adapters."""

from bob.stt.service import (
    build_speech_to_text_service,
    RecordedUtterance,
    SpeechToTextConfigurationError,
    SpeechToTextError,
    SpeechToTextService,
    SpeechToTextTranscriptionError,
    TranscriptionResult,
    UtteranceStopReason,
    VoskSpeechToTextConfig,
    VoskSpeechToTextService,
)

__all__ = [
    "RecordedUtterance",
    "build_speech_to_text_service",
    "SpeechToTextConfigurationError",
    "SpeechToTextError",
    "SpeechToTextService",
    "SpeechToTextTranscriptionError",
    "TranscriptionResult",
    "UtteranceStopReason",
    "VoskSpeechToTextConfig",
    "VoskSpeechToTextService",
]

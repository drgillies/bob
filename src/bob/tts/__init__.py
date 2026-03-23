"""Text-to-speech interfaces and implementations."""

from bob.tts.pyttsx3_synthesizer import Pyttsx3SpeechSynthesizer
from bob.tts.service import SpeechSynthesizer, TTSConfig, TextToSpeechError

__all__ = [
    "Pyttsx3SpeechSynthesizer",
    "SpeechSynthesizer",
    "TTSConfig",
    "TextToSpeechError",
]

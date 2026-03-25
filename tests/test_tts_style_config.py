"""Tests for configurable voice tuning behavior."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.tts import Pyttsx3SpeechSynthesizer, TTSConfig


class FakeEngine:
    def __init__(self) -> None:
        self.properties: dict[str, object] = {}
        self.spoken: list[str] = []
        self.run_calls = 0
        self.voices: list[object] = []

    def setProperty(self, key: str, value: object) -> None:
        self.properties[key] = value

    def getProperty(self, key: str) -> object:
        if key == "voices":
            return self.voices
        raise KeyError(key)

    def say(self, text: str) -> None:
        self.spoken.append(text)

    def runAndWait(self) -> None:
        self.run_calls += 1


def test_tts_synthesizer_applies_volume_and_sentence_pause() -> None:
    engine = FakeEngine()
    synth = Pyttsx3SpeechSynthesizer(
        config=TTSConfig(
            speech_rate=140,
            voice_id="voice-1",
            volume=0.8,
            sentence_pause_ms=200,
        ),
        engine_factory=lambda: engine,
    )

    synth.speak("Hello. I am here.")

    assert engine.properties["rate"] == 140
    assert engine.properties["voice"] == "voice-1"
    assert engine.properties["volume"] == 0.8
    assert engine.spoken == ["Hello. .. I am here."]
    assert engine.run_calls == 1


def test_tts_synthesizer_prefers_explicit_voice_id_over_gender() -> None:
    class FakeVoice:
        def __init__(self, voice_id: str, gender: str) -> None:
            self.id = voice_id
            self.gender = gender

    engine = FakeEngine()
    engine.voices = [FakeVoice("voice-m1", "male")]

    synth = Pyttsx3SpeechSynthesizer(
        config=TTSConfig(
            speech_rate=140,
            voice_id="manual-voice",
            preferred_gender="male",
            volume=0.8,
            sentence_pause_ms=200,
        ),
        engine_factory=lambda: engine,
    )

    synth.speak("Hello.")

    assert engine.properties["voice"] == "manual-voice"

"""Tests for text-to-speech adapters."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bob.tts import Pyttsx3SpeechSynthesizer, TTSConfig, TextToSpeechError


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


def test_pyttsx3_synthesizer_applies_config_and_speaks() -> None:
    engine = FakeEngine()
    synth = Pyttsx3SpeechSynthesizer(
        config=TTSConfig(speech_rate=125, voice_id="voice-1"),
        engine_factory=lambda: engine,
    )

    synth.speak("Hello, I'm here.")

    assert engine.properties["rate"] == 125
    assert engine.properties["voice"] == "voice-1"
    assert engine.spoken == ["Hello, I'm here."]
    assert engine.run_calls == 1


def test_pyttsx3_synthesizer_init_raises_on_factory_failure() -> None:
    def failing_factory() -> FakeEngine:
        raise RuntimeError("engine init failed")

    try:
        Pyttsx3SpeechSynthesizer(engine_factory=failing_factory)
        assert False, "Expected TextToSpeechError"
    except TextToSpeechError:
        pass


def test_pyttsx3_synthesizer_prefers_gender_when_voice_id_missing() -> None:
    class FakeVoice:
        def __init__(self, voice_id: str, name: str, gender: str) -> None:
            self.id = voice_id
            self.name = name
            self.gender = gender

    engine = FakeEngine()
    engine.voices = [
        FakeVoice("voice-f1", "Alice", "female"),
        FakeVoice("voice-m1", "Bob", "male"),
    ]

    synth = Pyttsx3SpeechSynthesizer(
        config=TTSConfig(speech_rate=125, preferred_gender="male"),
        engine_factory=lambda: engine,
    )

    synth.speak("Hello, I'm here.")

    assert engine.properties["voice"] == "voice-m1"
    assert engine.spoken == ["Hello, I'm here."]
    assert engine.run_calls == 1

# TTS Engine Decision

## Decision

For the MVP, Bob stays on `pyttsx3` as the supported default TTS engine.

Piper remains a documented optional upgrade path, not the default runtime path.

## Why `pyttsx3` Stays the Default

1. It already works with the current codebase and runtime flow.
2. It is offline and uses the operating system voice stack on Windows.
3. It keeps install and packaging complexity low for an older target machine.
4. Its license profile is easier for the current source-run MVP than a GPL-based engine.

## Current Machine Limitation

On the current Windows machine, `pyttsx3` only exposes two installed SAPI voices:

1. `Microsoft Hazel Desktop - English (Great Britain)`
2. `Microsoft Zira Desktop - English (United States)`

Both are female voices.

That means Bob's `preferred_gender: "male"` setting is currently best-effort only. It will not produce a male voice unless the machine has one installed and visible through the local SAPI voice list.

## Piper Upgrade Path

Piper is the main upgrade candidate when Bob needs a higher-quality local voice.

Why Piper is attractive:

1. local/offline neural TTS
2. Windows wheels are available on PyPI
3. voice quality is meaningfully better than stock SAPI voices on many machines

Why Piper is not the MVP default:

1. active `piper-tts` distribution is `GPL-3.0-or-later`
2. that creates packaging and redistribution questions if Bob is later shipped as a bundled executable
3. it adds model-download and voice-asset management that the MVP does not yet need

## Supported MVP Position

Supported now:

1. `pyttsx3` with tuning via:
   - `tts.speech_rate`
   - `tts.voice_id`
   - `tts.preferred_gender`
   - `tts.volume`
   - `tts.sentence_pause_ms`
2. source-run workflow with `uv`
3. local voice inspection via `_testing.py tts-voices`

Not yet a supported default:

1. bundled Piper distribution
2. automatic Piper model download/install
3. committing to GPL obligations for packaged releases

## Upgrade Recommendation

If Bob later needs a real male voice or a more natural tone, the next step should be:

1. evaluate Piper as an opt-in local enhancement
2. keep it outside the default MVP dependency path unless distribution terms are accepted
3. add a separate engine adapter and setup flow instead of replacing `pyttsx3` in place

## Revisit Trigger

Revisit this decision when any of the following becomes true:

1. the target machine still lacks an acceptable built-in male voice
2. voice quality becomes a release blocker
3. Bob moves from source-run usage toward packaged distribution

# Risk Register

## Purpose

Track the main licensing, packaging, and operational risks for Bob's current stack.

This register is meant to stay actionable. Each item should have a mitigation direction and a next step, not just a warning.

## Risk Table

| ID | Area | Risk | Current Impact | Mitigation | Owner | Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | Wake word | `openWakeWord` code is open-source, but bundled pre-trained models carry non-commercial licensing constraints. | Medium | Do not assume bundled pre-trained models are safe for every distribution context. Treat model choice as a separate compliance decision from code choice. | Project | Before any packaged release, confirm whether Bob ships a model, requires local download, or needs a separately trained model. |
| R-002 | Wake word | `Hey Bob` may require custom wake-word model work if the chosen engine does not provide a turnkey phrase model. | High | Keep the wake-engine adapter boundary. Document the phrase as a product choice but keep engine support as an implementation constraint. | Project | Run a real target-machine wake benchmark and decide whether custom model work is required. |
| R-003 | Wake word | Porcupine requires an AccessKey and vendor validation path, which weakens strict offline-first behavior. | Medium | Keep Porcupine as an optional operational fallback, not the default engine. | Project | Only adopt Porcupine if the team explicitly accepts the connectivity and vendor dependency. |
| R-004 | TTS | `pyttsx3` depends on the local Windows SAPI voice inventory, which may not provide an acceptable male voice or consistent quality across machines. | Medium | Keep `pyttsx3` as the stable default, but document voice inspection and explicit `voice_id` selection where available. | Project | Validate the target machine voice inventory before final packaging decisions. |
| R-005 | TTS | Piper is the most practical voice-quality upgrade path, but `piper-tts` is GPL-3.0-or-later. | High | Keep Piper out of the default MVP path. Treat it as an opt-in upgrade until distribution obligations are reviewed. | Project | If Piper becomes necessary, perform a dedicated licensing and packaging review before bundling it. |
| R-006 | STT | `Vosk` is the selected default, but maintenance cadence on PyPI is slower than some alternatives. | Medium | Keep the STT adapter boundary and documented fallback path. Avoid tightly coupling orchestration to one engine. | Project | Recheck release health before release packaging or major upgrades. |
| R-007 | STT | `faster-whisper` is a viable fallback, but has heavier runtime and dependency costs for older hardware. | Medium | Keep it as a fallback, not the default. Require target-machine benchmarking before any switch. | Project | Benchmark on the actual old-hardware target if Vosk quality becomes insufficient. |
| R-008 | Packaging | Bob's startup/service story is documented, but the current `python -m bob` path still exits after bootstrap instead of running continuously. | High | Keep startup automation documented, but do not represent it as a fully operational always-on path yet. | Project | Add a persistent runtime entrypoint before calling startup automation production-ready. |
| R-009 | Privacy | Debug audio capture can leak raw microphone data if enabled casually. | Medium | Keep raw audio capture disabled by default and require explicit opt-in for disk writes. | Project | Preserve privacy gating in future manual helpers and debug workflows. |
| R-010 | Compliance | The intended “Patrick-like” direction could drift into unsafe imitation language if docs or future features get sloppy. | Medium | Keep persona guidance focused on pacing, phrasing, and tone rather than imitation. | Project | Review future TTS/persona work against `docs/persona-style.md` before merge. |

## Summary

Current highest-priority risks:

1. wake-word model/compliance ambiguity for `openWakeWord`
2. lack of proven real spoken wake-phrase validation for `Hey Bob`
3. Piper GPL implications if the project later wants a better bundled local voice
4. lack of a true always-on runtime entrypoint behind the documented startup flow

## Review Trigger

Update this register when any of the following changes:

1. wake engine changes
2. STT engine changes
3. TTS engine changes
4. Bob moves from source-run usage toward packaged distribution
5. a target-machine benchmark reveals a blocker or new operational constraint

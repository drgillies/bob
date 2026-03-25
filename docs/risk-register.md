# Risk Register

## Purpose

Track the main licensing, packaging, and operational risks for Bob's current stack.

This register is meant to stay actionable. Each item should have a mitigation direction and a next step, not just a warning.

## Risk Table

| ID | Area | Risk | Current Impact | Mitigation | Owner | Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | Wake word | `openWakeWord` code is open-source, but bundled pre-trained models carry non-commercial licensing constraints. | Medium | Do not assume bundled pre-trained models are safe for every distribution context. Treat model choice as a separate compliance decision from code choice. | Project | Before any packaged release, confirm whether Bob ships a model, requires local download, or needs a separately trained model. |
| R-002 | Wake word | `Hey Bob` is not available as a built-in `openWakeWord` model on the validated Windows path, so preserving the finalized phrase requires custom-model work. | High | Keep the wake-engine adapter boundary. Preserve `Hey Bob` as the product phrase, but treat support for that phrase as a deliberate model-delivery task rather than a given. | Project | Produce a compatible model artifact in Linux or Google Colab, place it at `models/wakeword/openwakeword/hey_bob.onnx`, then rerun the real spoken validation path on Windows. |
| R-002A | Wake word | Using `Yo homie` as a temporary engineering phrase unblocks real validation, but it can also accidentally blur the distinction between engineering validation and the actual product wake phrase. | Medium | Keep the temporary phrase clearly documented as engineering-only and avoid changing product-facing docs to present it as final behavior. | Project | Keep `yo_homie` limited to engineering validation, keep `Hey Bob` as the documented product phrase, and replace the temporary phrase once `hey_bob` model work is possible. |
| R-003 | Wake word | Switching to a vendor-key engine such as Porcupine would reduce implementation friction but would violate the current no-API/no-vendor-dependency constraint for Bob's core wake path. | High | Keep vendor-key wake engines out of the default path unless the project explicitly changes that constraint later. | Project | Hold Porcupine as a rejected option for the current constraint set and revisit only if the project changes its operating rules. |
| R-004 | TTS | `pyttsx3` depends on the local Windows SAPI voice inventory, which may not provide an acceptable male voice or consistent quality across machines. | Medium | Keep `pyttsx3` as the stable default, but document voice inspection and explicit `voice_id` selection where available. | Project | Validate the target machine voice inventory before final packaging decisions. |
| R-005 | TTS | Piper is the most practical voice-quality upgrade path, but `piper-tts` is GPL-3.0-or-later. | High | Keep Piper out of the default MVP path. Treat it as an opt-in upgrade until distribution obligations are reviewed. | Project | If Piper becomes necessary, perform a dedicated licensing and packaging review before bundling it. |
| R-006 | STT | `Vosk` is the selected default, but maintenance cadence on PyPI is slower than some alternatives. | Medium | Keep the STT adapter boundary and documented fallback path. Avoid tightly coupling orchestration to one engine. | Project | Recheck release health before release packaging or major upgrades. |
| R-007 | STT | `faster-whisper` is a viable fallback, but has heavier runtime and dependency costs for older hardware. | Medium | Keep it as a fallback, not the default. Require target-machine benchmarking before any switch. | Project | Benchmark on the actual old-hardware target if Vosk quality becomes insufficient. |
| R-008 | Packaging | Bob's startup/service story is documented, but the current `python -m bob` path still exits after bootstrap instead of running continuously. | High | Keep startup automation documented, but do not represent it as a fully operational always-on path yet. | Project | Add a persistent runtime entrypoint before calling startup automation production-ready. |
| R-009 | Privacy | Debug audio capture can leak raw microphone data if enabled casually. | Medium | Keep raw audio capture disabled by default and require explicit opt-in for disk writes. | Project | Preserve privacy gating in future manual helpers and debug workflows. |
| R-010 | Compliance | The intended "Patrick-like" direction could drift into unsafe imitation language if docs or future features get sloppy. | Medium | Keep persona guidance focused on pacing, phrasing, and tone rather than imitation. | Project | Review future TTS/persona work against `docs/persona-style.md` before merge. |

## Summary

Current highest-priority risks:

1. wake-word model/compliance ambiguity for `openWakeWord`
2. custom `Hey Bob` model work is still required before real spoken validation can pass on the preferred wake path
3. Piper GPL implications if the project later wants a better bundled local voice
4. lack of a true always-on runtime entrypoint behind the documented startup flow

## Review Trigger

Update this register when any of the following changes:

1. wake engine changes
2. STT engine changes
3. TTS engine changes
4. Bob moves from source-run usage toward packaged distribution
5. a target-machine benchmark reveals a blocker or new operational constraint


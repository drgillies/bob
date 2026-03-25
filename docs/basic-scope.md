# Bob - Basic Scope (Phase 0)

## 1. Vision

Build a lightweight voice assistant named **Bob** that runs on older computer hardware, listens continuously, and responds when called.

Bob's speaking style target:

- Friendly, slow, simple delivery
- Inspired by a "Patrick-like" tone (not an exact voice clone)

## 2. Primary Goals

1. Always-on local listening with low CPU usage.
2. Reliable wake phrase detection.
3. Fast response loop: hear -> transcribe -> decide -> speak.
4. Offline-first operation where possible.
5. Easy setup and maintenance on old machines.

## 3. Non-Goals (for MVP)

1. Full smart-home control.
2. Complex personality simulation.
3. Perfect human-level conversation.
4. Exact imitation of copyrighted character voices.
5. Cloud-dependent core behavior.

## 4. MVP Capabilities

1. Wake phrase support (for example: "Hey Bob").
2. Speech-to-text for short commands/questions.
3. Intent handling for a small command set:
   - Time/date
   - Basic status ("Are you there?", "What can you do?")
   - Local actions (open app, play/pause media) if available
4. Text-to-speech output with configurable voice profile:
   - Lower pitch
   - Slower pace
   - Relaxed, friendly tone
5. Basic conversation memory for current session only.
6. Local logging for debugging.

## 5. Target Environment

- Older desktop/laptop hardware.
- Windows-first deployment (can later expand to Linux).
- Minimum viable assumptions:
  - 4+ GB RAM
  - Dual-core CPU
  - Built-in or USB microphone
  - Speakers or headset

## 6. Quality Targets (MVP)

1. Wake word false trigger rate low enough for normal room use.
2. Typical response start within 1-3 seconds after user stops speaking.
3. Recover cleanly from transient audio errors without reboot.
4. Runs for long sessions (4+ hours target) without memory leaks or crashes.
5. Default runtime should remain usable on target hardware without sustained high CPU.

## 7. System Scope (High Level)

1. Audio Input Layer
   - Mic capture
   - Noise gate / VAD (voice activity detection)
2. Wake Word Layer
   - Lightweight keyword model
3. STT Layer
   - Local speech recognition for short utterances
4. Orchestrator
   - Route input -> intent -> response
5. Skills/Commands Layer
   - Small pluggable command handlers
6. TTS Layer
   - Adjustable "Patrick-like" style parameters
7. Observability
   - Logs + basic health stats

## 8. Risks and Constraints

1. Old hardware may struggle with larger models.
2. Microphone quality/noise will heavily affect accuracy.
3. "Character-like" voice must stay stylistic, not cloned.
4. Always-listening mode requires careful CPU and privacy design.

## 9. Privacy and Safety Baseline

1. Default to local processing and local logs.
2. Provide a clear mute toggle / push-to-talk fallback.
3. Avoid storing raw audio unless explicitly enabled.
4. Add visible indicator when Bob is actively listening/processing.

## 10. Milestones

1. Milestone 1 - Skeleton
   - Audio loop + wake phrase + simple TTS reply
2. Milestone 2 - Core MVP
   - STT + 5-10 core intents + error handling
3. Milestone 3 - Reliability
   - Logging, config file, startup service mode
4. Milestone 4 - Personality Pass
   - Voice tuning, prompt tuning, response style polish

## 11. Milestone Exit Criteria

1. Milestone 1 exits when:
   - Wake phrase can trigger a deterministic local response.
   - Audio capture and playback work on the target machine.
2. Milestone 2 exits when:
   - MVP command list is implemented for core intents.
   - Unknown intent fallback is in place.
   - Basic error handling prevents crash-on-failure for common errors.
3. Milestone 3 exits when:
   - Configuration loading is centralized.
   - Logging and health signals are available for debugging.
   - Long-session stability is verified with a repeatable validation run.
4. Milestone 4 exits when:
   - Voice style settings are configurable and documented.
   - Response style is consistent with the target persona constraints.

## 12. Open Decisions

1. Final wake phrase.
2. Offline model stack (wake word/STT/TTS libraries).
3. Whether Bob should support internet fallback for harder queries.
4. Service mode: auto-start on boot or manual run.
5. Minimum acceptable hardware profile after first benchmark pass.
6. Telemetry depth for non-sensitive local health metrics.

## 13. Configuration and Secrets Baseline

1. Non-sensitive runtime settings belong in `config/settings.local.json`.
2. Secrets (API keys/tokens/credentials) belong only in `.env`.
3. `config/settings.example.json` and `.env.example` are templates for shared setup.
4. No secrets should ever be committed to git.

## 14. Repository Structure Baseline

1. Runtime implementation code belongs under `src/`.
2. Automated tests belong under `tests/` and should mirror `src/` layout.
3. Docs under `docs/`, standards under `standards/`, planning under `planning/`.

## 15. Deliverables Status

Completed:
1. `docs/architecture.md` with module boundaries and data flow.
2. `docs/mvp-command-list.md` with initial supported phrases/intents.
3. `docs/setup-target-machine.md` for old-computer install steps.
4. `docs/benchmark-baseline.md` with wake-word and STT spike findings plus benchmark procedures.
5. `docs/error-handling-policy.md` defining retry/recover/fail behavior by component and session-memory privacy rules.
6. `docs/service-mode.md` documenting the MVP startup and packaging strategy.
7. `docs/persona-style.md` documenting response tone and voice tuning guidance.

Next:
1. Extend `docs/benchmark-baseline.md` with target-machine CPU/memory/latency measurements.

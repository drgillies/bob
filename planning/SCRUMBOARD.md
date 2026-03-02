# Scrum Board

Execution board derived from `docs/deep-research-report.md`.

---

## Status Legend

- `Backlog`: scoped but not prioritized for current execution
- `To Do`: ready to start
- `In Progress`: currently being executed
- `In Review`: implementation complete, awaiting validation
- `Done`: accepted and verified

---

## Task Card Template

```md
### TASK-###: <Short Action Title>
- [ ] Status: Backlog | To Do | In Progress | In Review | Done
- Size: S | M | L
- Objective:
- Business Value:
- Inputs/Context:
- Target Files/Paths:
- Implementation Notes:
- Constraints/Standards:
- Tests Required:
- Done Criteria:
- Deliverable Format:
```

---

## Dependency-Critical Path (With Size)

1. `TASK-001` (S): Convert deep research into execution baseline docs
2. `TASK-002` (M): Repository skeleton + runnable entrypoint
3. `TASK-003` (S): Dependency baseline + audio device listing smoke
4. `TASK-004` (M): Audio capture MVP with recovery
5. `TASK-005` (M): Wake-word spike and decision
6. `TASK-006` (M): Wake phrase integration in idle loop
7. `TASK-007` (S): Deterministic TTS response
8. `TASK-008` (S): State indicator and mute control
9. `TASK-009` (M): STT engine spike and decision
10. `TASK-010` (M): Utterance recording with end-of-speech VAD
11. `TASK-011` (L): STT adapter + default implementation
12. `TASK-012` (L): Intent router and core intents
13. `TASK-013` (M): Local actions framework + open-app skill
14. `TASK-014` (M): Session memory + error-handling policy
15. `TASK-015` (M): Centralized config loader + validation
16. `TASK-016` (M): Logging + health metrics + watchdog
17. `TASK-017` (M): Long-session stability harness + benchmark baseline
18. `TASK-018` (S): Service mode decision + packaging strategy
19. `TASK-019` (S): Privacy mode hardening
20. `TASK-020` (M): Voice tuning + response style guide
21. `TASK-021` (S): TTS engine decision and optional upgrade path
22. `TASK-022` (S): Wake phrase finalization + compliance notes
23. `TASK-023` (S): Licensing and risk register

Notes:
- `S`: <= 0.5 day
- `M`: 1-2 days
- `L`: 3+ days or high uncertainty

---

## Backlog

### TASK-004: M1 audio capture MVP with recovery
- [ ] Status: Backlog
- Size: M
- Objective: Implement continuous mic frame capture using `sounddevice` with queue-based callback and stream recovery.
- Business Value: Enables low-latency always-on listening on older hardware.
- Inputs/Context: `docs/deep-research-report.md` (M1-03), `docs/architecture.md`.
- Target Files/Paths: `src/audio/`, `src/orchestrator/`, `tests/`.
- Implementation Notes: Keep callback lightweight; recover from unplug/replug within 30s.
- Constraints/Standards: `standards/code-standards.md`, `standards/style-guides.md`.
- Tests Required: Unit test for queueing path; integration smoke for capture start/stop and recovery.
- Done Criteria: Continuous capture works; callback non-blocking; recovery path verified.
- Deliverable Format: Code + test evidence + short validation log.

### TASK-005: M1 wake-word spike and decision
- [ ] Status: Backlog
- Size: M
- Objective: Evaluate openWakeWord, Porcupine, and one fallback; choose primary + fallback engine.
- Business Value: De-risks the always-on constraint and idle CPU target.
- Inputs/Context: `docs/deep-research-report.md` (M1-04), `docs/basic-scope.md`.
- Target Files/Paths: `docs/benchmark-baseline.md` or `planning/phase0-wakeword-spike.md`.
- Implementation Notes: Capture install friction, idle CPU, false-trigger observations, offline caveats/licensing.
- Constraints/Standards: Offline-first requirement; explicit licensing notes.
- Tests Required: Benchmark script/steps documented and reproducible.
- Done Criteria: Primary/fallback wake-word decision recorded with rationale.
- Deliverable Format: Spike report + decision record.

### TASK-006: M1 wake phrase integration in idle loop
- [ ] Status: Backlog
- Size: M
- Objective: Integrate wake detector with state machine (IDLE -> TRIGGERED) and debouncing.
- Business Value: Core activation path for Bob.
- Inputs/Context: `docs/deep-research-report.md` (M1-05), `docs/architecture.md`.
- Target Files/Paths: `src/wakeword/`, `src/orchestrator/`, `tests/`.
- Implementation Notes: Log false triggers during manual 15-minute run.
- Constraints/Standards: Keep idle CPU low; no full STT in idle loop.
- Tests Required: Unit tests for debouncing/state transitions; integration wake trigger test.
- Done Criteria: Wake phrase reliably triggers once per utterance; false triggers logged.
- Deliverable Format: Code + test output + manual observation note.

### TASK-007: M1 deterministic TTS response
- [ ] Status: Backlog
- Size: S
- Objective: On wake trigger, produce deterministic reply and return to IDLE.
- Business Value: Completes first end-to-end feedback loop.
- Inputs/Context: `docs/deep-research-report.md` (M1-06).
- Target Files/Paths: `src/tts/`, `src/orchestrator/`, `config/settings.example.json`, `tests/`.
- Implementation Notes: Default to `pyttsx3`; speech rate configurable.
- Constraints/Standards: Offline-first; configurable behavior in settings.
- Tests Required: Integration test for trigger->speak->idle flow.
- Done Criteria: Deterministic phrase spoken and state reset verified.
- Deliverable Format: Code + config update + test evidence.

### TASK-008: M1 state indicator and mute control
- [ ] Status: Backlog
- Size: S
- Objective: Expose and log IDLE/LISTENING/PROCESSING/SPEAKING and config-based mute mode.
- Business Value: Improves operability and privacy confidence.
- Inputs/Context: `docs/deep-research-report.md` (M1-07), `docs/basic-scope.md` safety baseline.
- Target Files/Paths: `src/orchestrator/`, `src/observability/`, `config/settings.example.json`, `tests/`.
- Implementation Notes: Mute disables wake processing while process remains running.
- Constraints/Standards: No secret logging; state transitions must be visible.
- Tests Required: Unit tests for mute behavior and state transition logging.
- Done Criteria: States are clearly observable; mute behavior works as documented.
- Deliverable Format: Code + test evidence + docs note.

### TASK-009: M2 STT engine spike and decision
- [ ] Status: Backlog
- Size: M
- Objective: Compare Vosk vs whisper.cpp/faster-whisper on target hardware and choose default + fallback.
- Business Value: Controls latency and memory risk before deeper implementation.
- Inputs/Context: `docs/deep-research-report.md` (M2-01).
- Target Files/Paths: `docs/benchmark-baseline.md`.
- Implementation Notes: Measure latency, CPU, memory, install complexity.
- Constraints/Standards: Offline-first; target hardware constraints.
- Tests Required: Benchmark runs with reproducible command set.
- Done Criteria: STT choice documented with measured tradeoffs.
- Deliverable Format: Benchmark section + decision note.

### TASK-010: M2 utterance recording with end-of-speech VAD
- [ ] Status: Backlog
- Size: M
- Objective: Record post-wake utterances and stop on end-of-speech with timeout fallback.
- Business Value: Enables reliable STT input and faster response loop.
- Inputs/Context: `docs/deep-research-report.md` (M2-02).
- Target Files/Paths: `src/audio/`, `src/stt/`, `src/orchestrator/`, `tests/`.
- Implementation Notes: Include trailing buffer and silence timeout.
- Constraints/Standards: Stop within ~0.5-1.0s after user speech in typical conditions.
- Tests Required: Integration tests for VAD-stop and timeout scenarios.
- Done Criteria: End-of-speech and timeout behavior validated.
- Deliverable Format: Code + test logs.

### TASK-011: M2 STT adapter + default implementation
- [ ] Status: Backlog
- Size: L
- Objective: Add STT interface and default engine implementation with typed error handling.
- Business Value: Decouples engine choice and reduces vendor/library lock-in.
- Inputs/Context: `docs/deep-research-report.md` (M2-03, M2-04), `docs/architecture.md`.
- Target Files/Paths: `src/stt/`, `src/data/model/`, `src/orchestrator/`, `tests/`.
- Implementation Notes: `transcribe(...) -> text + metadata`; fallback selection via config.
- Constraints/Standards: Offline mode supported; no orchestrator crash on STT errors.
- Tests Required: Unit tests for adapter contract and error paths.
- Done Criteria: Default STT works; fallback switching path exists.
- Deliverable Format: Code + contract tests + config update.

### TASK-012: M2 intent router and core intents
- [ ] Status: Backlog
- Size: L
- Objective: Implement deterministic intent router with exact + fuzzy matching and core intents.
- Business Value: Delivers usable assistant behaviors for MVP command set.
- Inputs/Context: `docs/deep-research-report.md` (M2-05, M2-06), `docs/mvp-command-list.md`.
- Target Files/Paths: `src/skills/`, `src/orchestrator/`, `src/data/model/`, `tests/`.
- Implementation Notes: Include unknown-intent fallback response path.
- Constraints/Standards: Keep behavior deterministic for MVP.
- Tests Required: Unit tests for parsing/matching and intent handlers.
- Done Criteria: All commands in `docs/mvp-command-list.md` implemented and tested.
- Deliverable Format: Code + tests + updated command list notes if needed.

### TASK-013: M2 local actions framework and Windows open-app skill
- [ ] Status: Backlog
- Size: M
- Objective: Add pluggable skills framework and implement `open <app>` with config mapping.
- Business Value: Enables first practical local action capability.
- Inputs/Context: `docs/deep-research-report.md` (M2-07, M2-08).
- Target Files/Paths: `src/skills/`, `config/settings.example.json`, `tests/`, `docs/mvp-command-list.md`.
- Implementation Notes: Feature-flag optional media controls; graceful unsupported response.
- Constraints/Standards: No privileged keylogging behavior by default.
- Tests Required: Integration tests for known app, missing app, disabled skill.
- Done Criteria: Open-app flow works with useful errors and config toggles.
- Deliverable Format: Code + config docs + tests.

### TASK-014: M2 session memory and error-handling policy
- [ ] Status: Backlog
- Size: M
- Objective: Implement session-only memory and create `docs/error-handling-policy.md`.
- Business Value: Improves conversational continuity and runtime resilience.
- Inputs/Context: `docs/deep-research-report.md` (M2-10, M2-11), `docs/basic-scope.md`.
- Target Files/Paths: `src/orchestrator/`, `src/data/model/`, `docs/error-handling-policy.md`, `tests/`.
- Implementation Notes: Memory cleared on restart; define retry/reset/fail strategy per component.
- Constraints/Standards: No raw audio persistence by default.
- Tests Required: Unit tests for memory lifecycle and error recovery paths.
- Done Criteria: Policy doc exists; transient failures recover to IDLE.
- Deliverable Format: Doc + code + tests.

### TASK-015: M3 centralized config loader and schema validation
- [ ] Status: Backlog
- Size: M
- Objective: Implement config loading with `settings.local.json` overrides and `.env` secrets only.
- Business Value: Safe, consistent runtime behavior across machines.
- Inputs/Context: `docs/deep-research-report.md` (M3-01), `docs/configuration.md`.
- Target Files/Paths: `src/config/`, `config/settings.example.json`, `.env.example`, `tests/`.
- Implementation Notes: Consider Pydantic Settings or lightweight typed validator.
- Constraints/Standards: `.env` secrets-only rule; no secrets in logs.
- Tests Required: Unit tests for merge order, validation, and missing/invalid keys.
- Done Criteria: Config load path centralized and documented.
- Deliverable Format: Code + tests + docs update.

### TASK-016: M3 logging, health metrics, and watchdog
- [ ] Status: Backlog
- Size: M
- Objective: Add rotating logs, health metrics, and no-audio watchdog reset.
- Business Value: Supports long-run debugging and uptime.
- Inputs/Context: `docs/deep-research-report.md` (M3-02, M3-03).
- Target Files/Paths: `src/observability/`, `src/audio/`, `src/orchestrator/`, `config/settings.example.json`, `tests/`.
- Implementation Notes: Emit state transitions, timings, and periodic psutil summary.
- Constraints/Standards: Structured actionable logs; avoid duplicate exception spam.
- Tests Required: Unit tests for logger config/watchdog triggers.
- Done Criteria: Rotating logs + health summaries + stream reset behavior verified.
- Deliverable Format: Code + test evidence + sample logs.

### TASK-017: M3 long-session stability harness and baseline benchmark
- [ ] Status: Backlog
- Size: M
- Objective: Create repeatable 4+ hour stability harness and benchmark baseline doc.
- Business Value: Proves MVP reliability on constrained hardware.
- Inputs/Context: `docs/deep-research-report.md` (M3-04), `docs/basic-scope.md`.
- Target Files/Paths: `docs/benchmark-baseline.md`, `src/` test-mode script, `tests/`.
- Implementation Notes: Include pass/fail thresholds for memory drift and crash-free run.
- Constraints/Standards: Reproducible procedure on target machine.
- Tests Required: Harness run procedure + output artifact checks.
- Done Criteria: Baseline documented and repeatable with pass criteria.
- Deliverable Format: Benchmark doc + harness script.

### TASK-018: M3 service mode decision and packaging strategy
- [ ] Status: Backlog
- Size: S
- Objective: Decide and document Windows startup/service mode and packaging approach.
- Business Value: Enables dependable deployment and operation.
- Inputs/Context: `docs/deep-research-report.md` (M3-05, M3-06), `docs/setup-target-machine.md`.
- Target Files/Paths: `docs/service-mode.md`, `docs/setup-target-machine.md`, `README.md`.
- Implementation Notes: Evaluate NSSM vs pywin32 service; source-run vs PyInstaller.
- Constraints/Standards: Include install/uninstall reproducible steps.
- Tests Required: Manual dry-run of chosen install/uninstall process.
- Done Criteria: Decision and operational steps are documented and tested once.
- Deliverable Format: Decision doc + updated setup steps.

### TASK-019: M3 privacy mode hardening
- [ ] Status: Backlog
- Size: S
- Objective: Enforce no raw audio storage by default with explicit debug opt-in.
- Business Value: Protects user privacy and reduces risk.
- Inputs/Context: `docs/deep-research-report.md` (M3-07), `docs/basic-scope.md`.
- Target Files/Paths: `src/config/`, `src/audio/`, `docs/configuration.md`, `tests/`.
- Implementation Notes: Add clear warning logs when debug audio capture is enabled.
- Constraints/Standards: Default secure behavior.
- Tests Required: Tests for default-off and explicit-on behavior.
- Done Criteria: Privacy behavior implemented and documented.
- Deliverable Format: Code + tests + doc updates.

### TASK-020: M4 voice tuning and response style guide
- [ ] Status: Backlog
- Size: M
- Objective: Add voice tuning config and define consistent response-style rules.
- Business Value: Delivers intended persona while staying legally safe.
- Inputs/Context: `docs/deep-research-report.md` (M4-01, M4-03, M4-05), `docs/basic-scope.md`.
- Target Files/Paths: `config/settings.example.json`, `docs/persona-style.md`, `src/tts/`.
- Implementation Notes: Short/friendly phrasing, slower delivery; no character voice cloning.
- Constraints/Standards: Compliance note required.
- Tests Required: Manual QA checklist for style consistency.
- Done Criteria: Style guide published and config controls wired.
- Deliverable Format: Doc + config + implementation notes.

### TASK-021: M4 TTS engine decision and optional upgrade path
- [ ] Status: Backlog
- Size: S
- Objective: Decide pyttsx3-only vs optional Piper path with licensing implications documented.
- Business Value: Balances voice quality, CPU, and distribution risk.
- Inputs/Context: `docs/deep-research-report.md` (M4-02).
- Target Files/Paths: `docs/persona-style.md`, `README.md`, `docs/setup-target-machine.md`.
- Implementation Notes: Capture GPL implications and support matrix by deployment mode.
- Constraints/Standards: Explicit legal/distribution caveats must be documented.
- Tests Required: Install/run sanity for chosen default engine.
- Done Criteria: TTS strategy decision recorded and docs aligned.
- Deliverable Format: Decision note + doc updates.

### TASK-022: M4 wake phrase finalization and compliance notes
- [ ] Status: Backlog
- Size: S
- Objective: Finalize wake phrase and operational notes for chosen wake engine.
- Business Value: Locks user-facing activation behavior for MVP release.
- Inputs/Context: `docs/deep-research-report.md` (M4-04), benchmark results from wake-word tasks.
- Target Files/Paths: `docs/mvp-command-list.md`, `docs/persona-style.md`, `config/settings.example.json`.
- Implementation Notes: Include false-trigger rationale and fallback operational caveats.
- Constraints/Standards: Offline-first expectations and licensing constraints documented.
- Tests Required: 1-hour false-trigger observation protocol run and recorded.
- Done Criteria: Wake phrase + rationale + caveats documented.
- Deliverable Format: Updated docs + test observation summary.

### TASK-023: Cross-cutting licensing and risk register
- [ ] Status: Backlog
- Size: S
- Objective: Create explicit licensing and operational risk register for selected stack.
- Business Value: Prevents late-stage legal/distribution blockers.
- Inputs/Context: `docs/deep-research-report.md` (licensing and risk sections).
- Target Files/Paths: `docs/risk-register.md`, `README.md`.
- Implementation Notes: Track openWakeWord model license, Piper GPL, Porcupine key dependency.
- Constraints/Standards: Keep actionable mitigations and owner/next-action fields.
- Tests Required: Documentation review checklist.
- Done Criteria: Risk register exists and is referenced by README.
- Deliverable Format: New doc + README reference.

---

## To Do

### TASK-003: M1 dependency baseline + audio device listing smoke
- [ ] Status: To Do
- Size: S
- Objective: Pin initial dependency set and add audio device listing script.
- Business Value: Confirms target-machine audio compatibility early.
- Inputs/Context: `docs/deep-research-report.md` (M1-02), `docs/setup-target-machine.md`.
- Target Files/Paths: `requirements.txt`, `src/audio/`, `docs/setup-target-machine.md`, `tests/`.
- Implementation Notes: Include `sounddevice` install notes and device enumeration command.
- Constraints/Standards: Reproducible install on Windows.
- Tests Required: Run smoke script and capture output on target machine.
- Done Criteria: Dependencies pinned and audio devices listed successfully.
- Deliverable Format: Updated deps/docs + smoke command evidence.

---

## In Progress

No active tasks.

---

## In Review

No tasks currently in review.

---

## Done

### TASK-001: Convert deep research into execution baseline docs
- [x] Status: Done
- Size: S
- Completed: 2026-03-02
- Outcome: Scope and board were aligned to deep research with dependency order and size estimates.
- Verification: Ticket file `planning/tickets/TASK-001.md` completed and board updated.
- Ticket Record: `planning/tickets/TASK-001.md`

### TASK-002: M1 repository skeleton + runnable entrypoint
- [x] Status: Done
- Size: M
- Completed: 2026-03-02
- Outcome: Implemented `src/bob` package skeleton with runnable `python -m bob` entrypoint.
- Verification: `python -m bob --version` -> `0.1.0`; `python -m bob` -> bootstrap message; `pytest -q` -> 2 passed.
- Ticket Record: `planning/tickets/TASK-002.md`

---

## Usage Notes

- Move tasks between sections instead of duplicating them.
- Keep task IDs stable and update only status/details.
- Add links to PRs/commits under the relevant task when work starts.
- Recommended next ticket: `TASK-003`.

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
- Manual Tests:
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

### TASK-018: M3 service mode decision and packaging strategy
- [ ] Status: Backlog
- Size: M
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

No tasks currently in To Do.

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

### TASK-003: M1 dependency baseline + audio device listing smoke
- [x] Status: Done
- Size: S
- Completed: 2026-03-02
- Outcome: Standardized a `uv`-first dependency workflow and added audio device listing smoke command.
- Verification: `uv run --with-requirements requirements.txt -- python -m bob --version` -> `0.1.0`; `--list-audio-devices` printed detected devices; `uv run ... pytest -q` -> 3 passed.
- Ticket Record: `planning/tickets/TASK-003.md`

### TASK-004: M1 audio capture MVP with recovery
- [x] Status: Done
- Size: M
- Completed: 2026-03-02
- Outcome: Added `AudioCaptureService` with queue-based callback capture, safe start/stop, and stream recovery retries.
- Verification: `uv run --with-requirements requirements.txt -- python -m pytest -q tests/test_audio_capture.py` -> 5 passed; `uv run --with-requirements requirements.txt -- python -m pytest -q` -> 12 passed, 1 skipped (hardware test skip-by-default).
- Ticket Record: `planning/tickets/TASK-004.md`

### TASK-005: M1 wake-word spike and decision
- [x] Status: Done
- Size: M
- Completed: 2026-03-23
- Outcome: Documented wake-word engine recommendation, fallback path, and reproducible benchmark procedure for target-machine validation.
- Verification: `openwakeword` import passed but model init was not turnkey; `pvporcupine` import passed; `pocketsphinx` import and `Decoder()` initialization passed.
- Ticket Record: `planning/tickets/TASK-005.md`

### TASK-006: M1 wake phrase integration in idle loop
- [x] Status: Done
- Size: M
- Completed: 2026-03-23
- Outcome: Added a wake-word adapter boundary, an optional `openWakeWord` detector wrapper, and idle-loop orchestration with debounced state transitions.
- Verification: `uv run --with-requirements requirements.txt -- python -m pytest -q tests/test_idle_loop_orchestrator.py tests/test_openwakeword_detector.py` -> 10 passed; `uv run --with-requirements requirements.txt -- python -m pytest -q` -> 22 passed, 1 skipped; `_testing.py wake-idle-loop` produced `IDLE -> TRIGGERED -> IDLE`.
- Ticket Record: `planning/tickets/TASK-006.md`

### TASK-007: M1 deterministic TTS response
- [x] Status: Done
- Size: S
- Completed: 2026-03-23
- Outcome: Added `pyttsx3`-backed deterministic speech output after wake trigger and returned Bob to `IDLE`.
- Verification: `uv run --with-requirements requirements.txt -- python -m pytest -q tests/test_tts_synthesizer.py tests/test_response_flow.py` -> 4 passed; `uv run --with-requirements requirements.txt -- python -m pytest -q` -> 26 passed, 1 skipped; `_testing.py deterministic-response --mode tts` audibly spoke `Hello, I'm here.` and returned to `IDLE`.
- Ticket Record: `planning/tickets/TASK-007.md`

### TASK-008: M1 state indicator and mute control
- [x] Status: Done
- Size: S
- Completed: 2026-03-23
- Outcome: Added observable assistant state tracking and mute-aware response control that suppresses wake handling without shutting down the runtime.
- Verification: `uv run --with-requirements requirements.txt -- python -m pytest -q tests/test_state_tracker.py tests/test_mute_control.py` -> 5 passed; `uv run --with-requirements requirements.txt -- python -m pytest -q` -> 31 passed, 1 skipped; `_testing.py mute-response` showed `IDLE -> TRIGGERED -> SPEAKING -> IDLE` and `_testing.py mute-response --muted` stayed at `IDLE`.
- Ticket Record: `planning/tickets/TASK-008.md`

### TASK-009: M2 STT engine spike and decision
- [x] Status: Done
- Size: M
- Completed: 2026-03-23
- Outcome: Documented the STT default recommendation (`Vosk`), fallback (`faster-whisper`), and native-build alternative (`whisper.cpp`) with reproducible benchmark steps.
- Verification: Local Windows feasibility checks showed `vosk`, `faster-whisper`, and `whispercpp` all imported successfully; `Vosk` was recorded as the lowest-friction default path.
- Ticket Record: `planning/tickets/TASK-009.md`

### TASK-010: M2 utterance recording with end-of-speech VAD
- [x] Status: Done
- Size: M
- Completed: 2026-03-24
- Outcome: Added an energy-based utterance recorder with trailing silence retention, typed stop reasons, and wake-to-utterance orchestration ready for STT integration.
- Verification: `python -m pytest -q` -> 36 passed, 1 skipped; manual `_testing.py utterance-record` validated both timeout-with-silence and end-of-speech-with-audio behavior.
- Ticket Record: `planning/tickets/TASK-010.md`

### TASK-011: M2 STT adapter + default implementation
- [x] Status: Done
- Size: L
- Completed: 2026-03-24
- Outcome: Added a typed STT service boundary, default Vosk adapter, service factory, and wake-to-transcription orchestration built on the utterance recorder.
- Verification: `python -m pytest -q` -> 47 passed, 1 skipped; `python _testing.py stt-fake` produced a deterministic transcript; real adapter checks via `_testing.py stt-vosk` transcribed `_stt_sample.wav` as `what time is it` and user-recorded `my_test.wav` without crashing.
- Ticket Record: `planning/tickets/TASK-011.md`

### TASK-012: M2 intent router and core intents
- [x] Status: Done
- Size: L
- Completed: 2026-03-24
- Outcome: Added deterministic text normalization, intent routing, core MVP handlers, and transcription-to-intent orchestration for time/date/status/capability/fallback flows.
- Verification: `python -m pytest -q` -> 59 passed, 1 skipped; `_testing.py intent-fake --text "what time is it"` returned `GET_TIME`; `_testing.py intent-fake --text "what date is it"` and `"what day is it"` returned `GET_DATE`.
- Ticket Record: `planning/tickets/TASK-012.md`

### TASK-013: M2 local actions framework and Windows open-app skill
- [x] Status: Done
- Size: M
- Completed: 2026-03-24
- Outcome: Added a config-driven local action layer and wired `open <app>` to a Windows-safe launcher with known/unknown/disabled behavior.
- Verification: `python -m pytest -q` -> 68 passed, 1 skipped; `_testing.py open-app-fake --app calculator` resolved `calc.exe`; `_testing.py open-app-real --app calculator` successfully opened Calculator.
- Ticket Record: `planning/tickets/TASK-013.md`

### TASK-014: M2 session memory and error-handling policy
- [x] Status: Done
- Size: M
- Completed: 2026-03-24
- Outcome: Added runtime-only session memory, resilient recovery paths that return Bob to `IDLE`, and a component-level error-handling policy doc.
- Verification: `python -m pytest -q` -> 75 passed, 1 skipped; `_testing.py session-runtime-fake` recorded the in-memory turn state; `_testing.py session-runtime-fake --tts-fail` recorded a recovered `TTS` error without crashing.
- Ticket Record: `planning/tickets/TASK-014.md`

### TASK-015: M3 centralized config loader and schema validation
- [x] Status: Done
- Size: M
- Completed: 2026-03-24
- Outcome: Added a centralized validated config loader with example/local layering, supported secret loading, and shared config access helpers for runtime callers.
- Verification: `python -m pytest -q` -> 82 passed, 1 skipped; `_testing.py config-summary --config config/settings.example.json` printed a safe validated summary; `_testing.py open-app-real --app calculator --config config/settings.example.json` still launched Calculator via the centralized config path.
- Ticket Record: `planning/tickets/TASK-015.md`

### TASK-016: M3 logging, health metrics, and watchdog
- [x] Status: Done
- Size: M
- Completed: 2026-03-25
- Outcome: Added rotating log setup, runtime health snapshots, and an audio watchdog that can detect stalled input and trigger recovery.
- Verification: `python -m pytest -q` -> 87 passed, 1 skipped; `_testing.py watchdog-fake` printed `watchdog triggered: True`, `recover calls: 1`, and a health summary line.
- Ticket Record: `planning/tickets/TASK-016.md`

### TASK-017: M3 long-session stability harness and baseline benchmark
- [x] Status: Done
- Size: M
- Completed: 2026-03-25
- Outcome: Added a repeatable test-mode stability harness, JSON benchmark artifact output, and documented the target-machine 4+ hour validation procedure with pass/fail thresholds.
- Verification: `python -m pytest -q` -> 89 passed, 1 skipped; `_testing.py stability-harness-fake --output artifacts/stability-smoke.json` printed `sample count: 4`, `recovery count: 1`, `rss drift bytes: 8000000`, and `passed: True`.
- Ticket Record: `planning/tickets/TASK-017.md`

---

## Usage Notes

- Move tasks between sections instead of duplicating them.
- Keep task IDs stable and update only status/details.
- Add links to PRs/commits under the relevant task when work starts.
- Recommended next ticket after `TASK-017`: `TASK-018`.

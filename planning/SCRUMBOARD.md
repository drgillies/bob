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

No tasks currently in backlog.

---

## To Do

### TASK-025: Wake-word custom model or engine change evaluation
- [ ] Status: To Do
- Size: M
- Objective: Decide whether to pursue a custom `Hey Bob` model for `openWakeWord` or change wake engine / wake phrase based on the `TASK-024` blocker result.
- Business Value: Resolves the main blocker to real spoken wake-word support.
- Inputs/Context: `TASK-024`, `docs/benchmark-baseline.md`, `docs/risk-register.md`.
- Target Files/Paths: `docs/benchmark-baseline.md`, `docs/risk-register.md`, `planning/tickets/TASK-025.md`.
- Implementation Notes: Compare custom-model cost, engine-switch cost, licensing impact, and likely wake quality.
- Constraints/Standards: Recommendation must stay evidence-based.
- Tests Required: Documentation review and any supporting spike outputs.
- Done Criteria: One concrete forward path is chosen and documented.
- Deliverable Format: Recommendation doc + next-step definition.

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

### TASK-018: M3 service mode decision and packaging strategy
- [x] Status: Done
- Size: M
- Completed: 2026-03-25
- Outcome: Documented the MVP startup and packaging strategy, added a Task Scheduler wrapper script, and recorded the current limitation that Bob still exits after bootstrap because a persistent runtime entrypoint does not exist yet.
- Verification: `python -m pytest -q` -> 89 passed, 1 skipped; `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-bob.ps1` launched the current startup path and then exited after bootstrap as expected; Task Scheduler dry-run commands are documented for execution on the target machine with sufficient permissions.
- Ticket Record: `planning/tickets/TASK-018.md`

### TASK-019: M3 privacy mode hardening
- [x] Status: Done
- Size: S
- Completed: 2026-03-25
- Outcome: Added explicit privacy gating for raw debug audio capture so disk writes are disabled by default and only allowed through deliberate opt-in.
- Verification: `python -m pytest -q` -> 91 passed, 1 skipped; `_testing.py audio-capture-wav --seconds 0 --output debug_capture.wav` refused to write by default; explicit opt-in with `--allow-debug-audio` allowed the write path, and a real 10-second opt-in run captured 125 frames and wrote `debug_capture.wav`.
- Ticket Record: `planning/tickets/TASK-019.md`

### TASK-020: M4 voice tuning and response style guide
- [x] Status: Done
- Size: M
- Completed: 2026-03-25
- Outcome: Added configurable TTS style controls, documented Bob's spoken persona rules, and introduced best-effort male voice preference with safe fallback behavior.
- Verification: `python -m pytest -q` -> `95 passed, 1 skipped`; `_testing.py tts-style --mode fake` printed the tuned rate/volume/pause output; `_testing.py tts-voices` showed the current machine only exposes female SAPI voices, so male selection remains best-effort until a male voice or alternate engine is added.
- Ticket Record: `planning/tickets/TASK-020.md`

### TASK-021: M4 TTS engine decision and optional upgrade path
- [x] Status: Done
- Size: S
- Completed: 2026-03-25
- Outcome: Recorded `pyttsx3` as the supported MVP default and documented Piper as a later optional upgrade path with explicit GPL and packaging caveats.
- Verification: `_testing.py tts-voices` reported two visible SAPI voices on the current machine, both female (`Microsoft Hazel Desktop` and `Microsoft Zira Desktop`), confirming that `pyttsx3` works while also confirming the current local voice limitation.
- Ticket Record: `planning/tickets/TASK-021.md`

### TASK-022: M4 wake phrase finalization and compliance notes
- [x] Status: Done
- Size: S
- Completed: 2026-03-25
- Outcome: Finalized `Hey Bob` as the MVP wake phrase and documented the operational caveats around engine support, false-trigger review, and possible custom-model requirements.
- Verification: Documentation review confirmed `Hey Bob` is consistent across shared config and wake-phrase docs, and `docs/benchmark-baseline.md` now records the custom-model and false-trigger observation caveats explicitly.
- Ticket Record: `planning/tickets/TASK-022.md`

### TASK-023: Cross-cutting licensing and risk register
- [x] Status: Done
- Size: S
- Completed: 2026-03-25
- Outcome: Added an explicit licensing and operational risk register covering the selected wake-word, STT, TTS, packaging, privacy, and compliance risks.
- Verification: Documentation review confirmed the chosen stack risks, mitigations, owners, and next actions are recorded in `docs/risk-register.md`, and `README.md` now references the register directly.
- Ticket Record: `planning/tickets/TASK-023.md`

### TASK-024: Real spoken wake-word validation for Hey Bob
- [x] Status: Done
- Size: M
- Completed: 2026-03-25
- Outcome: Performed real spoken wake-word validation work for `Hey Bob` and confirmed the current `openWakeWord` path is blocked by model availability, not by generic engine setup alone.
- Verification: Live validation confirmed official `openWakeWord` assets can be downloaded and ONNX initialization works on Windows, but the built-in model list does not include `hey_bob`; current machine result is that real spoken validation for `Hey Bob` remains blocked until a custom model is provided or the wake engine changes.
- Ticket Record: `planning/tickets/TASK-024.md`

---

## Usage Notes

- Move tasks between sections instead of duplicating them.
- Keep task IDs stable and update only status/details.
- Add links to PRs/commits under the relevant task when work starts.
- Recommended next ticket after `TASK-024`: `TASK-025`.



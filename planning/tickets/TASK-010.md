# TASK-010

## Ticket Metadata
- [x] Ticket ID: `TASK-010`
- [x] Title: `M2 utterance recording with end-of-speech VAD`
- [x] Status: `Done`
- [x] Size: `M`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-24`
- [x] Branch: `feature/task-010-utterance-recording-vad`

## Objective
- [x] What should be implemented or changed: Add post-wake utterance recording that captures speech frames, retains a short trailing silence buffer, and stops on end-of-speech or timeout.

## Business Value
- [x] Why this work matters: This creates a stable audio handoff for the upcoming STT adapter work and keeps the assistant response loop responsive after wake detection.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/SCRUMBOARD.md`
  - `docs/architecture.md`
  - `docs/basic-scope.md`
  - `docs/deep-research-report.md` (M2-02, referenced by scrumboard)
  - `TASK-009` decision: `Vosk` is the default STT target, so utterance output should stay simple PCM + metadata.

## Target Files / Paths
- [x] Files or directories expected to change:
  - `src/bob/audio/`
  - `src/bob/stt/`
  - `src/bob/orchestrator/`
  - `tests/`
  - `_testing.py`

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Use a lightweight energy-based VAD so the feature is testable without the full STT engine.
  - Return a typed utterance result with audio bytes, metadata, and stop reason.
  - Add a wake-to-utterance controller that builds on the existing idle loop instead of bypassing it.
  - Keep trailing silence in the recorded result to avoid clipping the end of speech.

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - Keep implementation under `src/`.
  - Prefer deterministic tests with fake frame sources and fake clocks where needed.
  - Preserve offline-first behavior and avoid raw audio persistence by default.

## Tests Required
- [x] Unit/integration/verification requirements:
  - Unit tests for energy-based VAD behavior.
  - Recorder tests for end-of-speech stop and timeout stop.
  - Orchestrator integration test for wake-to-utterance handoff.

## Manual Tests
- [x] Command:
  - `$env:PYTHONPATH="src"; uv run --with-requirements requirements.txt -- python _testing.py utterance-record --output debug_utterance.wav`
- [x] Expected Result:
  - Audio capture starts, the recorder waits for speech, and it stops with `END_OF_SPEECH` after a short silence or `TIMEOUT` if no speech arrives.
  - A WAV file is written only when utterance audio was captured.
- [x] Actual Result:
  - Silent run: `speech started: False`, `stop reason: TIMEOUT`, `frame count: 0`, and no WAV file written.
  - Spoken run: `speech started: True`, `stop reason: END_OF_SPEECH`, `frame count: 14`, `speech frames: 3`, `duration seconds: 1.12`, and `debug_utterance.wav` was written.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - A wake-triggered utterance can be recorded without STT integration.
  - End-of-speech stop and timeout stop are both validated.
  - Result metadata is sufficient for the next STT ticket.

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Code changes, updated planning files, test evidence, and a manual `_testing.py` command.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-24`
- [x] Latest Update: `Manual validation passed for both timeout-with-silence and end-of-speech-with-audio scenarios.`
- [x] Blockers: `None`
- [x] Completed: `2026-03-24`
- [x] Merge Commit (if merged): `69399f3`

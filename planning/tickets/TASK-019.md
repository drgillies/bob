# TASK-019

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-019`
- [x] Title: `M3 privacy mode hardening`
- [x] Status: `Done`
- [x] Size: `S`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-25`
- [x] Branch: `feature/task-019-privacy-mode-hardening`

## Objective
- [x] What should be implemented or changed: Enforce no raw audio persistence by default and make any debug audio capture an explicit opt-in with clear visibility.

## Business Value
- [x] Why this work matters: Reduces privacy risk, aligns the runtime with the project’s documented safety baseline, and makes debugging behavior explicit instead of accidental.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `docs/deep-research-report.md` (M3-07)
  - `docs/basic-scope.md`
  - `docs/error-handling-policy.md`
  - current audio/manual test helpers in `_testing.py`

## Target Files / Paths
- [x] Files or directories expected to change:
  - `src/bob/config/`
  - `src/bob/audio/`
  - `docs/configuration.md`
  - `tests/`
  - `_testing.py` if debug behavior needs clearer control

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - keep raw audio persistence disabled by default
  - add explicit debug opt-in for any saved audio artifacts
  - make privacy-impacting behavior visible in logs or output

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - secure/default-private behavior first
  - no surprise raw audio storage
  - docs and config must match runtime behavior

## Tests Required
- [x] Unit/integration/verification requirements:
  - tests for default-off behavior
  - tests for explicit-on debug behavior
  - manual validation that debug capture only occurs when enabled

## Manual Tests
- [x] Command: `python _testing.py audio-capture-wav --seconds 0 --output debug_capture.wav`
- [x] Expected Result: Raw audio write is refused by default and no WAV file is created.
- [x] Actual Result: Printed `debug audio capture disabled by default` and `Refusing to write raw audio. Use --allow-debug-audio for explicit opt-in.` No `debug_capture.wav` file was created.
- [x] Command: `python _testing.py audio-capture-wav --seconds 0 --output debug_capture.wav --allow-debug-audio`
- [x] Expected Result: Raw audio write path is only reachable with explicit opt-in.
- [x] Actual Result: Printed `WARNING: writing raw debug audio to disk.` and then attempted audio startup. In this shell the run stopped at dependency startup because `sounddevice` was not installed, but the privacy gate itself was bypassed only after explicit opt-in.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - raw audio persistence is off by default
  - explicit debug opt-in exists
  - privacy behavior is documented
  - tests cover the behavior

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Code changes, config/doc updates, and validation evidence.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-25`
- [x] Latest Update: `2026-03-25`
- [ ] Blockers:
- [x] Completed: `2026-03-25`
- [ ] Merge Commit (if merged):

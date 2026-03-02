# TICKET_TEMPLATE

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-004`
- [x] Title: M1 audio capture MVP with recovery
- [x] Status: `Done`
- [x] Size: `M`
- [x] Priority: High
- [x] Requested By: User
- [x] Created Date: 2026-03-02
- [x] Branch: `feature/task-004-audio-capture-mvp`

## Objective
- [x] What should be implemented or changed: Implement continuous microphone frame capture using `sounddevice` with queue-based callback and stream recovery.

## Business Value
- [x] Why this work matters: Enables low-latency always-on listening on older hardware and unlocks wake-word integration work.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/SCRUMBOARD.md` (`TASK-004`)
  - `docs/deep-research-report.md` (M1-03)
  - `docs/architecture.md`
  - `docs/basic-scope.md`

## Target Files / Paths
- [x] Files or directories expected to change:
  - `src/bob/audio/`
  - `src/bob/orchestrator/`
  - `tests/`
  - `planning/tickets/TASK-004.md`

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Keep audio callback lightweight; queue frames for downstream processing.
  - Add recovery path for audio stream interruption/device loss.
  - Keep implementation compatible with older Windows hardware.

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - `AGENT.md`
  - `standards/code-standards.md`
  - `standards/project-standards.md`
  - `standards/style-guides.md`

## Tests Required
- [x] Unit/integration/verification requirements:
  - Unit test for frame queueing path.
  - Integration smoke for capture start/stop and recovery behavior.

## Manual Tests
- [x] Command: `$env:PYTHONPATH='src'; uv run --with-requirements requirements.txt -- python -m pytest -q tests/test_audio_capture.py`
- [x] Expected Result: Audio capture tests pass (queueing, start/stop, recovery behavior).
- [x] Actual Result: `5 passed`

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - Continuous capture path implemented.
  - Callback remains non-blocking with queue handoff.
  - Stream recovery path verified and documented.
  - Ticket and scrumboard status are synchronized.

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence):
  - Patch summary
  - Changed files
  - Test and manual verification output summary

## Execution Log
- [x] Agent: Codex
- [x] Started: 2026-03-02
- [x] Latest Update: Marked complete after unit + optional hardware test path validation.
- [x] Blockers: None
- [x] Completed: 2026-03-02
- [x] Merge Commit (if merged): `adf64ee`

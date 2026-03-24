# TASK-014

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-014`
- [x] Title: `M2 session memory and error-handling policy`
- [x] Status: `Done`
- [x] Size: `M`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-24`
- [x] Branch: `feature/task-014-session-memory-error-policy`

## Objective
- [x] What should be implemented or changed: Add session-only memory for the current runtime and document a clear error-handling policy that defines retry, reset, and fail-safe behavior per component.

## Business Value
- [x] Why this work matters: Improves conversational continuity within a single run and makes failure handling predictable so the assistant can recover cleanly instead of degrading silently.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `docs/deep-research-report.md` (M2-10, M2-11)
  - `docs/basic-scope.md`
  - Current orchestration and state flow in `src/bob/orchestrator/`
  - Session memory must be runtime-only and cleared on restart

## Target Files / Paths
- [x] Files or directories expected to change:
  - `src/bob/orchestrator/`
  - `src/bob/data/model/`
  - `docs/error-handling-policy.md`
  - `tests/`

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Add a lightweight session memory structure for recent turns/state only
  - Keep memory scoped to process lifetime with no persistence by default
  - Define recovery behavior for wake, audio capture, STT, routing, and TTS paths
  - Ensure transient failures return the assistant to a safe idle state

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - Use `src/` layout conventions already established in the repo
  - No raw audio persistence by default
  - Keep behavior deterministic and easy to test

## Tests Required
- [x] Unit/integration/verification requirements:
  - Unit tests for session memory lifecycle
  - Tests for error recovery paths back to `IDLE`
  - Documentation of expected runtime behavior for handled failures

## Manual Tests
- [x] Command: `python _testing.py session-runtime-fake`
- [x] Expected Result: Session memory records the routed turn and fake TTS speaks the response with no recovered error.
- [x] Actual Result: Printed `recent user texts: ['what time is it']`, `last intent: GET_TIME`, `last response: The time is 8:00 PM.`, and `errors: []`.
- [x] Command: `python _testing.py session-runtime-fake --tts-fail`
- [x] Expected Result: TTS failure is recovered without crash, Bob returns to idle behavior, and session memory records a `TTS` recovery event.
- [x] Actual Result: Printed `acknowledge calls: 1`, `errors: [('TTS', 'fake tts failure')]`, and `recovered error: TTS`.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - `docs/error-handling-policy.md` exists
  - Session memory is implemented for runtime-only use
  - Transient failures recover to `IDLE`
  - Tests cover lifecycle and recovery behavior

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Code changes, policy doc, updated ticket/board state, and test evidence.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-24`
- [x] Latest Update: `2026-03-24`
- [ ] Blockers:
- [x] Completed: `2026-03-24`
- [ ] Merge Commit (if merged):

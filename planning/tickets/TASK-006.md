# TICKET_TEMPLATE

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-006`
- [x] Title: M1 wake phrase integration in idle loop
- [x] Status: `Done`
- [x] Size: `M`
- [x] Priority: High
- [x] Requested By: User
- [x] Created Date: 2026-03-23
- [x] Branch: `feature/task-006-wake-phrase-integration`

## Objective
- [x] What should be implemented or changed: Integrate wake-word detection into Bob's idle loop with clear state transitions and debouncing, using the `TASK-005` spike as the basis for engine abstraction and selection.

## Business Value
- [x] Why this work matters: This is the first real activation path for Bob and is required before the assistant can move from passive listening to deterministic interaction.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/SCRUMBOARD.md` (`TASK-006`)
  - `planning/tickets/TASK-005.md`
  - `docs/benchmark-baseline.md`
  - `docs/architecture.md`
  - `docs/basic-scope.md`

## Target Files / Paths
- [x] Files or directories expected to change:
  - `src/bob/wakeword/`
  - `src/bob/orchestrator/`
  - `src/bob/`
  - `tests/`
  - `planning/tickets/TASK-006.md`
  - `planning/SCRUMBOARD.md`

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Add a wake-word adapter boundary instead of hard-coding a vendor/library directly into the orchestrator.
  - Keep the idle loop lightweight and avoid any STT work before a wake trigger.
  - Implement debouncing so a single utterance cannot trigger repeated wake events.
  - Prefer a fake/test detector for automated tests and keep real engine wiring minimal until the integration path is stable.

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - `AGENT.md`
  - `standards/code-standards.md`
  - `standards/project-standards.md`
  - `standards/style-guides.md`

## Tests Required
- [x] Unit/integration/verification requirements:
  - Unit tests for debouncing and wake-trigger state transitions.
  - Integration-style test proving the idle loop moves from `IDLE` to triggered state once per utterance.
  - Manual observation path documented for false-trigger logging.

## Manual Tests
- [x] Command: `$env:PYTHONPATH='src'; uv run --with-requirements requirements.txt -- python _testing.py wake-idle-loop --seconds 2 --trigger-after-frames 3`
- [x] Expected Result: Live audio capture should start, the fake wake detector should trigger once, and the orchestrator should print `IDLE -> TRIGGERED -> IDLE`.
- [x] Actual Result: Audio started, one wake event was emitted, detector reset once, and state transitions printed as `['IDLE', 'TRIGGERED', 'IDLE']`.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - Wake detection is integrated behind an adapter or service boundary.
  - Idle loop transitions are observable and debounced.
  - No full STT runs in the idle loop.
  - Ticket and scrumboard status are synchronized.

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence):
  - Code changes
  - Test evidence
  - Updated planning artifacts

## Execution Log
- [x] Agent: Codex
- [x] Started: 2026-03-23
- [x] Latest Update: Accepted after automated validation and manual `_testing.py` wake-idle-loop confirmation.
- [x] Blockers: None
- [x] Completed: 2026-03-23
- [x] Merge Commit (if merged): `8217e14`

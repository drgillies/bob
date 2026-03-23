# TICKET_TEMPLATE

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-008`
- [x] Title: M1 state indicator and mute control
- [x] Status: `Done`
- [x] Size: `S`
- [x] Priority: High
- [x] Requested By: User
- [x] Created Date: 2026-03-23
- [x] Branch: `feature/task-008-state-indicator-mute-control`

## Objective
- [x] What should be implemented or changed: Expose observable assistant states and add a config-driven mute control that disables wake processing while the process remains running.

## Business Value
- [x] Why this work matters: This improves operability, debugging, and privacy confidence by making assistant state visible and giving the user a non-destructive mute path.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/SCRUMBOARD.md` (`TASK-008`)
  - `planning/tickets/TASK-006.md`
  - `planning/tickets/TASK-007.md`
  - `docs/basic-scope.md`
  - `docs/architecture.md`

## Target Files / Paths
- [x] Files or directories expected to change:
  - `src/bob/orchestrator/`
  - `src/bob/observability/`
  - `config/settings.example.json`
  - `tests/`
  - `planning/tickets/TASK-008.md`
  - `planning/SCRUMBOARD.md`

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Build on the wake and TTS state flow already added in `TASK-006` and `TASK-007`.
  - Keep state reporting simple and explicit for MVP.
  - Mute should block wake-response handling without shutting down the process.
  - Prefer testable in-memory state observers before adding heavier logging infrastructure.

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - `AGENT.md`
  - `standards/code-standards.md`
  - `standards/project-standards.md`
  - `standards/style-guides.md`

## Tests Required
- [x] Unit/integration/verification requirements:
  - Unit tests for mute behavior.
  - State transition tests proving visibility of relevant assistant states.
  - Manual test command documented.

## Manual Tests
- [x] Command: `$env:PYTHONPATH='src'; uv run --with-requirements requirements.txt -- python _testing.py mute-response` and `$env:PYTHONPATH='src'; uv run --with-requirements requirements.txt -- python _testing.py mute-response --muted`
- [x] Expected Result: Unmuted mode should speak the deterministic response and show visible state changes; muted mode should suppress wake handling while the process remains running.
- [x] Actual Result: Unmuted mode printed `['IDLE', 'TRIGGERED', 'SPEAKING', 'IDLE']` and spoke `Hello, I'm here.`; muted mode printed `['IDLE']` with `detection: None`.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - Assistant states are observable in a consistent way.
  - Mute disables wake processing while runtime remains active.
  - Tests cover mute and state transitions.
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
- [x] Latest Update: Accepted after automated coverage and manual muted/unmuted validation through `_testing.py`.
- [x] Blockers: None
- [x] Completed: 2026-03-23
- [ ] Merge Commit (if merged):

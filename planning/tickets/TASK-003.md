# TICKET_TEMPLATE

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-003`
- [x] Title: M1 dependency baseline + audio device listing smoke
- [x] Status: `Done`
- [x] Size: `S`
- [x] Priority: High
- [x] Requested By: User
- [x] Created Date: 2026-03-02
- [x] Branch: `feature/task-003-dependency-baseline-uv`

## Objective
- [x] What should be implemented or changed: Pin initial dependency baseline and add audio device listing smoke flow.

## Business Value
- [x] Why this work matters: Confirms target-machine audio compatibility early and keeps dependency setup reproducible.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/SCRUMBOARD.md` (`TASK-003`)
  - `docs/deep-research-report.md` (M1-02)
  - `docs/setup-target-machine.md`
  - `README.md`

## Target Files / Paths
- [x] Files or directories expected to change:
  - `requirements.txt`
  - `src/audio/`
  - `docs/setup-target-machine.md`
  - `README.md`
  - `planning/tickets/TASK-003.md`

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Use `uv` for dependency installation and project command execution.
  - Add an audio device listing smoke command/script.
  - Update docs to use `uv` consistently for this project workflow.

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - `AGENT.md`
  - `standards/code-standards.md`
  - `standards/project-standards.md`
  - `standards/style-guides.md`

## Tests Required
- [x] Unit/integration/verification requirements:
  - Smoke command prints available audio devices.
  - Commands documented and runnable with `uv`.

## Manual Tests
- [x] Command: `$env:PYTHONPATH='src'; uv run --with-requirements requirements.txt -- python -m bob --version`
- [x] Expected Result: Version prints and command exits 0.
- [x] Actual Result: `0.1.0`
- [x] Command: `$env:PYTHONPATH='src'; uv run --with-requirements requirements.txt -- python -m bob --list-audio-devices`
- [x] Expected Result: At least one audio device line is printed and command exits 0.
- [x] Actual Result: Printed `Detected audio devices:` plus enumerated device list.
- [x] Command: `$env:PYTHONPATH='src'; uv run --with-requirements requirements.txt -- python -m pytest -q`
- [x] Expected Result: Test suite passes and command exits 0.
- [x] Actual Result: `3 passed in 0.27s`

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - Dependency baseline and docs updated to `uv`.
  - Audio device listing smoke path exists and is documented.
  - Ticket and scrumboard status are synchronized.

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence):
  - Patch summary
  - Changed files
  - Smoke command output summary

## Execution Log
- [x] Agent: Codex
- [x] Started: 2026-03-02
- [x] Latest Update: Implemented `uv` workflow docs, added audio device listing command, and verified with `uv run` + pytest.
- [x] Blockers: None
- [x] Completed: 2026-03-02
- [ ] Merge Commit (if merged):

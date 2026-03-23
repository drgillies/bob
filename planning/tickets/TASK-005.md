# TICKET_TEMPLATE

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-005`
- [x] Title: M1 wake-word spike and decision
- [x] Status: `Done`
- [x] Size: `M`
- [x] Priority: High
- [x] Requested By: User
- [x] Created Date: 2026-03-23
- [x] Branch: `feature/task-005-wake-word-spike`

## Objective
- [x] What should be implemented or changed: Evaluate wake-word engine options for Bob and record a primary plus fallback recommendation with reproducible benchmarking steps.

## Business Value
- [x] Why this work matters: Reduces risk around always-on activation, CPU usage, offline operation, and licensing before wake-word integration begins.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/SCRUMBOARD.md` (`TASK-005`)
  - `docs/deep-research-report.md`
  - `docs/basic-scope.md`
  - `docs/architecture.md`

## Target Files / Paths
- [x] Files or directories expected to change:
  - `docs/benchmark-baseline.md`
  - `docs/`
  - `planning/tickets/TASK-005.md`
  - `planning/SCRUMBOARD.md`

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Compare `openWakeWord`, `Porcupine`, and one fallback option against project constraints.
  - Capture install friction, offline behavior, CPU expectations, and licensing caveats.
  - Prefer a documented, reproducible spike over premature integration code.

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - `AGENT.md`
  - `standards/code-standards.md`
  - `standards/project-standards.md`
  - `standards/style-guides.md`

## Tests Required
- [x] Unit/integration/verification requirements:
  - Reproducible benchmark or evaluation steps documented.
  - Decision rationale tied back to hardware and offline-first constraints.

## Manual Tests
- [x] Command: `uv run --with openwakeword -- python -c "import openwakeword; print('openwakeword import ok')"` plus candidate smoke commands for `pvporcupine` and `pocketsphinx`
- [x] Expected Result: Candidate packages should install and provide enough signal to compare Windows setup friction and basic runtime readiness.
- [x] Actual Result: `openwakeword` imported but model initialization was not turnkey; `pvporcupine` imported cleanly; `pocketsphinx` imported and `Decoder()` initialized cleanly.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - Primary and fallback wake-word engine recommendation recorded.
  - Tradeoffs, licensing, and installation constraints documented.
  - Benchmark/evaluation process is reproducible.
  - Ticket and scrumboard status are synchronized.

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence):
  - Decision record
  - Benchmark or evaluation notes
  - Updated planning artifacts

## Execution Log
- [x] Agent: Codex
- [x] Started: 2026-03-23
- [x] Latest Update: Accepted and ready for merge after documenting the recommendation, fallback, and benchmark procedure.
- [x] Blockers: None
- [x] Completed: 2026-03-23
- [x] Merge Commit (if merged): `4316c56`

# TICKET_TEMPLATE

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-009`
- [x] Title: M2 STT engine spike and decision
- [x] Status: `Done`
- [x] Size: `M`
- [x] Priority: High
- [x] Requested By: User
- [x] Created Date: 2026-03-23
- [x] Branch: `feature/task-009-stt-spike-decision`

## Objective
- [x] What should be implemented or changed: Compare likely offline STT options for Bob and record the default plus fallback choice with reproducible benchmark steps.

## Business Value
- [x] Why this work matters: This de-risks latency, memory, and install complexity before deeper utterance recording and STT integration work begins.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/SCRUMBOARD.md` (`TASK-009`)
  - `docs/deep-research-report.md`
  - `docs/basic-scope.md`
  - `docs/architecture.md`
  - `docs/benchmark-baseline.md`

## Target Files / Paths
- [x] Files or directories expected to change:
  - `docs/benchmark-baseline.md`
  - `docs/`
  - `planning/tickets/TASK-009.md`
  - `planning/SCRUMBOARD.md`

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Compare `Vosk` against `whisper.cpp` and one practical fallback path such as `faster-whisper`.
  - Focus on target-machine suitability: latency, memory, install friction, and offline operation.
  - Keep this as a documented spike/decision ticket, not a full STT implementation ticket.

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - `AGENT.md`
  - `standards/code-standards.md`
  - `standards/project-standards.md`
  - `standards/style-guides.md`

## Tests Required
- [x] Unit/integration/verification requirements:
  - Reproducible benchmark or evaluation procedure documented.
  - Default and fallback STT recommendations justified against project constraints.

## Manual Tests
- [x] Command: `uv run --with vosk -- python -c "import vosk; print('vosk import ok')"` plus import checks for `faster-whisper` and `whispercpp`
- [x] Expected Result: Candidate STT engines should install or import with enough signal to compare Windows setup friction and operational fit.
- [x] Actual Result: `vosk`, `faster-whisper`, and `whispercpp` all imported on this machine; `vosk` was lowest-friction, `faster-whisper` pulled a heavier dependency stack, and `whispercpp` required a build during install.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - STT default and fallback recommendations are recorded.
  - Tradeoffs for latency, memory, install complexity, and offline suitability are documented.
  - Benchmark/evaluation steps are reproducible.
  - Ticket and scrumboard status are synchronized.

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence):
  - Benchmark/decision update
  - Updated planning artifacts
  - Manual validation notes if applicable

## Execution Log
- [x] Agent: Codex
- [x] Started: 2026-03-23
- [x] Latest Update: Accepted after documenting the STT recommendation, local feasibility checks, and reproducible benchmark procedure.
- [x] Blockers: None
- [x] Completed: 2026-03-23
- [x] Merge Commit (if merged): `8c586c9`

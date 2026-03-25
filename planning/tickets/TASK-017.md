# TASK-017

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-017`
- [x] Title: `M3 long-session stability harness and baseline benchmark`
- [x] Status: `Done`
- [x] Size: `M`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-25`
- [x] Branch: `feature/task-017-stability-harness-benchmark`

## Objective
- [x] What should be implemented or changed: Create a repeatable long-session stability harness and extend the benchmark baseline so Bob can be exercised for multi-hour reliability validation.

## Business Value
- [x] Why this work matters: Gives us a practical way to measure crash-free runtime, memory drift, and watchdog/recovery behavior before we treat the assistant as stable on target hardware.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `docs/deep-research-report.md` (M3-04)
  - `docs/basic-scope.md`
  - `docs/benchmark-baseline.md`
  - `docs/error-handling-policy.md`
  - recent observability work in `src/bob/observability/`

## Target Files / Paths
- [x] Files or directories expected to change:
  - `docs/benchmark-baseline.md`
  - `src/` test-mode harness script or module
  - `tests/`
  - related docs if validation workflow changes

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Add a repeatable test-mode harness that can run for long periods without needing full live interaction
  - Capture health data relevant to memory drift and uptime
  - Define pass/fail criteria that are realistic for target hardware
  - Keep the procedure reproducible on the target machine

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - Prefer reproducible local validation over ad hoc checks
  - No raw audio persistence by default
  - Keep outputs safe to share in repo docs

## Tests Required
- [x] Unit/integration/verification requirements:
  - Tests for the harness control flow and output artifact shape
  - Manual validation procedure documented in the benchmark doc

## Manual Tests
- [x] Command: `python _testing.py stability-harness-fake --output artifacts/stability-smoke.json`
- [x] Expected Result: Writes a benchmark artifact, prints sample/recovery counts, and returns a passing result for the fake smoke profile.
- [x] Actual Result: Printed `sample count: 4`, `recovery count: 1`, `rss drift bytes: 8000000`, `passed: True`, and wrote `artifacts/stability-smoke.json`.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - Benchmark doc includes repeatable long-run procedure
  - Harness exists and is runnable
  - Pass/fail criteria are documented
  - Tests cover the harness behavior

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Code changes, doc updates, and validation evidence.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-25`
- [x] Latest Update: `2026-03-25`
- [ ] Blockers:
- [x] Completed: `2026-03-25`
- [x] Merge Commit (if merged): `d40b964`

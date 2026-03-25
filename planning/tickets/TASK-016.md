# TASK-016

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-016`
- [x] Title: `M3 logging, health metrics, and watchdog`
- [x] Status: `Done`
- [x] Size: `M`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-25`
- [x] Branch: `feature/task-016-logging-health-watchdog`

## Objective
- [x] What should be implemented or changed: Add rotating logs, runtime health metrics, and a watchdog that can detect stalled audio input and reset the stream safely.

## Business Value
- [x] Why this work matters: Improves reliability for long-running sessions, gives us actionable runtime visibility, and reduces the risk of silent audio failure.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `docs/deep-research-report.md` (M3-02, M3-03)
  - `docs/basic-scope.md`
  - `docs/error-handling-policy.md`
  - Existing config loader in `src/bob/config/`

## Target Files / Paths
- [x] Files or directories expected to change:
  - `src/bob/observability/`
  - `src/bob/audio/`
  - `src/bob/orchestrator/`
  - `config/settings.example.json`
  - `tests/`
  - related docs if runtime behavior changes

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Add structured rotating log setup for local diagnostics
  - Add health snapshot collection for CPU, memory, and uptime
  - Add watchdog logic for “no audio frames for > X seconds” and reset behavior
  - Keep logging useful without spamming duplicate exception noise

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - Logs should be actionable and local-first
  - No secrets in logs
  - Recovery behavior should align with `docs/error-handling-policy.md`

## Tests Required
- [x] Unit/integration/verification requirements:
  - Tests for logger setup and rotation config
  - Tests for health metric snapshots
  - Tests for watchdog trigger and reset behavior

## Manual Tests
- [x] Command: `python _testing.py watchdog-fake`
- [x] Expected Result: Watchdog detects a simulated no-audio stall, triggers one recovery, and prints a safe health summary.
- [x] Actual Result: Printed `watchdog triggered: True`, `recover calls: 1`, and `health summary: health uptime_seconds=3.0 cpu_percent=7.5 rss_bytes=12345678`.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - Rotating log setup exists
  - Health summaries are available
  - Audio watchdog can trigger a reset path
  - Tests cover core reliability behavior

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Code changes, tests, config/doc updates, and verification evidence.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-25`
- [x] Latest Update: `2026-03-25`
- [ ] Blockers:
- [x] Completed: `2026-03-25`
- [x] Merge Commit (if merged): `c48fa01`

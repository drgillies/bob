# TASK-013

## Ticket Metadata
- [x] Ticket ID: `TASK-013`
- [x] Title: `M2 local actions framework and Windows open-app skill`
- [x] Status: `Done`
- [x] Size: `M`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-24`
- [x] Branch: `feature/task-013-local-actions-open-app`

## Objective
- [x] What should be implemented or changed: Add a small local-actions framework and wire the `open <app>` intent to a Windows-safe app launcher driven by config mappings.

## Business Value
- [x] Why this work matters: This is Bob's first practical local action and it turns the current routing layer into something the user can actually use.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/SCRUMBOARD.md`
  - `docs/mvp-command-list.md`
  - `config/settings.example.json`
  - `TASK-012` currently routes `OPEN_APP`, `PLAY_MEDIA`, and `PAUSE_MEDIA`
  - `TASK-013` should activate `open <app>` while keeping unsupported actions safely gated

## Target Files / Paths
- [x] Files or directories expected to change:
  - `src/bob/skills/`
  - `src/bob/orchestrator/`
  - `config/settings.example.json`
  - `tests/`
  - `_testing.py`
  - `docs/mvp-command-list.md` if behavior needs clarification

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Add a simple action-dispatch abstraction so app launching is not embedded directly in the intent handler.
  - Drive app resolution from config aliases, for example `calculator -> calc.exe`.
  - Keep launch behavior Windows-first and non-privileged.
  - Return clear fallback responses for unknown apps or disabled skills.
  - Leave media-control intent routing in a safe "not enabled yet" state unless there is time to wire a minimal framework toggle cleanly.

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - No privileged or hidden automation behavior by default.
  - Runtime code stays under `src/`.
  - Tests should isolate launcher execution behind fakes.
  - Config should remain explicit and readable.

## Tests Required
- [x] Unit/integration/verification requirements:
  - Tests for app alias resolution.
  - Tests for known app, unknown app, and disabled action behavior.
  - Integration coverage from routed `OPEN_APP` intent to action response output.

## Manual Tests
- [x] Command:
  - `$env:PYTHONPATH="src"; python _testing.py open-app-fake --app calculator`
  - `$env:PYTHONPATH="src"; python _testing.py open-app-fake --app unknown-app --disabled`
  - `$env:PYTHONPATH="src"; uv run --with-requirements requirements.txt -- python _testing.py open-app-real --app calculator`
- [x] Expected Result:
  - Known configured aliases should resolve to a launch command and report success.
  - Disabled action mode should not launch anything and should return a safe disabled message.
  - Real action mode should resolve `calculator` and actually open Calculator on Windows.
- [x] Actual Result:
  - `open-app-fake --app calculator` printed `launch command: calc.exe`, `succeeded: True`, and `message: Opening calculator.`
  - `open-app-fake --app unknown-app --disabled` printed `succeeded: False`, no launch command, and `message: App launching is disabled right now.`
  - `open-app-real --app calculator` successfully opened Calculator.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - `open <app>` launches a configured Windows app through the new action layer.
  - Unknown or disabled apps return safe, useful responses.
  - Action behavior is config-driven and tested.
  - The framework leaves room for additional local actions later.

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Code changes, config update, tests, and a manual validation command.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-24`
- [x] Latest Update: `Validated the real open-app path by launching Calculator from the configured alias.`
- [x] Blockers: `None`
- [x] Completed: `2026-03-24`
- [ ] Merge Commit (if merged):

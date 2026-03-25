# TASK-024

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-024`
- [x] Title: `Real spoken wake-word validation for Hey Bob`
- [x] Status: `Done`
- [x] Size: `M`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-25`
- [x] Branch: `feature/task-024-real-wakeword-validation`

## Objective
- [x] What should be implemented or changed: Add a real validation path for spoken `Hey Bob` wake detection and record the target-machine results.

## Business Value
- [x] Why this work matters: Confirms whether Bob can actually wake from real spoken audio instead of only simulated trigger paths.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `docs/benchmark-baseline.md`
  - `docs/mvp-command-list.md`
  - `docs/risk-register.md`
  - `TASK-005`, `TASK-006`, and `TASK-022`
  - current wake phrase decision: `Hey Bob`

## Target Files / Paths
- [x] Files or directories expected to change:
  - `_testing.py`
  - `src/bob/wakeword/`
  - `docs/benchmark-baseline.md`
  - `planning/tickets/TASK-024.md`
  - related tests/docs if needed

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - create a real wake-word manual test path using live microphone input
  - record whether the current engine/model path can actually detect spoken `Hey Bob`
  - document blockers clearly if custom model work or engine changes are required

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - keep hardware/manual validation honest
  - do not claim support for `Hey Bob` unless it is truly validated on the machine

## Tests Required
- [x] Unit/integration/verification requirements:
  - manual live wake-word validation
  - update docs with actual observed outcome

## Manual Tests
- [x] Command: `$env:PYTHONPATH="src"; uv run --with openwakeword --with-requirements requirements.txt -- python _testing.py wake-openwakeword-live --seconds 15`
- [x] Expected Result: The command either detects a spoken `Hey Bob` and prints the detection details, or it reports a clear blocker/no-detection result without pretending wake support is validated.
- [x] Actual Result: The command downloaded the official `openWakeWord` assets, forced the ONNX path on Windows, and initialized successfully. It then reported the available built-in keywords as `['alexa', 'hey_jarvis', 'hey_mycroft', 'hey_rhasspy', 'timer', 'weather']` and confirmed that `hey_bob` is not a built-in model. Current machine result: spoken validation for `Hey Bob` is blocked until a custom model is provided or the wake engine changes.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - a real spoken wake validation path exists
  - results are recorded for the current machine
  - blockers or follow-up actions are documented if validation fails

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Manual test path, recorded validation result, and updated docs.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-25`
- [x] Latest Update: `2026-03-25`
- [ ] Blockers:
- [x] Completed:
- [ ] Merge Commit (if merged):

# TASK-026

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-026`
- [x] Title: `Custom openWakeWord Hey Bob model and integration path`
- [x] Status: `To Do`
- [x] Size: `L`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-25`
- [x] Branch: `feature/task-026-openwakeword-hey-bob-model`

## Objective
- [x] What should be implemented or changed: Define and implement the next practical path for custom `Hey Bob` support on `openWakeWord`, including model sourcing/training assumptions and integration requirements.

## Business Value
- [x] Why this work matters: Moves Bob from a documented wake-word blocker to an actual implementation path for real spoken `Hey Bob` without introducing vendor-key dependencies.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/tickets/TASK-024.md`
  - `planning/tickets/TASK-025.md`
  - `docs/benchmark-baseline.md`
  - `docs/risk-register.md`
  - `docs/mvp-command-list.md`
  - current validated result: `openWakeWord` runs on Windows with ONNX assets, but `hey_bob` is not a built-in model

## Target Files / Paths
- [x] Files or directories expected to change:
  - `src/bob/wakeword/`
  - `config/settings.example.json`
  - `docs/benchmark-baseline.md`
  - `docs/risk-register.md`
  - `planning/tickets/TASK-026.md`
  - any model-path setup or supporting docs required for the chosen custom-model workflow

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - keep the current wake-word adapter boundary
  - determine whether Bob will train, source, or locally load a custom `Hey Bob` model compatible with `openWakeWord`
  - document the required model files, config shape, and validation flow
  - only claim success if real spoken validation is possible on the selected path

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - no vendor-key or hosted-console wake-word dependency in the default path
  - keep conclusions and docs honest about model quality, licensing, and setup friction

## Tests Required
- [x] Unit/integration/verification requirements:
  - config and adapter tests for any new model-loading path
  - manual validation path for real spoken `Hey Bob` if a usable custom model becomes available
  - documentation review for model setup and licensing notes

## Manual Tests
- [ ] Command:
- [ ] Expected Result:
- [ ] Actual Result:

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - custom `Hey Bob` model path is clearly defined and wired, or a concrete blocker is documented
  - integration/config requirements are captured
  - the next real spoken validation step is clear

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Model-path decision, integration updates, and clear validation steps.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-25`
- [x] Latest Update: `2026-03-25`
- [ ] Blockers:
- [ ] Completed:
- [ ] Merge Commit (if merged):

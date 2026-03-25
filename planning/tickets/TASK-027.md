# TASK-027

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-027`
- [x] Title: `Source or train hey_bob.onnx for openWakeWord`
- [x] Status: `To Do`
- [x] Size: `L`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-25`
- [x] Branch: `feature/task-027-hey-bob-model-artifact`

## Objective
- [x] What should be implemented or changed: Source, train, or otherwise produce a compatible `openWakeWord` custom model artifact for `Hey Bob`, expected at `models/wakeword/openwakeword/hey_bob.onnx`, and validate whether it can support real spoken wake detection.

## Business Value
- [x] Why this work matters: This is the remaining blocker between Bob's documented wake integration path and real spoken `Hey Bob` validation.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/tickets/TASK-024.md`
  - `planning/tickets/TASK-025.md`
  - `planning/tickets/TASK-026.md`
  - `docs/openwakeword-custom-model.md`
  - `docs/benchmark-baseline.md`
  - `docs/risk-register.md`
  - current blocker: integration/config support exists, but `models/wakeword/openwakeword/hey_bob.onnx` does not

## Target Files / Paths
- [x] Files or directories expected to change:
  - `models/wakeword/openwakeword/` if a usable artifact is produced
  - `docs/openwakeword-custom-model.md`
  - `docs/benchmark-baseline.md`
  - `docs/risk-register.md`
  - `planning/tickets/TASK-027.md`
  - any supporting setup or validation docs required by the model workflow

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - stay within the no-vendor-key wake-word constraint
  - determine whether a compatible model can be trained locally, sourced from a permissible workflow, or whether training remains blocked
  - if a model artifact is produced, validate it with Bob's live wake helper
  - if a model artifact cannot be produced yet, document the concrete blocker honestly

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - no vendor-key or hosted-console dependency in the default wake path
  - do not claim wake-word success unless real spoken validation passes
  - document any model licensing or redistribution constraints explicitly

## Tests Required
- [x] Unit/integration/verification requirements:
  - manual live validation with `_testing.py wake-openwakeword-live`
  - documentation review for model source/training/licensing notes
  - any adapter/config tests needed if the model workflow changes the runtime contract

## Manual Tests
- [ ] Command:
- [ ] Expected Result:
- [ ] Actual Result:

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - a compatible `hey_bob.onnx` path is either produced and validated, or blocked with a concrete reason
  - artifact/source/training requirements are documented
  - the next wake-word decision is clear

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Model artifact outcome, validation result, and updated docs.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-25`
- [x] Latest Update: `2026-03-25`
- [ ] Blockers:
- [ ] Completed:
- [ ] Merge Commit (if merged):

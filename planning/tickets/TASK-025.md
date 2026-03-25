# TASK-025

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-025`
- [x] Title: `Wake-word custom model or engine change evaluation`
- [x] Status: `In Review`
- [x] Size: `M`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-25`
- [x] Branch: `feature/task-025-wake-model-or-engine-eval`

## Objective
- [x] What should be implemented or changed: Decide whether Bob should pursue a custom `Hey Bob` wake-word model for `openWakeWord` or switch to a different wake engine/phrase path.

## Business Value
- [x] Why this work matters: Resolves the blocker preventing real spoken wake validation for the finalized product phrase.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/tickets/TASK-024.md`
  - `docs/benchmark-baseline.md`
  - `docs/risk-register.md`
  - `docs/mvp-command-list.md`
  - current machine result: `hey_bob` is not a built-in `openWakeWord` model

## Target Files / Paths
- [x] Files or directories expected to change:
  - `docs/benchmark-baseline.md`
  - `docs/risk-register.md`
  - `planning/tickets/TASK-025.md`
  - any evaluation notes or spike docs created during the decision

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - compare custom model work for `openWakeWord` against changing wake engine or wake phrase
  - record implementation cost, licensing impact, and expected quality/risk
  - recommend one concrete path forward

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - keep conclusions evidence-based
  - do not overstate support for `Hey Bob` without a validated engine/model path

## Tests Required
- [x] Unit/integration/verification requirements:
  - documentation review
  - any spike command outputs needed to support the recommendation

## Manual Tests
- [x] Command: `uv run --with openwakeword --with-requirements requirements.txt -- python _testing.py wake-openwakeword-live --seconds 15`
- [x] Expected Result: `openWakeWord` should either detect `Hey Bob` or report a concrete model/setup blocker for the finalized phrase.
- [x] Actual Result: ONNX initialization and official asset download succeeded, but the available built-in keywords did not include `hey_bob`, so real spoken validation for the finalized phrase remained blocked without a custom model or engine change.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - one recommended path is chosen
  - tradeoffs are documented
  - next implementation step is clear

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Recommendation doc updates and a clearly scoped next action.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-25`
- [x] Latest Update: `2026-03-25`
- [x] Blockers: `openWakeWord` does not provide a built-in `hey_bob` model on the validated Windows ONNX path.
- [x] Completed: Recommendation recorded: keep `Hey Bob`, preserve the adapter boundary, reject vendor-key wake-engine paths for now, and make custom `openWakeWord` model work the next implementation step.
- [ ] Merge Commit (if merged):


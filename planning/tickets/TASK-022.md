# TASK-022

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-022`
- [x] Title: `M4 wake phrase finalization and compliance notes`
- [x] Status: `Done`
- [x] Size: `S`
- [x] Priority: `Medium`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-25`
- [x] Branch: `feature/task-022-wake-phrase-finalization`

## Objective
- [x] What should be implemented or changed: Finalize Bob's wake phrase and document the operational and compliance notes for the chosen wake-word path.

## Business Value
- [x] Why this work matters: Locks the user-facing activation behavior for MVP release and makes the wake-word tradeoffs explicit.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `docs/deep-research-report.md` (M4-04)
  - `docs/benchmark-baseline.md`
  - prior wake-word decision from `TASK-005`
  - current wake phrase defaults in config/docs

## Target Files / Paths
- [x] Files or directories expected to change:
  - `docs/mvp-command-list.md`
  - `docs/persona-style.md`
  - `config/settings.example.json`
  - related wake-word docs if needed

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - confirm the default wake phrase for MVP
  - record false-trigger rationale and operational caveats
  - align docs/config with the final phrase and current engine constraints

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - offline-first assumptions should stay explicit
  - compliance and licensing caveats must remain visible

## Tests Required
- [x] Unit/integration/verification requirements:
  - documentation review
  - record the wake-phrase observation protocol or validation note if behavior changes

## Manual Tests
- [x] Command: Documentation review against `config/settings.example.json`, `docs/mvp-command-list.md`, and `docs/benchmark-baseline.md`
- [x] Expected Result: The final wake phrase is consistent across config and docs, and the `openWakeWord` custom-model caveat remains visible.
- [x] Actual Result: `Hey Bob` is consistent across the shared config and wake-phrase docs, and the benchmark doc now records the custom-model and false-trigger observation caveats explicitly.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - final wake phrase is recorded
  - rationale and caveats are documented
  - config/docs are aligned

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Updated docs/config and any recorded observation notes.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-25`
- [x] Latest Update: `2026-03-25`
- [ ] Blockers:
- [x] Completed:
- [ ] Merge Commit (if merged):

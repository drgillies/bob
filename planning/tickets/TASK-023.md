# TASK-023

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-023`
- [x] Title: `Cross-cutting licensing and risk register`
- [x] Status: `Done`
- [x] Size: `S`
- [x] Priority: `Medium`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-25`
- [x] Branch: `feature/task-023-risk-register`

## Objective
- [x] What should be implemented or changed: Create an explicit licensing and operational risk register for Bob's selected stack and link it from the shared docs.

## Business Value
- [x] Why this work matters: Prevents late-stage legal, packaging, and operational blockers from being discovered too late.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `docs/deep-research-report.md`
  - `docs/benchmark-baseline.md`
  - `docs/tts-engine-decision.md`
  - prior wake-word, STT, and TTS decisions

## Target Files / Paths
- [x] Files or directories expected to change:
  - `docs/risk-register.md`
  - `README.md`
  - related docs if cross-references are needed

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - list the selected stack risks and licensing notes
  - include mitigation, owner, and next-action fields
  - keep the register actionable rather than abstract

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - keep licensing caveats explicit
  - document current decisions, not hypothetical future stacks only

## Tests Required
- [x] Unit/integration/verification requirements:
  - documentation review

## Manual Tests
- [x] Command: Documentation review against `docs/benchmark-baseline.md`, `docs/tts-engine-decision.md`, `README.md`, and `docs/risk-register.md`
- [x] Expected Result: The chosen stack risks, licensing caveats, mitigations, owners, and next actions are recorded in one place and referenced from shared docs.
- [x] Actual Result: The risk register now captures wake-word, TTS, STT, packaging, privacy, and compliance risks, and `README.md` references the register directly.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - risk register exists
  - README references it
  - key stack risks and mitigations are recorded

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): New doc, README reference, and planning updates.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-25`
- [x] Latest Update: `2026-03-25`
- [ ] Blockers:
- [x] Completed:
- [x] Merge Commit (if merged): `abd3256`


# TASK-021

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-021`
- [x] Title: `M4 TTS engine decision and optional upgrade path`
- [x] Status: `Done`
- [x] Size: `S`
- [x] Priority: `Medium`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-25`
- [x] Branch: `feature/task-021-tts-engine-decision`

## Objective
- [x] What should be implemented or changed: Decide whether Bob should stay on `pyttsx3` only for MVP or document an optional upgrade path for a better TTS engine.

## Business Value
- [x] Why this work matters: Clarifies the path to a better voice without creating packaging or licensing surprises.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `docs/deep-research-report.md` (M4-02)
  - `docs/persona-style.md`
  - current `pyttsx3` implementation and machine voice limitations
  - packaging and licensing constraints from MVP

## Target Files / Paths
- [x] Files or directories expected to change:
  - `docs/persona-style.md`
  - `README.md`
  - `docs/setup-target-machine.md`
  - related decision docs if needed

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - record the default TTS engine decision for MVP
  - document optional upgrade candidates and tradeoffs
  - capture licensing or distribution caveats clearly

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - keep legal/distribution caveats explicit
  - align docs with the actual supported runtime path

## Tests Required
- [x] Unit/integration/verification requirements:
  - documentation review
  - install/run sanity for the chosen default path if behavior changes

## Manual Tests
- [x] Command: `$env:PYTHONPATH="src"; uv run --with-requirements requirements.txt -- python _testing.py tts-voices`
- [x] Expected Result: Local `pyttsx3` voices are listed so the MVP default can be judged against actual target-machine voice availability.
- [x] Actual Result: The current machine reported two visible SAPI voices, both female (`Microsoft Hazel Desktop` and `Microsoft Zira Desktop`), which confirms `pyttsx3` is operational but also confirms that a better male voice requires either extra local voice installation or a later engine upgrade path.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - TTS strategy decision is recorded
  - optional upgrade path is documented
  - docs are aligned with supported MVP behavior

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Decision note, doc updates, and validation evidence if runtime behavior changes.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-25`
- [x] Latest Update: `2026-03-25`
- [ ] Blockers:
- [x] Completed:
- [ ] Merge Commit (if merged):

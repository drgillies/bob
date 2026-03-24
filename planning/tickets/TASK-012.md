# TASK-012

## Ticket Metadata
- [x] Ticket ID: `TASK-012`
- [x] Title: `M2 intent router and core intents`
- [x] Status: `Done`
- [x] Size: `L`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-24`
- [x] Branch: `feature/task-012-intent-router-core-intents`

## Objective
- [x] What should be implemented or changed: Build a deterministic intent router that consumes STT text, resolves the MVP command set, and produces user-facing responses for the initial core intents.

## Business Value
- [x] Why this work matters: This turns transcription into useful assistant behavior and unlocks the first real end-to-end command loop for Bob.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/SCRUMBOARD.md`
  - `docs/mvp-command-list.md`
  - `docs/architecture.md`
  - `docs/basic-scope.md`
  - `TASK-011` output contract: `TranscriptionResult`
  - MVP focus remains deterministic routing before broader action/plugin work.

## Target Files / Paths
- [x] Files or directories expected to change:
  - `src/bob/skills/`
  - `src/bob/orchestrator/`
  - `src/bob/data/model/`
  - `tests/`
  - `_testing.py`
  - `docs/mvp-command-list.md` if any clarifications are needed

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Start with normalized exact matching for the listed MVP phrases.
  - Add limited fuzzy matching for close variants without making routing nondeterministic.
  - Return typed routing results rather than raw strings where possible.
  - Include an unknown-intent fallback response that is short and helpful.
  - Keep local-action intents routed but conservative until `TASK-013` wires the actual actions framework.

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - Keep behavior deterministic for MVP.
  - Runtime code stays under `src/`.
  - Prefer simple, explainable matching rules over opaque heuristics.
  - Tests should cover both exact and near-match behavior.

## Tests Required
- [x] Unit/integration/verification requirements:
  - Unit tests for text normalization and routing decisions.
  - Handler tests for time/date/status/fallback responses.
  - Integration coverage from `TranscriptionResult` into routed response output.

## Manual Tests
- [x] Command:
  - `$env:PYTHONPATH="src"; python _testing.py intent-fake --text "what time is it"`
  - `$env:PYTHONPATH="src"; python _testing.py intent-fake --text "what date is it"`
  - `$env:PYTHONPATH="src"; python _testing.py intent-fake --text "what day is it"`
- [x] Expected Result:
  - The fake transcription should route supported time/date phrases to the correct intent and return a short deterministic response.
- [x] Actual Result:
  - Output included `intent: GET_TIME`, `matched phrase: what time is it`, `confidence: 1.0`, and a time response in the form `The time is ...`.
  - Output included `intent: GET_DATE`, `matched phrase: what date is it`, `confidence: 1.0`, and a date response in the form `Today's date is ...`.
  - Output included `intent: GET_DATE`, `matched phrase: what day is it`, `confidence: 1.0`, and a date response in the form `Today's date is ...`.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - All commands in `docs/mvp-command-list.md` are routed.
  - Unknown intents produce a safe fallback.
  - Core intent responses are deterministic and tested.
  - The output is ready to be paired with TTS in the next user-visible loop.

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Code changes, tests, and a manual validation command or script.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-24`
- [x] Latest Update: `Fixed date/time routing edge cases, added regression coverage, and completed manual routing validation.`
- [x] Blockers: `None`
- [x] Completed: `2026-03-24`
- [ ] Merge Commit (if merged):

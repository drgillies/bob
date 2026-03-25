# TASK-020

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-020`
- [x] Title: `M4 voice tuning and response style guide`
- [x] Status: `Done`
- [x] Size: `M`
- [x] Priority: `Medium`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-25`
- [x] Branch: `feature/task-020-voice-tuning-style-guide`

## Objective
- [x] What should be implemented or changed: Add voice tuning config and document a consistent response style guide for Bob's spoken output.

## Business Value
- [x] Why this work matters: Helps Bob sound intentional and consistent, and keeps the intended "friendly, slow, simple" voice style aligned with the project's safety and compliance boundaries.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `docs/deep-research-report.md` (M4-01, M4-03, M4-05)
  - `docs/basic-scope.md`
  - current TTS config and `pyttsx3` implementation
  - project requirement to stay stylistic, not cloned

## Target Files / Paths
- [x] Files or directories expected to change:
  - `config/settings.example.json`
  - `docs/persona-style.md`
  - `src/bob/tts/`
  - related docs if style/config behavior changes

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - add simple voice tuning controls such as speech rate and voice selection guidance
  - define response-style rules for tone, length, and phrasing
  - keep the guidance friendly and legally safe

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - no copyrighted voice cloning
  - short, clear, friendly phrasing
  - config and docs should reflect actual runtime controls

## Tests Required
- [x] Unit/integration/verification requirements:
  - manual QA checklist for style consistency
  - tests for any new config-driven TTS behavior that is implemented

## Manual Tests
- [x] Command: `$env:PYTHONPATH="src"; uv run --with-requirements requirements.txt -- python _testing.py tts-style --mode fake`
- [x] Expected Result: Tuned TTS settings are printed (`rate`, `volume`, `sentence pause ms`) and the fake engine output shows sentence padding that reflects the configured pause style.
- [x] Actual Result: `python _testing.py tts-style --mode fake` printed `mode: fake`, `rate: 140`, `volume: 0.9`, `sentence pause ms: 150`, and `spoken: ['Hello. . I am here. . I can help with simple tasks.']`.
- [x] Command: `$env:PYTHONPATH="src"; uv run --with-requirements requirements.txt -- python _testing.py tts-voices`
- [x] Expected Result: Local `pyttsx3` voices are listed so a matching male voice can be selected or the machine limitation can be recorded.
- [x] Actual Result: `tts-voices` reported only two installed voices, both female (`Microsoft Hazel Desktop` and `Microsoft Zira Desktop`), so `preferred_gender: "male"` remains best-effort only on the current machine.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - style guide is published
  - config controls for voice tuning are wired if implemented
  - docs and implementation are aligned

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Doc updates, config changes, implementation changes if needed, and validation evidence.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-25`
- [x] Latest Update: `2026-03-25`
- [ ] Blockers:
- [x] Completed:
- [ ] Merge Commit (if merged):

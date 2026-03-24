# TASK-015

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-015`
- [x] Title: `M3 centralized config loader and schema validation`
- [x] Status: `Done`
- [x] Size: `M`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-24`
- [x] Branch: `feature/task-015-config-loader-validation`

## Objective
- [x] What should be implemented or changed: Centralize runtime config loading with `settings.local.json` overrides, validate expected fields, and keep `.env` restricted to secrets-only values.

## Business Value
- [x] Why this work matters: Gives Bob one reliable config path across machines, reduces setup drift, and prevents runtime failures caused by missing or malformed settings.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `docs/deep-research-report.md` (M3-01)
  - `docs/configuration.md`
  - `config/settings.example.json`
  - `config/settings.local.json`
  - `.env.example`
  - `.env` should remain secrets-only

## Target Files / Paths
- [x] Files or directories expected to change:
  - `src/`
  - `config/settings.example.json`
  - `.env.example`
  - `tests/`
  - related docs if config behavior changes

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Add a centralized loader instead of ad hoc file reads
  - Merge shared defaults with local machine overrides in a predictable order
  - Validate required keys and expected value types
  - Keep room for future config growth without scattering parsing logic

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - `.env` is secrets-only
  - No secrets should be logged
  - Keep config behavior deterministic and easy to test

## Tests Required
- [x] Unit/integration/verification requirements:
  - Unit tests for merge order
  - Validation tests for missing/invalid fields
  - Tests for `.env` secrets behavior where applicable

## Manual Tests
- [x] Command: `python _testing.py config-summary --config config/settings.example.json`
- [x] Expected Result: Validated config loads successfully and prints a safe summary without exposing secret values.
- [x] Actual Result: Printed project, assistant, wake phrase, STT/TTS engines, open-app aliases, and `loaded secret keys: []`.
- [x] Command: `python _testing.py open-app-real --app calculator --config config/settings.example.json`
- [x] Expected Result: Real open-app action resolves from centralized config loader and launches Calculator.
- [x] Actual Result: Printed `succeeded: True`, `message: Opening calculator.`, and metadata with `calc.exe`.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - Config load path is centralized
  - Validation failures are explicit and actionable
  - Example/local config layering is documented or self-evident in code/tests
  - Tests cover merge and validation behavior

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Code changes, tests, and any required config/doc updates.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-24`
- [x] Latest Update: `2026-03-24`
- [ ] Blockers:
- [x] Completed: `2026-03-24`
- [x] Merge Commit (if merged): `74445df`

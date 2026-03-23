# TICKET_TEMPLATE

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-007`
- [x] Title: M1 deterministic TTS response
- [x] Status: `Done`
- [x] Size: `S`
- [x] Priority: High
- [x] Requested By: User
- [x] Created Date: 2026-03-23
- [x] Branch: `feature/task-007-deterministic-tts-response`

## Objective
- [x] What should be implemented or changed: When the wake path triggers, produce a deterministic spoken response and return Bob to `IDLE`.

## Business Value
- [x] Why this work matters: This completes the first audible end-to-end interaction loop and proves Bob can react to a wake event with a predictable response.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/SCRUMBOARD.md` (`TASK-007`)
  - `planning/tickets/TASK-006.md`
  - `docs/deep-research-report.md`
  - `docs/basic-scope.md`
  - `docs/architecture.md`

## Target Files / Paths
- [x] Files or directories expected to change:
  - `src/bob/tts/`
  - `src/bob/orchestrator/`
  - `src/bob/cli.py`
  - `config/settings.example.json`
  - `tests/`
  - `planning/tickets/TASK-007.md`
  - `planning/SCRUMBOARD.md`

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Keep TTS behind a small adapter boundary similar to wake-word integration.
  - Default to `pyttsx3` for MVP, but keep test coverage independent of real audio output.
  - Reuse the `TASK-006` idle-loop trigger path to prove `TRIGGERED -> SPEAKING/response -> IDLE`.
  - Prefer deterministic text such as `Hello, I'm here.`

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - `AGENT.md`
  - `standards/code-standards.md`
  - `standards/project-standards.md`
  - `standards/style-guides.md`

## Tests Required
- [x] Unit/integration/verification requirements:
  - Integration-style test proving wake trigger leads to deterministic response handling and return to `IDLE`.
  - Unit tests for TTS adapter behavior and orchestrator response flow.
  - Manual test command documented.

## Manual Tests
- [x] Command: `$env:PYTHONPATH='src'; uv run --with-requirements requirements.txt -- python _testing.py deterministic-response --mode tts`
- [x] Expected Result: The wake-response flow should emit a wake detection, audibly speak `Hello, I'm here.`, and return to `IDLE`.
- [x] Actual Result: Audible output `Hello, I'm here.` was heard and the printed state flow returned to `IDLE` with response states `['TRIGGERED', 'SPEAKING', 'IDLE']`.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - Deterministic response path exists after wake trigger.
  - Bob returns to `IDLE` after the response path completes.
  - TTS behavior is configurable enough for MVP use.
  - Ticket and scrumboard status are synchronized.

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence):
  - Code changes
  - Test evidence
  - Updated planning artifacts

## Execution Log
- [x] Agent: Codex
- [x] Started: 2026-03-23
- [x] Latest Update: Accepted after automated validation and real `pyttsx3` manual confirmation of the deterministic reply.
- [x] Blockers: None
- [x] Completed: 2026-03-23
- [ ] Merge Commit (if merged):

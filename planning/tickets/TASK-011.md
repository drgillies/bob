# TASK-011

## Ticket Metadata
- [x] Ticket ID: `TASK-011`
- [x] Title: `M2 STT adapter + default implementation`
- [x] Status: `Done`
- [x] Size: `L`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-24`
- [x] Branch: `feature/task-011-stt-adapter-default-impl`

## Objective
- [x] What should be implemented or changed: Add a speech-to-text adapter boundary plus a default local implementation that can transcribe `TASK-010` utterances into text with typed metadata and typed error handling.

## Business Value
- [x] Why this work matters: This is the bridge from captured speech to usable text, and it keeps the project from locking orchestrator logic directly to a single STT library.

## Inputs / Context
- [x] Relevant links, docs, decisions, and assumptions:
  - `planning/SCRUMBOARD.md`
  - `docs/architecture.md`
  - `docs/basic-scope.md`
  - `docs/benchmark-baseline.md`
  - `TASK-009` decision: default STT engine is `Vosk`
  - `TASK-010` output contract: `RecordedUtterance`

## Target Files / Paths
- [x] Files or directories expected to change:
  - `src/bob/stt/`
  - `src/bob/orchestrator/`
  - `src/bob/data/model/`
  - `tests/`
  - `config/settings.example.json`
  - `_testing.py`

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - Define a stable STT service interface around `RecordedUtterance -> transcription result`.
  - Implement `Vosk` as the default adapter and keep engine-specific details behind the adapter boundary.
  - Use typed exceptions for model-load and transcription failures.
  - Keep model path and fallback behavior configurable rather than hard-coded.
  - Ensure orchestrator-side integration can handle STT failures without crashing the runtime.

## Constraints / Standards
- [x] Standards to follow (for example `standards/code-standards.md`):
  - Offline-first behavior must remain intact.
  - Runtime code stays under `src/`.
  - Tests should prefer deterministic fakes for adapter contract coverage.
  - Default behavior should be safe on older Windows hardware.

## Tests Required
- [x] Unit/integration/verification requirements:
  - Contract tests for STT service result and exception paths.
  - Default adapter tests for load/transcribe behavior using fakes or controlled seams.
  - Integration coverage for handing a `RecordedUtterance` into STT without crashing the orchestrator.

## Manual Tests
- [x] Command:
  - `$env:PYTHONPATH="src"; python _testing.py stt-fake`
  - Optional real-adapter check when a local Vosk model is present:
    - `$env:PYTHONPATH="src"; python _testing.py stt-vosk --model-path models/vosk/vosk-model-small-en-us-0.15 --wav debug_utterance.wav`
- [x] Expected Result:
  - The fake STT flow should show a wake event, a recorded utterance, and a deterministic fake transcript.
  - The real Vosk path should print a transcript for the provided WAV when a valid local model directory exists.
- [x] Actual Result:
  - `python _testing.py stt-fake` printed `utterance stop reason: END_OF_SPEECH`, `utterance duration: 0.40`, `wake keyword: hey bob`, `utterance frame count: 4`, and `transcript: what time is it`.
  - Real adapter validation passed with:
    - `uv run --with-requirements requirements.txt -- python _testing.py stt-vosk --model-path models/vosk/vosk-model-small-en-us-0.15 --wav _stt_sample.wav`
    - Output included `transcript: what time is it`, `engine: vosk`, and `audio duration: 2.04`.
  - User-recorded validation passed with:
    - `uv run --with-requirements requirements.txt -- python _testing.py stt-vosk --model-path models/vosk/vosk-model-small-en-us-0.15 --wav my_test.wav`
    - Output included `transcript: the alias aden is the smell is person i know`, `engine: vosk`, and `audio duration: 3.28`.

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - A default STT adapter exists behind a stable interface.
  - `RecordedUtterance` can be transcribed into typed text output plus metadata.
  - Error paths are typed and recoverable.
  - Config can select the default engine and reserve a fallback path.

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Code changes, config update, tests, and a manual validation command.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-24`
- [x] Latest Update: `Validated the real Vosk adapter with both a generated WAV sample and a user-recorded WAV sample.`
- [x] Blockers: `None`
- [x] Completed: `2026-03-24`
- [ ] Merge Commit (if merged):

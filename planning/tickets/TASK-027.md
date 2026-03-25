# TASK-027

Use this template when creating implementation tickets from `planning/SCRUMBOARD.md`.
The agent creates the initial ticket body, then you add final acceptance criteria.

## Ticket Metadata
- [x] Ticket ID: `TASK-027`
- [x] Title: `Source or train hey_bob.onnx for openWakeWord`
- [x] Status: `Done`
- [x] Size: `L`
- [x] Priority: `High`
- [x] Requested By: `User`
- [x] Created Date: `2026-03-25`
- [x] Branch: `feature/task-027-hey-bob-model-artifact`

## Objective
- [x] What should be implemented or changed: Investigate the `hey_bob.onnx` artifact path, validate whether Bob's real live `openWakeWord` runtime works on the target machine, and unblock wake-word testing with a temporary engineering phrase if a `Hey Bob` model cannot yet be produced.

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
  - current blocker at start: integration/config support exists, but `models/wakeword/openwakeword/hey_bob.onnx` does not

## Target Files / Paths
- [x] Files or directories expected to change:
  - `models/wakeword/openwakeword/`
  - `config/settings.example.json`
  - `src/bob/config/loader.py`
  - `src/bob/wakeword/openwakeword_detector.py`
  - `tests/test_openwakeword_detector.py`
  - `tests/test_config_loader.py`
  - `docs/openwakeword-custom-model.md`
  - `docs/benchmark-baseline.md`
  - `docs/risk-register.md`
  - `planning/tickets/TASK-027.md`
  - supporting setup or validation docs required by the model workflow

## Implementation Notes
- [x] Proposed approach and constraints for implementation:
  - stay within the no-vendor-key wake-word constraint
  - determine whether a compatible `Hey Bob` model can be trained locally, sourced from a permissible workflow, or whether training remains blocked
  - verify that Bob's real `openWakeWord` live runtime works on this machine
  - if a `Hey Bob` artifact cannot be produced yet, document the concrete blocker honestly
  - if a temporary engineering phrase is used, keep it clearly separate from the product phrase

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
- [x] Command: `uv run --with openwakeword --with-requirements requirements.txt -- python _testing.py wake-openwakeword-live --seconds 5 --use-builtin --wake-phrase "Hey Jarvis" --keyword hey_jarvis`
- [x] Expected Result: If Bob's live `openWakeWord` runtime is wired correctly, a built-in wake phrase should trigger a real detection event and drive `IDLE -> TRIGGERED -> IDLE`.
- [x] Actual Result: Real spoken `Hey Jarvis` triggered successfully with score `0.9556882381439209`, and Bob reported `['IDLE', 'TRIGGERED', 'IDLE']`.
- [x] Command: `uv run --with openwakeword --with-requirements requirements.txt -- python _testing.py wake-openwakeword-live --seconds 10`
- [x] Expected Result: Bob should initialize the configured temporary engineering model and detect real spoken `Yo homie`.
- [x] Actual Result: Bob initialized successfully with `models/wakeword/openwakeword/yo_homie.onnx`, detected real spoken `Yo homie` with score `0.99876868724823`, and reported `['IDLE', 'TRIGGERED', 'IDLE']`.
- [x] Command: `Invoke-RestMethod https://api.github.com/repos/fwartner/home-assistant-wakewords-collection/git/trees/main?recursive=1 | ...`
- [x] Expected Result: If a community `Bob` model exists in the referenced collection, it should appear in the repository tree.
- [x] Actual Result: `NO_BOB_MODELS_FOUND`

## Done Criteria
- [x] Minimum completion conditions for the agent:
  - Bob's real `openWakeWord` runtime is proven or disproven on the target machine
  - the `Hey Bob` artifact path is either produced and validated, or blocked with a concrete reason
  - artifact/source/training requirements are documented
  - the next wake-word decision is clear

## Additional Acceptance Criteria (User)
- [ ] Add your final acceptance criteria here:
- [ ] Add edge cases or non-goals here:

## Deliverable Format
- [x] Expected output from the agent (for example patch summary, changed files, test evidence): Runtime validation outcome, model artifact outcome, and updated docs.

## Execution Log
- [x] Agent: `Codex`
- [x] Started: `2026-03-25`
- [x] Latest Update: `2026-03-25`
- [x] Blockers: The final product-aligned `hey_bob.onnx` artifact still does not exist, and the official automated `openWakeWord` training path is currently documented as Linux-only.
- [x] Completed: Confirmed there is no `Bob` artifact in the referenced community collection, documented the official Linux-only training constraint, sourced `yo_homie.onnx` as a temporary engineering model, fixed the live frame-format bug in Bob's `openWakeWord` adapter, validated real spoken built-in `Hey Jarvis`, and validated real spoken `Yo homie` as a temporary engineering wake phrase.
- [x] Merge Commit (if merged): `56e4857`

# Bob

Lightweight local voice assistant project focused on older hardware.

## Current Status

- Repository is in planning/bootstrap phase.
- Primary implementation targets live under `src/` when development begins.
- `TASK-001`, `TASK-002`, and `TASK-003` are complete.

## Repository Layout

- `docs/`: product, architecture, setup, and configuration documentation
- `planning/`: scrum board and execution planning
- `standards/`: engineering standards and process rules
- `templates/`: reusable templates for tickets and planning
- `config/`: config templates (local machine-specific files are ignored)
- `src/`: application code
- `tests/`: automated tests

## Local Setup (Windows PowerShell)

1. Create local config files:
   - `Copy-Item config/settings.example.json config/settings.local.json`
   - `Copy-Item .env.example .env`
2. Set import path for `src/` layout:
   - `$env:PYTHONPATH = "src"`
3. Verify bootstrap entrypoint with `uv`:
   - `uv run --with-requirements requirements.txt -- python -m bob --version`
4. Verify default entrypoint with `uv`:
   - `uv run --with-requirements requirements.txt -- python -m bob`
5. List available audio devices with `uv`:
   - `uv run --with-requirements requirements.txt -- python -m bob --list-audio-devices`

## Workflow Baseline

- Branch naming:
  - `feature/<ticket-number>-<topic>`
  - `fix/<ticket-number>-<topic>`
  - `chore/<ticket-number>-<topic>`
- Use `planning/SCRUMBOARD.md` for task state tracking.
- Follow all documents in `standards/`.

## Validation Baseline

- Run tests before PR:
  - `uv run --with-requirements requirements.txt -- python -m pytest -q`
- Run lint/type checks when configured for the project.
- Update docs with any behavior/configuration changes.

## Bootstrap Smoke Check

From repository root (PowerShell):

1. Set import path for `src/` layout:
   - `$env:PYTHONPATH = "src"`
2. Run version smoke check:
   - `uv run --with-requirements requirements.txt -- python -m bob --version`
3. Run default entrypoint:
   - `uv run --with-requirements requirements.txt -- python -m bob`
4. Run audio device discovery smoke check:
   - `uv run --with-requirements requirements.txt -- python -m bob --list-audio-devices`

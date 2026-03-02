# Bob

Lightweight local voice assistant project focused on older hardware.

## Current Status

- Repository is in planning/bootstrap phase.
- Primary implementation targets live under `src/` when development begins.
- `TASK-001` and `TASK-002` are complete; next execution ticket is `TASK-003`.

## Repository Layout

- `docs/`: product, architecture, setup, and configuration documentation
- `planning/`: scrum board and execution planning
- `standards/`: engineering standards and process rules
- `templates/`: reusable templates for tickets and planning
- `config/`: config templates (local machine-specific files are ignored)
- `src/`: application code
- `tests/`: automated tests

## Local Setup (Windows PowerShell)

1. Create virtual environment:
   - `python -m venv .venv`
2. Activate virtual environment:
   - `.venv\Scripts\Activate.ps1`
3. Install dependencies:
   - `python -m pip install --upgrade pip`
   - `pip install -r requirements.txt`
4. Create local config files:
   - `Copy-Item config/settings.example.json config/settings.local.json`
   - `Copy-Item .env.example .env`

## Workflow Baseline

- Branch naming:
  - `feature/<ticket-number>-<topic>`
  - `fix/<ticket-number>-<topic>`
  - `chore/<ticket-number>-<topic>`
- Use `planning/SCRUMBOARD.md` for task state tracking.
- Follow all documents in `standards/`.

## Validation Baseline

- Run tests before PR:
  - `pytest`
- Run lint/type checks when configured for the project.
- Update docs with any behavior/configuration changes.

## Bootstrap Smoke Check

From repository root (PowerShell):

1. Set import path for `src/` layout:
   - `$env:PYTHONPATH = "src"`
2. Run version smoke check:
   - `python -m bob --version`
3. Run default entrypoint:
   - `python -m bob`

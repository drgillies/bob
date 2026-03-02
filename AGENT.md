# Agent Instructions

## Standards

- Follow repository standards documents:
  - `standards/style-guides.md`
  - `standards/code-standards.md`
  - `standards/project-standards.md`
  - `standards/git-standards.md`
- If guidance conflicts, follow the stricter rule and note the exception in the PR.

## Git and Branches

- Source of truth for Git workflow: `standards/git-standards.md`.
- Every ticket MUST get a new short-lived branch created from `main` before any implementation work starts.
- Branch naming follows: `feature/<ticket-number>-<topic>`, `fix/<ticket-number>-<topic>`, `chore/<ticket-number>-<topic>`.
  - Example: `feature/b1001-add-voice`.
- Before merge to `main`:
  - Ticket acceptance requirements are met.
  - Required local checks/tests pass.
  - Required reviewer approval is present.
  - User/product owner merge approval is present.

## Commits and Pull Requests

- Commit messages use imperative, specific format: `<type>: <summary>`.
  - Example: `fix: handle null values in parser`.
- Keep commits focused; do not mix unrelated changes.
- Do not commit generated artifacts unless explicitly required.
- Pull requests must include:
  - what changed
  - why it changed
  - how to verify
  - risks or follow-ups
- Link the related ticket/issue in the PR when available.

## Code

- Prefer existing, maintained libraries over new custom implementations when they satisfy requirements.
  - Add approved Python dependencies to `requirements.txt`.
- Prefer `dataclass` and class-based design where appropriate.
  - Place data validation and invariants at model/class boundaries.
- Use structured logging for debugging and error tracing.
  - Use consistent log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`).
  - Do not log secrets, credentials, or sensitive user data.
- Use Google-style docstrings where appropriate.
  - Add a `testing:` section that states what should be tested.

## Testing and Validation

- New or changed behavior should include tests when practical (unit first, integration where needed).
- At minimum, validate the changed path locally before requesting review.
- Bug fixes should include a regression test when practical.

## Template Usage

- If a template is required for a task, use the appropriate template from `templates/`.
  - If a required template is missing, request creation and add it to the list below.

- Templates:
  - `templates/TICKET_TEMPLATE.md`

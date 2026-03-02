# Style Guides

## Purpose

Define practical style conventions that keep code and documentation consistent and easy to review.

## Scope and Precedence

- This guide focuses on style and readability.
- Functional/quality requirements still come from:
  - `standards/code-standards.md`
  - `standards/project-standards.md`
  - `standards/git-standards.md`
- If rules conflict, follow the stricter rule and document the exception in the PR.

## Repository Base Layout

- Keep a predictable top-level structure:
  - `docs/`: Product, architecture, setup, and operational documentation.
  - `planning/`: Tickets, phase plans, and implementation notes.
  - `standards/`: Team standards and governance docs.
  - `templates/`: Reusable templates (tickets, PRs, docs).
  - `config/`: Project configuration templates and defaults (no machine-specific secrets).
  - `src/`: Application/runtime code (source of truth for implementation modules).
  - `tests/`: Automated tests that mirror `src/` structure (create with first testable module).
- Keep root files minimal and intentional:
  - `AGENT.md`: Agent operating rules.
  - `requirements.txt`: Python dependency declarations.
  - `README.md` (recommended): project overview and run steps.
- Avoid placing feature code directly in the repository root.
- When adding a new top-level directory, document its purpose in `README.md` or `docs/`.

## Python Style

- Follow PEP 8 formatting and naming.
- Prefer explicit, descriptive names over abbreviations.
- Keep functions focused; split when a function handles multiple concerns.
- Avoid magic numbers and hidden constants; name them.
- Use type hints for public functions and non-trivial internal helpers.

## Naming Conventions

- `snake_case` for variables, functions, and module filenames.
- `PascalCase` for classes and dataclasses.
- `UPPER_SNAKE_CASE` for module-level constants.
- Boolean names should read like predicates (`is_ready`, `has_error`).

## Documentation Style

- Use Google-style docstrings for non-trivial public functions/classes.
- Keep comments focused on intent and reasoning, not restating obvious code.
- Keep README and run instructions aligned with real commands.
- Prefer short sections and scannable bullets in docs.

## Logging Message Style

- Write log messages as clear action + context.
  - Good: `Failed to load profile for user_id=%s`
- Include stable identifiers when available (request ID, job ID, record ID).
- Avoid vague messages like `Something went wrong`.

## Error Message Style

- Error messages should be specific and actionable.
- Include what failed and which input/resource caused it.
- Raise domain-appropriate exceptions rather than broad `Exception`.

## Test Readability Style

- Use descriptive test names that encode behavior and expected outcome.
- Keep arrange/act/assert structure clear.
- Prefer deterministic test data and explicit fixtures.

## Imports and File Layout

- Group imports as stdlib, third-party, then local modules.
- Keep top-level module code minimal; place behavior in functions/classes.
- One module should have one clear responsibility.

## Style Exceptions

- When breaking style rules intentionally, add a brief code comment.
- Note any major style exception in the PR description with rationale.

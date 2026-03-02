# Code Standards

## Language and Style

- Target Python 3.10+.
- Follow PEP 8 and use clear, descriptive names.
- Keep functions small and single-purpose where practical.
- Avoid duplicated logic; refactor shared behavior into helpers.

## Environment and Execution

- Use the repository's documented workflow tool for environment setup and execution.
- Keep local setup commands consistent with the team baseline.
- Prefer reproducible commands over machine-specific shortcuts.

## Typing and Interfaces

- Add type hints for public functions and non-trivial internal helpers.
- Prefer explicit return types.
- Validate external inputs (config/data) near boundaries.
- Raise meaningful exceptions for invalid states.
- Document non-trivial functions using Google Style Docstrings.
- Include a `Testing:` section in each non-trivial function docstring that states what must be tested for that function (happy path, edge cases, and failure cases where applicable).

## Project Structure

- Keep domain logic in dedicated modules, not in entrypoint scripts.
- Place cross-cutting helpers in purpose-specific utility modules.
- Use `src/` as the project code root.
- Pull data through functions in `src/data/` rather than ad-hoc access patterns.
- Any data passed between components should use models defined in `src/data/model/` to enforce validation and consistency checks.
- Minimize side effects in core logic functions.
- Isolate I/O (file writes, network calls, logging) from computation when possible.
- Keep configuration parsing centralized.

## Data and State

- Place data checks and balances at the model level so validation is centralized and consistently enforced.
- Avoid mutating shared state unless intentional and documented.
- Copy mutable inputs when function behavior depends on isolation.
- Be explicit about units and semantics for values and counters.
- Preserve consistent naming across processing stages.

## Testing Standards

- Add tests for all bug fixes.
- Use each function's docstring `Testing:` section as a minimum baseline for test coverage.
- Add unit tests for core business logic and boundary conditions.
- Add integration tests for critical end-to-end flows where practical.
- Use deterministic seeds for stochastic behavior in tests.
- Cover primary branches, failure paths, and configuration variants.

## Logging Standards

- Use the standard `logging` module (or the repository's approved logging wrapper), not ad-hoc `print` statements.
- Log with appropriate levels: `DEBUG` for diagnostics, `INFO` for key state transitions, `WARNING` for recoverable issues, `ERROR` for failures.
- Keep log messages structured and actionable; include stable identifiers (for example request ID, record ID, job ID) when available.
- Do not log secrets or sensitive values (credentials, tokens, personal data); mask or redact when needed.
- Log exceptions with context and stack trace at the handling boundary; avoid logging the same exception multiple times.
- Configure logging centrally (format, handlers, levels) and avoid per-module one-off configuration.

## Quality Gates

- No known runtime exceptions on supported configuration paths.
- No dead imports or unused variables in modified files.
- New code should not add uncontrolled sleeps or debug prints in hot loops.
- Update docs alongside behavior changes.

## Dependency Standards

- Dependencies in `requirements.txt` must be valid installable package names.
- Add only required packages; remove unused dependencies.
- Pin or constrain versions intentionally and document rationale when strict.

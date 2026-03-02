# Project Standards

## Purpose

Define how work is scoped, documented, implemented, and accepted across a repository.

## Core Rules

- Every change must map to a clear objective in scope.
- Work should be incremental and reviewable in small PRs.
- Behavior changes must include documentation updates.
- Defects and known risks must be tracked in project docs.

## Scope and Planning

- Start each feature with a short scope statement:
  - problem
  - target behavior
  - non-goals
- Define acceptance criteria before implementation.
- Avoid mixing unrelated changes in one PR.

## Documentation Requirements

- Update the repository's primary documentation when adding or changing behavior.
- Keep run instructions current with actual commands.
- Record assumptions and constraints for non-obvious logic.
- Add or update architecture notes when module responsibilities change.

## Delivery Standards

- Prefer deterministic behavior for stateful or stochastic workflows when possible (seed support).
- No debug-only delays or logs in final default paths.
- Runtime side effects (files, prints) must be intentional and documented.
- New configuration options must have defaults and schema notes.
- Environment and run commands must follow the repository's documented workflow.

## Definition of Done

- Acceptance criteria are met.
- Relevant tests pass.
- Documentation is updated.
- Lint/type checks pass (where configured).
- Reviewer can reproduce behavior from documented steps.
- Verification commands are runnable with the documented project tooling.

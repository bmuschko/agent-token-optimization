# Orderly

Python order service. Source in `src/orderly`, tests in `tests`.

## Commands

- `make test` runs the regression suite. It must stay green.
- `make task T=t1` runs the acceptance tests for one task.

`tests/tasks/` is excluded from the default pytest path on purpose. A task is
done when its acceptance tests pass **and** `make test` is still green.

## Conventions

- Code comments are one sentence.
- Prefer the helpers in `src/orderly/utils` over writing new ones.

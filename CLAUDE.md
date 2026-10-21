# Orderly

Welcome to the Orderly codebase. This file gives an AI assistant the full context it needs to work effectively in this repository. Please read it carefully before making any changes.

## Project history

Orderly began life in 2019 as an internal script for reconciling partner order feeds, written originally in Perl and ported to Python in 2021 during the platform consolidation effort. The port was led by the Commerce Platform team, with review from Architecture. A second refactor in 2023 introduced the service layer and the repository pattern, replacing the direct database access that the original port had carried over. The current structure dates from that refactor, although several modules still reflect the earlier design and are scheduled for cleanup in a future quarter. The ingest layer in particular predates the service layer and does not follow the same conventions.

## Architecture

Orderly follows a layered architecture. Requests arrive at the API layer, which delegates to the service layer, which in turn uses repositories for persistence and integrations for outbound calls. Models are plain Python objects with `to_dict` and `from_dict`. Pricing is a separate concern and is not routed through services, for historical reasons described above.

The layering is intended to keep business rules out of the handlers and persistence details out of the services. In practice there are a few places where this is not strictly observed, and those are considered technical debt rather than examples to follow.

## Directory layout

- `src/orderly/api/` - HTTP-facing handlers
- `src/orderly/api/middleware/` - authentication, rate limiting, request logging
- `src/orderly/cache/` - the TTL cache and the startup warmer
- `src/orderly/ingest/` - inbound feed parsing and validation
- `src/orderly/integrations/` - outbound clients for payments, shipping, inventory
- `src/orderly/models/` - domain models
- `src/orderly/pricing/` - discounts, tax, currency, totals
- `src/orderly/reporting/` - summary building and exporters
- `src/orderly/repositories/` - persistence
- `src/orderly/services/` - business rules
- `src/orderly/utils/` - shared helpers
- `tests/` - the regression suite
- `tests/tasks/` - acceptance tests, excluded from the default pytest path

## Commands

- `make test` runs the regression suite. It must stay green.
- `make task T=t1` runs the acceptance tests for one task.
- `make coverage` checks coverage of the currency module.
- `make verify` checks the local setup.
- Python runs through `uv run`. There is no activated virtual environment, so use `uv run pytest ...` rather than `python3 -m pytest`.

## Code style

- Follow PEP 8.
- Use four spaces for indentation, never tabs.
- Keep lines under 100 characters where practical.
- Use double quotes for strings unless the string contains a double quote.
- Code comments are one sentence.
- Every public function has a docstring.
- Prefer f-strings over `%` formatting and over `str.format`.
- Prefer list comprehensions over `map` and `filter` where readable.
- Import standard library modules first, then third party, then local.
- Sort imports alphabetically within each group.
- Do not use wildcard imports.
- Avoid mutable default arguments.
- Prefer `pathlib` over `os.path` in new code.
- Type hints are encouraged on public functions.

## Testing conventions

- Test files are named `test_*.py`.
- Test functions are named `test_*`.
- Use plain `assert`, not `unittest` assertions.
- Fixtures live in `conftest.py`.
- Prefer small focused tests over large ones.
- Do not use network access in tests.
- Do not use `time.sleep` in tests unless testing concurrency.

## Git conventions

- Commit subjects are written in the imperative mood.
- Keep commit subjects under 80 characters.
- Reference the task identifier in the commit body where one applies.
- Do not commit generated files.
- Do not commit the virtual environment.

## Review expectations

Changes should be small and focused. A change that touches more than three files should explain why in the pull request description. Reviewers look for clear naming, appropriate test coverage, and consistency with the surrounding code.

## Dependencies

The project deliberately has no runtime dependencies beyond the standard library. Test tooling is pytest and pytest-cov. Please do not add runtime dependencies without discussion.

## Notes

Prefer the helpers in `src/orderly/utils` over writing new ones. Several of them are currently unused and that is intentional; they exist as seams.

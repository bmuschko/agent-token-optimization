# Tasks

Eight tasks seeded into this repository. You work them with your agent during
the exercises. Each one has acceptance tests that are **red on a fresh clone**.

```bash
make task T=t1        # acceptance tests for T1
make test             # regression suite, must stay green
```

A task is done when both are satisfied.

| ID | Kind | Task | Scope | Verify |
|---|---|---|---|---|
| T1 | Bug | Tier boundary off by one | 1 file | `make task T=t1` |
| T2 | Feature | Add `--format json` to the report command | 1 file | `make task T=t2` |
| T3 | Refactor | Extract the duplicated retry logic | 3 files | `make task T=t3` |
| T4 | Feature | Add pagination to `list_orders` | 2 files | `make task T=t4` |
| T5 | Exploration | Where is rate limiting, and how do I change the limit | read only | an answer |
| T6 | Bug | Missing null handling across parser and validator | 2 files | `make task T=t6` |
| T7 | Test | Cover the untested branches in `currency.py` | 1 test file | `make coverage` |
| T8 | Bug | Race condition in the cache warmer | subtle | `make task T=t8` |

## T1 - Tier boundary off by one

`src/orderly/pricing/discount.py`

The volume discount tiers are documented as inclusive of their thresholds: an
order of exactly $100.00 should earn the 5% rate. It does not. Orders one cent
above the threshold are fine, which is why the regression suite misses it.

## T2 - JSON output for the report command

`src/orderly/cli.py`

`orderly report` prints aligned text. Add `--format json` so it can also emit
JSON, keeping text as the default. The summary dictionary is already built by
`orderly.reporting.summary.build_summary`.

## T3 - Extract the duplicated retry logic

`src/orderly/integrations/{payments,shipping,inventory}.py`

The same retry loop with exponential backoff is copy-pasted into six methods
across three clients. `src/orderly/utils/retry.py` already has a
`call_with_retry` helper that nothing uses.

The acceptance test is structural: it fails if any integration module still
contains an inline `for attempt in range(` loop or a direct `time.sleep(`.
Behaviour is pinned by `tests/test_integrations.py`, which must stay green.

## T4 - Paginate `list_orders`

`src/orderly/api/orders.py`

The endpoint returns every order. Add `limit` and `offset`, and report `total`
and `has_more` in the response. `src/orderly/utils/pagination.py` already has
the clamping and slicing helpers.

## T5 - Where is rate limiting

Read only. Answer two questions:

1. Which file implements rate limiting?
2. How do you change the limit, and in how many ways?

A complete answer names the file, the constant, and the fact that the limit can
also be passed per instance. This task exists to show what unscoped exploration
costs: the answer lives in one file out of sixty.

## T6 - Missing null handling

`src/orderly/ingest/parser.py` and `src/orderly/ingest/validator.py`

Partners omit optional fields. The parser passes them through as `None`, and
the validator calls `len()` on them, so a record without `notes` raises
`TypeError` instead of validating cleanly. The bug spans both files; scoping to
one of them produces a defensive patch rather than a fix.

## T7 - Cover `currency.py`

`src/orderly/pricing/currency.py` sits at **52%** line coverage. Get it to
**95%** by adding tests, without changing the module.

```bash
make coverage
```

The uncovered branches are the ones nobody thinks about: zero-decimal
currencies, three-decimal currencies, the unsupported-currency error, and the
formatting and splitting helpers.

## T8 - Race in the cache warmer

`src/orderly/cache/warmer.py`

`CacheWarmer.warm` runs across a thread pool. Each key should be loaded exactly
once, however many workers are running and however often a key appears in the
input. It is not. Both `entries` and `load_count` are touched without
synchronization.

```bash
make task T=t8
```

This is the task that justifies a frontier model. The obvious fix, wrapping the
whole method in a lock, passes the tests and serializes the warm, defeating the
thread pool. Read the diff.

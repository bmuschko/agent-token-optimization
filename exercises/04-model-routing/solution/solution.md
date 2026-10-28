# Solution: Escalate and Compare

## What usually happens

Run B usually wins on cost at the same pass rate. The one published measurement of this policy is on the effort dial: Anthropic ran Claude Opus 5.5 on SWE-bench Pro at low effort with failures re-run at high, and it came out about 40% cheaper than everything at high, at a slightly better pass rate. On the model dial there is no published number; the ranking flips by workload, which is why the exercise measures rather than tells.

The escalations cluster on **T3**, because the refactor spans three files and has a structural acceptance test, and on **T8** if you add it, because a concurrency bug is genuinely hard. T1 and T4 almost never need a frontier model. T1 is one character.

## When Run B loses

It happens in most cohorts, to at least one person, and it is the most useful result in the room. Two causes:

1. **A task mix that is mostly hard.** Every cheap first attempt is a tax. If four of your six tasks escalate, you paid the cheap rate four times for nothing and the frontier rate anyway.
2. **Escalating mid-session.** Switching models rewrites the cached prefix at the cache-write rate, and on Copilot's production traffic the cache hit rate after a model switch was about 8%. Escalate as a fresh session.

If your B run lost, say what your mix looked like. The pattern is conditional, not universal, and the condition is worth more to the room than the result.

## Reference fixes

### T3, extract the retry logic

`utils/retry.py` already has `call_with_retry`. The three clients should use it rather than each hand-rolling the same loop:

```python
from orderly.utils.retry import call_with_retry

def charge(self, order_id: str, amount_cents: int, currency: str) -> dict:
    """Charge an order, retrying transient gateway failures."""
    return call_with_retry(
        lambda: self.transport.post(
            f"{GATEWAY_URL}/charges",
            {"order_id": order_id, "amount": amount_cents, "currency": currency},
        ),
        attempts=self.attempts,
        retry_on=TransientError,
    )
```

Shipping and inventory follow the same shape, one `call_with_retry` per method, and the `import time` goes with the loops.

The acceptance test is structural: it reads the source of all three modules and fails if any still contains a `for attempt in range(` loop or a direct `time.sleep(`. Behaviour is pinned separately by `tests/test_integrations.py`, which must stay green.

**Why agents get this wrong.** A cheap model given all three files will often write a new helper rather than find the existing one, leaving two retry implementations. The acceptance test catches the loops but not the duplication, so read the diff.

### T8, the cache warmer race

Not in the six, but it is the task that justifies a frontier model. The warmer checks `if key in self.entries` and then loads, with nothing holding the claim in between, so every worker clears the check before the first load finishes. `load_count` is also incremented without a lock.

The fix needs a lock and a claim taken *before* the slow work:

```python
def _warm_one(self, key: str) -> None:
    """Load a single key unless another worker already claimed it."""
    with self._lock:
        if key in self.entries or key in self._claimed:
            return
        self._claimed.add(key)
    value = self.loader(key)
    with self._lock:
        self.entries[key] = value
        self.load_count += 1
```

with the two attributes it relies on added in `__init__`:

```python
self._lock = threading.Lock()
self._claimed: Set[str] = set()
```

**Why cheap models fail this one.** The common wrong answer wraps the whole method in a lock, which is correct but serializes the warm and defeats the thread pool. The tests still pass. Only reading the diff catches it, which is the point: your test suite is a floor, not a proof.

## The routing table that comes out of this

| Task | Tier that was enough |
|---|---|
| T1 bug, one character | cheapest |
| T2 feature, one file | cheapest |
| T4 feature, two files | mid |
| T6 bug, two files | mid |
| T3 refactor, three files | mid, escalating on failure |
| T8 concurrency | frontier |

## Common wrong turns

- **Forgetting to reset between runs.** Run B starts from a clean tree. If you do not reset, B inherits A's work and looks free.
- **Giving a run one session.** One session per attempt, as in every other exercise. A single session for all of Run B cannot be split by task, and the escalation share disappears into the total.
- **Counting only successful attempts in Run B.** The failed cheap attempts are the cost of the strategy. Include them or the comparison is dishonest.
- **Declaring a winner from one task.** Six tasks is already a small sample. The number worth taking home is the pattern, not the percentage.

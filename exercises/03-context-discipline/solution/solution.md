# Solution: Scope It Down and Measure

## What the drop usually is

40 to 70%, with the three changes contributing roughly in this order:

| Change | Typical share of the saving |
|---|---|
| Naming the files instead of loading the repo | most of it |
| Starting a fresh session | a large chunk if the old session was long |
| Trimming the rules file | smallest per turn, compounding across turns |

People routinely guess the rules file is the big one because it is the thing
they can see. It is usually third. Say that out loud: the biggest lever is the
one that is hardest to notice, because nobody prints their file context.

## T3 reference fix

The bug spans two files, which is why scoping to one of them fails.

`parse_record` copies optional fields straight through, so an omitted `notes`
arrives as `None`. `_validate_text` then calls `len(None)` and raises
`TypeError` instead of a clean `ValidationError`.

Either file can own the fix. The cleaner one is the validator, because the
parser is right to preserve the difference between "absent" and "empty":

```python
def _validate_text(record: Dict[str, Any], field: str, limit: int) -> None:
    """Validate an optional free-text field against a length limit."""
    value = record.get(field)
    if value is None:
        return
    if len(value) > limit:
        raise ValidationError(field, f"must be {limit} characters or fewer")
```

A complete fixed file is in [validator.py](validator.py).

**The wrong fix** is to make the parser coerce `None` to `""`. It passes the
acceptance tests and quietly destroys information: downstream code can no
longer tell a partner who sent an empty note from one who sent none. If an
agent proposes it, that is a good moment to talk about tests as a floor.

## T5 reference fix

`list_orders` grows a `limit` and `offset`, using the helpers that already
exist in `utils/pagination.py`:

```python
from orderly.utils.pagination import clamp_limit, clamp_offset, page

def list_orders(self, query: Dict[str, Any] = None) -> Dict[str, Any]:
    query = query or {}
    orders = self.repository.all()
    if query.get("customer_id"):
        orders = [o for o in orders if o["customer_id"] == query["customer_id"]]
    if query.get("status"):
        orders = [o for o in orders if o["status"] == query["status"]]

    limit = clamp_limit(query.get("limit"))
    offset = clamp_offset(query.get("offset"))
    window = page(orders, limit, offset)
    return {
        "orders": window["items"],
        "total": window["total"],
        "limit": window["limit"],
        "offset": window["offset"],
        "has_more": window["has_more"],
    }
```

A complete fixed file is in [orders.py](orders.py).

**The discoverability point.** `utils/pagination.py` already does the clamping
and slicing, and an agent working from a scoped context will usually miss it
and write its own. That is the honest cost of scoping down, and it is worth
naming: context discipline is not free, it trades token cost for the risk of
reinventing something. The mitigation is one grep for `pagination` before you
start, not a bigger context window.

## The lean rules file

`CLAUDE.md` in this repo is about 90 lines, most of which earn nothing. A
version that keeps only the lines that change agent behaviour is in
[CLAUDE.lean.md](CLAUDE.lean.md). It is roughly a quarter of the size.

The test for a rules file line: **does it change behaviour you would otherwise
have to correct by hand?** If not, it is decoration you pay rent on, every turn,
for the life of the session.

Lines worth keeping in this repo:

- where the source lives and how to run the tests
- the rule that `make test` must stay green
- the fact that acceptance tests live outside the default test path

Lines worth cutting: the architecture essay, the style preferences your linter
already enforces, the history of the project, and the list of every directory.

## Common wrong turns

- **Compacting instead of starting fresh.** Compaction preserves a summary of
  the bloat. If your old session went down a dead end, a fresh session with a
  two-sentence problem statement beats a compacted one.
- **Editing `CLAUDE.md` mid-session.** It sits near the top of the prefix, so
  changing it invalidates the cache for everything after it. Finish the
  session first.
- **Scoping to one file on a two-file bug.** T3 spans parser and validator. An
  agent given only the validator will write a defensive `try/except` that hides
  the problem rather than fixing it.

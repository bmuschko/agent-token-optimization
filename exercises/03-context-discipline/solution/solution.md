# Solution: Scope It Down and Measure

## What the drop usually is

40 to 70%, with the three changes contributing roughly in this order. This is a judgment from the second look, how many files each run read, not something the two rows can separate:

| Change | Typical share of the saving |
|---|---|
| Naming the files instead of loading the repo | most of it |
| Starting a fresh session | a large chunk if the old session was long |
| Trimming the rules file | smallest per turn, compounding across turns |

People routinely guess the rules file is the big one because it is the thing they can see. It is usually third. Say that out loud: the biggest lever is the one that is hardest to notice, because nobody prints their file context.

## T6 reference fix

The bug spans two files, which is why scoping to one of them fails.

`parse_record` copies optional fields straight through, so an omitted `notes` arrives as `None`. `_validate_text` then calls `len(None)` and raises `TypeError` instead of a clean `ValidationError`.

Either file can own the fix. The cleaner one is the validator, because the parser is right to preserve the difference between "absent" and "empty":

```python
def _validate_text(record: Dict[str, Any], field: str, limit: int) -> None:
    """Validate an optional free-text field against a length limit."""
    value = record.get(field)
    if value is None:
        return
    if len(value) > limit:
        raise ValidationError(field, f"must be {limit} characters or fewer")
```

**The wrong fix** is to make the parser coerce `None` to `""`. It passes the acceptance tests and quietly destroys information: downstream code can no longer tell a partner who sent an empty note from one who sent none. If an agent proposes it, that is a good moment to talk about tests as a floor.

## The lean rules file

`CLAUDE.md` in this repo is 107 lines, about 1,100 tokens, most of which earn nothing. A version that keeps only the lines that change agent behaviour is in [CLAUDE.lean.md](CLAUDE.lean.md). It is roughly a quarter of the size.

The test for a rules file line: **does it change behaviour you would otherwise have to correct by hand?** If not, it is decoration you pay rent on, every turn, for the life of the session.

Lines worth keeping in this repo:

- where the source lives and how to run the tests
- the rule that `make test` must stay green
- the fact that acceptance tests live outside the default test path

Lines worth cutting: the architecture essay, the style preferences your linter already enforces, the history of the project, and the list of every directory.

## Common wrong turns

- **Compacting instead of clearing.** Compaction preserves a summary of the bloat. The overview prompt was a different task, so the move is `/clear`, which costs nothing. If a session went down a dead end, `/rewind` to before it; never compact one.
- **Editing `CLAUDE.md` mid-session.** Claude Code reads it once at startup, so the edit does not reach the agent until the next `/clear`, `/compact` or restart. Finish the session first, then trim.
- **Scoping to one file on a two-file bug.** T6 spans parser and validator. An agent given only the validator will write a defensive `try/except` that hides the problem rather than fixing it.

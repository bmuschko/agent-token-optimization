# Solution: Compaction, Memory and Your Plan

## What the delta usually is

Post-compaction turns typically cost 50 to 80% less than the turns immediately before, on a session that had run 30 or more turns. The saving is almost entirely on the input side, and almost entirely cache reads, because what you removed was transcript that was being resent every turn.

The saving shrinks the earlier you compact. That is not an argument for compacting late. A session compacted at turn 15 never reaches the cost of one compacted at turn 40, it just has less to show on the before-and-after.

## Compact, clear, or start fresh

| Situation | Do this |
|---|---|
| Same task, long session, history still relevant | **Compact** |
| New task, same repo | **Start fresh** |
| Agent is confused or looping | **Start fresh**, do not compact |
| Rules file needs an edit | Finish the session, then edit |
| Approaching the window limit | Compact **before** auto-compact fires |

Row three is the counterintuitive one and the one people get wrong. Compaction summarizes; it does not diagnose. A session that went down a dead end produces a summary of the dead end, and the agent carries the same wrong assumption into the next turn more cheaply.

Row five matters because auto-compact fires when the window is nearly full, which is the most expensive possible moment: every turn before it was billed at full length.

## A good memory note

Short, concrete, and about the codebase rather than the conversation:

```markdown
## Notes

- Retry logic belongs in `utils/retry.py`; the integration clients call it.
- Rate limiting is `api/middleware/rate_limit.py`, constant `WINDOW_REQUEST_LIMIT`.
- Acceptance tests are in `tests/tasks/`, excluded from the default pytest path.
- `make test` must stay green; it is the floor for every change.
```

## A bad memory note

```markdown
- We tried fixing the discount bug by changing the loop, then realised the
  thresholds were the problem, and after some back and forth we decided...
```

That is archaeology. It costs tokens on every future turn and tells the next session nothing it can act on.

## The trap worth repeating

A memory note added mid-session is itself a prefix change. You pay the 1.25x cache write on everything below it, immediately, and the saving only starts on the following turn. Write notes at session boundaries.

## Common wrong turns

- **Measuring the compaction turn itself.** `/compact` costs tokens; it has to read the conversation to summarize it. Measure the turns *after* it.
- **Compacting and then immediately pasting context back in.** People do this without noticing, usually by re-attaching the files they were working on.
- **Writing the plan after the session.** It does not happen. Write it now.

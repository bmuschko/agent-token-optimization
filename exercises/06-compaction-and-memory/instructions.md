# Exercise 6: Compaction, Memory and Your Plan

**Section 5 · 6 minutes · runs to the end of the session**

## Objective

Stop paying to replay stale history, and leave with a written plan rather than
a good feeling.

## Steps

1. **Take your longest session from today.** Probably the one from Exercise 2
   or 4.

2. **Compact it.**

   ```
   /compact
   ```

   Cursor and Copilot users: start a new chat seeded with a three-line summary
   of where you got to. Same effect, different button.

3. **Add a memory note to the rules file.** Two or three lines capturing what
   the agent learned that is worth keeping. Conclusions, not narration:

   > Retry logic lives in `utils/retry.py`. Rate limiting is
   > `api/middleware/rate_limit.py`, constant `WINDOW_REQUEST_LIMIT`.
   > Acceptance tests live in `tests/tasks/` and are excluded from `make test`.

4. **Run two or three more turns** and compare the burn against your
   pre-compaction turns.

5. **Fill in your 30/60/90** using [solution/30-60-90.md](solution/30-60-90.md)
   as the template. Do it now, in the session, not later.

## The plan is the deliverable

The measurement is repeatable at home. Fifteen minutes of honest reflection
about your own habits is not. If you only finish one of the two, finish the
plan.

## Done when

- A measured post-compaction delta
- A completed 30/60/90

## If you get stuck

- **The cost went up after adding the memory note.** You added it mid-session.
  The rules file sits near the top of the prefix, so changing it invalidates
  the cache for everything below. Write memory notes at a session boundary.
- **Compaction made the agent worse.** It was probably confused before you
  compacted, and compaction preserved the confusion in summary form. Start
  fresh with a two-sentence problem statement instead.
- **Replay mode.** `replays/compaction/` has a 40-turn session before and
  after.

The reference answers are in [solution/solution.md](solution/solution.md).

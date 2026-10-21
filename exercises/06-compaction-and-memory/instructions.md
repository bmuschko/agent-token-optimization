# Exercise 6: Compaction, Memory and Your Plan

**Section 5 · 6 minutes · runs to the end of the session**

## Objective

Stop paying to replay stale history, and leave with a written plan rather than a good feeling.

## Before you start

The proxy from Exercise 5 should still be running, and your agent still launched through it. `headroom doctor` confirms both; its `savings` row names how long ago the proxy last saw a request.

## Steps

1. **Take your longest session from today.** Probably the one from Exercise 2 or 4.

2. **Measure the burn before you compact.** Zero the ledger, run two or three ordinary turns, and read it:

   ```bash
   headroom savings --reset
   # two or three turns in the agent
   headroom savings          # N in "saved 0 / N tokens", divided by the turns
   ```

   That per-turn figure is your "before". It is the one number in the course you cannot reconstruct afterwards, so take it now.

   **Why the proxy here.** A turn's cost is dominated by the history resent with it, and that is precisely what compaction removes. `headroom savings` counts forwarded input per request, cached history included, so the per-turn figure moves exactly when the resent prefix shrinks. `ccusage` reports per session and `/context` per snapshot; neither shows a turn.

3. **Compact it.**

   ```
   /compact
   ```

   Cursor and Copilot users: start a new chat seeded with a three-line summary of where you got to. Same effect, different button.

4. **Add a memory note to the rules file.** Two or three lines capturing what the agent learned that is worth keeping. Conclusions, not narration:

   > Retry logic lives in `utils/retry.py`. Rate limiting is `api/middleware/rate_limit.py`, constant `WINDOW_REQUEST_LIMIT`. Acceptance tests live in `tests/tasks/` and are excluded from `make test`.

5. **Run two or three more turns** and measure them the same way:

   ```bash
   headroom savings --reset    # after /compact and the note, before the turns
   # two or three turns
   headroom savings
   ```

   Compare per turn against step 2. The first turn after the memory note carries a cache write for the changed rules file, so expect it to look worse; the second and third show the saving.

6. **Fill in your 30/60/90** using [solution/30-60-90.md](solution/30-60-90.md) as the template. Do it now, in the session, not later.

## The plan is the deliverable

The measurement is repeatable at home. Fifteen minutes of honest reflection about your own habits is not. If you only finish one of the two, finish the plan.

## Done when

- A measured post-compaction delta
- A completed 30/60/90

## If you get stuck

- **The cost went up after adding the memory note.** You added it mid-session. The rules file sits near the top of the prefix, so changing it invalidates the cache for everything below. Write memory notes at a session boundary.
- **Compaction made the agent worse.** It was probably confused before you compacted, and compaction preserved the confusion in summary form. Start fresh with a two-sentence problem statement instead.

The reference answers are in [solution/solution.md](solution/solution.md).

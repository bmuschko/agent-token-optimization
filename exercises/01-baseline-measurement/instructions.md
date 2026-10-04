# Exercise 1: Establish Your Baseline

**Section 1 · 6 minutes · work alone**

## Objective

Produce an honest, unoptimized number for two tasks. Every later result in
this course is measured against it.

## Before you start

- `headroom doctor` prints green. If it does not, see [TROUBLESHOOTING.md](../../TROUBLESHOOTING.md).
- Your agent is installed and signed in.
- You have [worksheet.csv](../../worksheet.csv) open, or a scratch file with the same columns.

## Steps

1. **Start the proxy and your agent together.**

   ```bash
   headroom wrap claude      # or: headroom wrap cursor | headroom wrap copilot
   ```

   Confirm traffic is actually routed before you trust any number:

   ```bash
   headroom doctor
   ```

2. **Work T1 and T2 exactly the way you normally would.** Open the files you
   would normally open. Use the model you normally use. Attach what you would
   normally attach.

   - **T1** Tier boundary off by one in `src/orderly/pricing/discount.py`
   - **T2** Add `--format json` to the CLI `report` command

   Full descriptions are in [TASKS.md](../../TASKS.md).

3. **Verify each task.** A task is done when its acceptance tests pass and the
   regression suite is still green:

   ```bash
   make task T=t1        # acceptance tests for T1
   make test             # regression suite, must stay green
   ```

4. **Record one worksheet row per task**: input tokens, output tokens, cache
   read, cache write, cost, attempts, tests pass. Read the numbers from
   `headroom stats`, or from your agent's own usage view.

5. **Post your combined total for T1 plus T2 in chat.**

## Do not optimize anything yet

This is the single most important instruction in the exercise. The temptation
to tidy your context before you measure is strong, and a flattering baseline
makes everything you do afterwards look worse than it is.

## Done when

- Two complete worksheet rows, including attempts and pass/fail
- A combined token total posted in chat

Tests passing is not required here. A failed baseline is still a baseline.

## If you get stuck

- **The token counter reads zero.** The proxy is running but your agent is not
  routed through it. Run `headroom doctor`.
- **You cannot run your agent live.** `export REPLAY_MODE=true` and work from
  `replays/baseline/`. Your absolute numbers will differ from a live run; the
  deltas you measure later still hold.
- **You are out of time.** A partial row is a usable baseline. Record what you
  have and move on.

The reference answers are in [solution/solution.md](solution/solution.md).
Read them after you have your own number, not before.

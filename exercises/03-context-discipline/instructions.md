# Exercise 3: Scope It Down and Measure

**Section 3 · 14 minutes · work alone**

This is the longest hands-on block in the course and the one with the biggest
payoff. Take the time.

## Objective

Cut the context on a task you already ran expensively, measure the drop, and
prove the task still passes.

## Before you start: the proxy enters here

This is the first exercise that needs per-request input-token counts for any
agent, which is what the Headroom proxy provides. In one terminal, at the
repository root, start it in passthrough mode so it measures without changing
anything:

```bash
headroom proxy --no-optimize
```

In a second terminal, also at the root, confirm it is up and launch your agent
through it:

```bash
headroom doctor                                     # proxy, readiness, version must pass
headroom wrap claude --no-proxy --project-settings  # or: codex | copilot | cursor
```

`doctor`'s `claude` row turns green only when run from the directory you
launched `wrap` in. The `savings` row, which names how long ago the proxy saw
a request, is the check that works from anywhere. If the launch misbehaves,
[TROUBLESHOOTING.md](../../TROUBLESHOOTING.md) covers the usual causes.

## Steps

1. **Pick T3 or T5**, whichever your agent handled expensively in Exercise 2.

   - **T3** A record with no `notes` blows up in the validator
   - **T5** `list_orders` returns everything, with no pagination

2. **Baseline run.** Reproduce your bloated version: same session, same
   attachments, same habits. Zero the ledger before you start and read it when
   the task is done:

   ```bash
   headroom savings --reset
   # work the task
   headroom savings          # N in "saved 0 / N tokens" is the bloated row
   ```

   If you have been working in one long session since Exercise 1, that session
   *is* your bloated version. Use it.

   **Why the proxy and not `ccusage` here.** The drop you are about to measure
   is in input tokens, nearly all of it the prefix resent on every turn: the
   rules file, the attachments, the history. `headroom savings` counts exactly
   that, forwarded input per request with cached history included, for any
   agent. `ccusage` prices a session, which is the right tool for money and the
   wrong one for a before-and-after on context size.

3. **Scoped run.** Start over, changing exactly three things:

   - **A fresh session.** Not `/compact`, a new one.
   - **Name the two or three files that matter** instead of loading the repo.
     For T3 that is `ingest/parser.py` and `ingest/validator.py`. For T5 it is
     `api/orders.py` and `utils/pagination.py`.
   - **Trim the rules file.** `CLAUDE.md` in this repo is deliberately
     overgrown. Cut it to what this task actually needs.

   Measure it the same way, so the two rows share a basis:

   ```bash
   headroom savings --reset
   # work the task in the fresh session
   headroom savings          # the scoped row
   ```

4. **Run the tests.**

   ```bash
   make task T=t3        # or T=t5
   make test             # must stay green
   ```

5. **Post three things in chat:** token drop as a percentage, pass or fail, and
   which of the three changes you think did the most work. The drop is
   `(bloated - scoped) / bloated`, both from the proxy.

## How to find the right files without reading everything

This is the question everyone asks. The answer is a throwaway search before the
real session, not a bigger context:

```bash
grep -rn "notes" src/orderly/ingest --include=*.py
```

One grep, one file list, then start the real session already knowing where to
look. The search costs almost nothing compared to letting the agent read its
way there.

## Done when

- Two runs recorded, with a measured delta
- The acceptance tests for your task pass
- `make test` is still green

A token drop with a red suite is a failed exercise, and a useful one. Say so
in chat if it happens to you.

## Expect

A drop between 40 and 70%. If you are over 90%, check your tests: you have
probably scoped away something the task needed.

## If you get stuck

- **You trimmed the rules file mid-session and the cost went up.** That is the
  prefix cache being invalidated. Edit the rules file *between* sessions.

The reference answers are in [solution/solution.md](solution/solution.md).

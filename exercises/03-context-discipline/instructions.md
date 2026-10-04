# Exercise 3: Scope It Down and Measure

**Section 3 · 14 minutes · work alone**

This is the longest hands-on block in the course and the one with the biggest
payoff. Take the time.

## Objective

Cut the context on a task you already ran expensively, measure the drop, and
prove the task still passes.

## Steps

1. **Pick T3 or T5**, whichever your agent handled expensively in Exercise 2.

   - **T3** A record with no `notes` blows up in the validator
   - **T5** `list_orders` returns everything, with no pagination

2. **Baseline run.** Reproduce your bloated version: same session, same
   attachments, same habits. Record the row.

   If you have been working in one long session since Exercise 1, that session
   *is* your bloated version. Use it.

3. **Scoped run.** Start over, changing exactly three things:

   - **A fresh session.** Not `/compact`, a new one.
   - **Name the two or three files that matter** instead of loading the repo.
     For T3 that is `ingest/parser.py` and `ingest/validator.py`. For T5 it is
     `api/orders.py` and `utils/pagination.py`.
   - **Trim the rules file.** `CLAUDE.md` in this repo is deliberately
     overgrown. Cut it to what this task actually needs.

4. **Run the tests.**

   ```bash
   make task T=t3        # or T=t5
   make test             # must stay green
   ```

5. **Post three things in chat:** token drop as a percentage, pass or fail, and
   which of the three changes you think did the most work.

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
- **Replay mode.** `replays/scoped/` has a bloated and a scoped run of T3.

The reference answers are in [solution/solution.md](solution/solution.md).

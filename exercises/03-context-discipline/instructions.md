# Exercise 3: Scope It Down and Measure

**Section 3 · 14 minutes · work alone**

This is the longest hands-on block in the course and the one with the biggest
payoff. Take the time.

## Objective

Exercise 2 showed where the money goes: into context the agent did not need,
resent with every request. This exercise cuts that context on one task,
measures the drop, and proves the task still passes.

## Before you start

Nothing new to install. The task is T3, which none of the earlier tasks
touched, so the fixes from Exercises 1 and 2 can stay in the working tree.

Two things to know before the first session:

- The rules file is edited **between** sessions, never during one. It sits
  near the top of every request, and changing it mid-session invalidates the
  prompt cache for everything after it.
- After each run, `git status`. The agent may have touched more than the two
  files the task names, and that is part of the run's cost.

## The measurement

The drop you are after is in input tokens, nearly all of it the prefix resent
with every request: the rules file, the files the agent loaded, the history.
On a `ccusage` row that is Input plus Cache Create plus Cache Read, the same
row Exercise 1 read, so the instrument is the same: one session per run, found
by its id. The drop is computed on Total Tokens, which adds the small output
figure to those three. It is close enough to the input-side drop that the
distinction does not matter here.

`ccwhy session` is the second look, and here it answers the question the
exercise ends on: which change did the work. Its per-turn table shows the
prefix shrinking, and its tool-call count shows how many files the agent read
on its own.

Cursor and Copilot users: your usage dashboard, one session per run.

## Steps

1. **Look at the starting line, in a second terminal.**

   ```bash
   make task T=t3        # expect: 2 failed, 1 passed
   ```

   A record without `notes`, or with `notes` set to `None`, raises
   `TypeError` instead of validating. The third test, that over-long notes
   are still rejected, passes now and must keep passing.

2. **The bloated run.** Reproduce the expensive habits deliberately: load a
   large slice of the repo, carry that history into the task, keep the
   overgrown rules file.

   ```bash
   id=$(uuidgen | tr 'A-Z' 'a-z')
   claude --session-id "$id"
   ```

   Two prompts, in this order. The first manufactures the history a long
   session would have:

   > Walk me through how an inbound partner feed is processed, from
   > `src/orderly/ingest` to the API.

   Then the task, with no file names:

   > Partners sometimes omit optional fields such as `notes`. A record without
   > `notes` currently raises `TypeError` during validation instead of
   > validating cleanly. Fix it.

   When it says it is done, verify in the second terminal, then `/exit` and
   read the row:

   ```bash
   make task T=t3
   make test
   ```

   ```bash
   COLUMNS=200 npx ccusage@latest session | grep -E "^│ Session|${id:0:8}"
   ccwhy session "$id"
   ```

   Record the row as `T3,bug,bloated`, with `attempts` and `tests_pass`, and
   keep the `ccwhy` output. Then put the task back for the second run:

   ```bash
   git checkout -- src/orderly/ingest
   make task T=t3        # red again
   ```

3. **Change three things between the sessions.**

   - **Trim the rules file.** `CLAUDE.md` in this repo is deliberately
     overgrown. Cut it to what this task needs: where the source and tests
     live, how to run them, the rule that `make test` must stay green. Do not
     commit it; `git checkout CLAUDE.md` restores it whenever you want.
   - **Find the files with one search instead of a session.**

     ```bash
     grep -rn "notes" src/orderly/ingest --include='*.py'
     ```

     One grep, one file list, and you start the next session already knowing
     where to look. Both `parser.py` and `validator.py` are in it, and the
     task needs both.
   - **A fresh session**, which the loop gives you anyway. No overview prompt
     this time.

4. **The scoped run.** New id, and a prompt that names the files:

   ```bash
   id=$(uuidgen | tr 'A-Z' 'a-z')
   claude --session-id "$id"
   ```

   > A record without `notes` raises `TypeError` in the validator instead of
   > validating cleanly. `src/orderly/ingest/parser.py` passes omitted
   > optional fields through as `None`, and `src/orderly/ingest/validator.py`
   > calls `len()` on them. Fix it so a missing or `None` optional field
   > validates, while over-long notes are still rejected. Only those two
   > files should change.

   Verify, `/exit`, read the row the same way, and record it as
   `T3,bug,scoped`.

5. **Compare.**

   ```
   drop = (bloated Total Tokens - scoped Total Tokens) / bloated Total Tokens
   ```

   Then put the two `ccwhy session` outputs side by side. The per-turn table
   shows how much each request resent, and "Tools Used" shows how many files
   the agent read on its own in each run. That is the evidence for which of
   the three changes did the most work.

6. **If time permits, scope T1 as well.** You have its baseline from Exercise
   1. Put the bug back with `git checkout -- src/orderly/pricing/discount.py`,
   run it once more in a fresh session with the trimmed rules file and a
   prompt that names the file, and record `T1,bug,scoped`. One-character
   fixes are where scoping gains the least in absolute terms and the most as
   a percentage, which is worth seeing once.

7. **Post three things in chat:** the drop as a percentage, pass or fail, and
   which of the three changes you think did the most work.

## Done when

- `T3,bug,bloated` and `T3,bug,scoped` recorded, with a drop
- The scoped run's acceptance tests pass and `make test` is still green

A token drop with a red suite is a failed exercise, and a useful one. Say so
in chat if it happens to you.

## Expect

A drop between 40 and 70%. If you are over 90%, check your tests: you have
probably scoped away something the task needed.

## If you get stuck

- **You trimmed the rules file mid-session and the cost went up.** That is the
  prefix cache being invalidated. Edit the rules file *between* sessions.
- **The scoped run changed only one file.** T3 spans parser and validator. An
  agent shown only the validator writes a defensive patch that hides the
  problem. A fix that passes `make task T=t3` but leaves the parser alone is
  worth reading closely.
- **You reset `src/orderly/ingest` and the tests are still green.** The agent
  fixed it somewhere else. `git status` shows where.

The reference answers are in [solution/solution.md](solution/solution.md).

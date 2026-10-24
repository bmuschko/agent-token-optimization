# Exercise 3: Scope It Down and Measure

**Section 3 · 14 minutes · work alone**

This is the longest hands-on block in the course and the one with the biggest payoff. Take the time.

## Objective

Exercise 2 showed where the money goes: into context the agent did not need, resent with every request. This exercise cuts that context on one task, measures the drop, and proves the task still passes.

## Before you start

Nothing new to install. The task is T6, which none of the earlier tasks touched, so the fixes from Exercises 1 and 2 can stay in the working tree.

Two things to know before the first session:

- The rules file is edited **between** sessions. Claude Code reads it once at session start and holds it, so an edit during a session reaches the agent only at the next `/clear`, `/compact` or restart. Trim it after the first session ends and before the second begins, and the second session starts with the lean file.
- After each run, `git status`. The agent may have touched more than the two files the task names, and that is part of the run's cost.

## The measurement

The drop you are after is in input tokens, nearly all of it the prefix resent with every request: the rules file, the files the agent loaded, the history. On a tokscale row that is Input plus Cache write plus Cache read, the same row Exercise 1 read, so the instrument is the same: one session per run, read exactly as you read T1. The drop is computed on the total of all four token columns, output included; output is small enough that this is the input-side drop for practical purposes.

Note one more figure per run, the **cache read share**: Cache read divided by Input plus Cache read plus Cache write. Section 3 argued that a stable prefix turns full-price input into cheap cache reads; this is where you see whether yours did. Copilot in VS Code rows have no cache columns, so skip the share there.

The second look is the per-agent view from Exercise 2: `ccwhy session "$id"` on Claude Code, `scripts/copilot_session.py` on Copilot CLI, Agent Session Viewer in VS Code, the transcript folder in Cursor. It shows how many files each run read on its own, which is the evidence for the question the exercise ends on.

## Steps

1. **Look at the starting line, in a second terminal.**

   ```bash
   make task T=t6        # expect: 2 failed, 1 passed
   ```

   A record without `notes`, or with `notes` set to `None`, raises `TypeError` instead of validating. The third test, that over-long notes are still rejected, passes now and must keep passing.

2. **The bloated run.** Reproduce the expensive habits deliberately: load a large slice of the repo, carry that history into the task, keep the overgrown rules file.

   ```bash
   id=$(uuidgen | tr 'A-Z' 'a-z')
   claude --session-id "$id"
   ```

   Two prompts, in this order. The first manufactures the history a long session would have:

   > Walk me through how an inbound partner feed is processed, from `src/orderly/ingest` to the API.

   Then the task, with no file names:

   > Partners sometimes omit optional fields such as `notes`. A record without `notes` currently raises `TypeError` during validation instead of validating cleanly. Fix it.

   When it says it is done, verify in the second terminal, then `/exit` and read the row:

   ```bash
   make task T=t6
   make test
   ```

   ```bash
   npx tokscale@latest --json --no-spinner --today --group-by client,session,model \
     | uv run python scripts/session_row.py "$id"
   ```

   Other agents read the row as in Exercise 1: list before and after. Note it as the bloated run, with the cache read share. Add your attempts, the number of times you sent the agent back after a red test, and whether both commands ended green. Neither comes from a tool. Take the second look now too, `ccwhy session "$id"` on Claude Code or your agent's view from Exercise 2, and keep it for step 5; nothing from it goes into the comparison. Then put the task back for the second run:

   ```bash
   git checkout -- src/orderly/ingest
   make task T=t6        # red again
   ```

3. **Change three things between the sessions.**

   - **Trim the rules file.** `CLAUDE.md` in this repo is deliberately overgrown. Cut it to what this task needs: where the source and tests live, how to run them, the rule that `make test` must stay green. Do not commit it; `git checkout CLAUDE.md` restores it whenever you want.
   - **Find the files with one search instead of a session.**

     ```bash
     grep -rn "notes" src/orderly/ingest --include='*.py'
     ```

     One grep, one file list, and you start the next session already knowing where to look. Both `parser.py` and `validator.py` are in it, and the task needs both.
   - **A fresh session**, which the loop gives you anyway. No overview prompt this time.

4. **The scoped run.** New id, and a prompt that names the files:

   ```bash
   id=$(uuidgen | tr 'A-Z' 'a-z')
   claude --session-id "$id"
   ```

   > A record without `notes` raises `TypeError` in the validator instead of validating cleanly. `src/orderly/ingest/parser.py` passes omitted optional fields through as `None`, and `src/orderly/ingest/validator.py` calls `len()` on them. Fix it so a missing or `None` optional field validates, while over-long notes are still rejected. Only those two files should change.

   Verify, `/exit`, read the row the same way, and note it as the scoped run with its own cache read share, attempts and test result.

5. **Compare.**

   ```
   total = Input + Output + Cache read + Cache write
   drop  = (bloated total - scoped total) / bloated total
   ```

   Then compare the cache read shares, and put the two second looks side by side: how many files did each run read on its own? That is the best evidence you have for which of the three changes did the most work. It is evidence, not a measurement: you changed three things between the runs, so the answer you post in step 7 is a judgment, and the solution says what it usually is.

6. **If time permits, scope T1 as well.** You have its baseline from Exercise
   1. Put the bug back with `git checkout -- src/orderly/pricing/discount.py`, run it once more in a fresh session with the trimmed rules file and a prompt that names the file, and note it next to the baseline. One-character fixes are where scoping gains the least in absolute terms and the most as a percentage, which is worth seeing once.

7. **Post three things in chat:** the drop as a percentage, pass or fail, and which of the three changes you think did the most work.

## Done when

- The bloated and scoped T6 runs noted, with a drop
- The scoped run's acceptance tests pass and `make test` is still green

A token drop with a red suite is a failed exercise, and a useful one. Say so in chat if it happens to you.

## Expect

A drop between 40 and 70%. If you are over 90%, check your tests: you have probably scoped away something the task needed.

## If you get stuck

- **You trimmed the rules file mid-session and nothing changed.** Claude Code read it once at startup and is still holding the long version. Finish the session; the scoped run starts with the trimmed file.
- **The scoped run changed only one file.** T6 spans parser and validator. An agent shown only the validator writes a defensive patch that hides the problem. A fix that passes `make task T=t6` but leaves the parser alone is worth reading closely.
- **You reset `src/orderly/ingest` and the tests are still green.** The agent fixed it somewhere else. `git status` shows where.

The reference answers are in [solution/solution.md](solution/solution.md).

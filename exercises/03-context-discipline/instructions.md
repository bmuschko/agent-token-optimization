# Exercise 3: Scope It Down and Measure

**Section 3 · 14 minutes · work alone**

This is the longest hands-on block in the course and the one with the biggest payoff. Take the time.

## Objective

Exercise 2 showed where the money goes: into context the agent did not need, resent with every request. This exercise cuts that context on one task, measures the drop, and proves the task still passes.

## Before you start

Nothing new to install. The task is T6, which none of the earlier tasks touched, so the fixes from Exercises 1 and 2 can stay in the working tree.

Two things to know before the first session:

- The rules file is edited **between** sessions. Claude Code reads it once at session start and holds it, so an edit during a session reaches the agent only at the next `/clear`, `/compact` or restart. Trim it after the second session ends and before the third begins, so the lean run is the only one that starts with the lean file.
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

   When it says it is done, verify in the second terminal:

   ```bash
   make task T=t6
   make test
   ```

   Back in the session, run `/context` and note the Memory files figure, which is the rules file as the agent holds it. Then `/exit` and read the row:

   ```bash
   npx tokscale@latest --json --no-spinner --today --group-by client,session,model \
     | uv run python scripts/session_row.py "$id"
   ```

   Other agents read the row as in Exercise 1: list before and after. Note it as the **bloated run**, with the cache read share and the Requests figure. Add your attempts, the number of times you sent the agent back after a red test, and whether both commands ended green. Neither comes from a tool. Take the second look now too, `ccwhy session "$id"` on Claude Code or your agent's view from Exercise 2, and keep it for step 5; nothing from it goes into the comparison. Then put the task back:

   ```bash
   git checkout -- src/orderly/ingest
   make task T=t6        # red again
   ```

3. **The scoped run: change the prompt, keep the rules file.** Find the files with one search instead of a session:

   ```bash
   grep -rn "notes" src/orderly/ingest --include='*.py'
   ```

   One grep, one file list, and you start the next session already knowing where to look. Both `parser.py` and `validator.py` are in it, and the task needs both. New id, fresh session, no overview prompt this time:

   ```bash
   id=$(uuidgen | tr 'A-Z' 'a-z')
   claude --session-id "$id"
   ```

   Now use the following prompt, or something close to it:

   > A record without `notes` raises `TypeError` in the validator instead of validating cleanly. `src/orderly/ingest/parser.py` passes omitted optional fields through as `None`, and `src/orderly/ingest/validator.py` calls `len()` on them. Fix it so a missing or `None` optional field validates, while over-long notes are still rejected. Only those two files should change.

   Verify, `/exit`, read the row the same way, and note it as the **scoped run** with its own cache read share, Requests, attempts and test result. Keep the prompt; the next run sends it again. Put the task back once more:

   ```bash
   git checkout -- src/orderly/ingest
   ```

4. **The lean run: trim the rules file, same prompt.** `CLAUDE.md` in this repo is deliberately overgrown. Cut it to what this task needs: where the source and tests live, how to run them, the rule that `make test` must stay green. Do not commit it; `git checkout CLAUDE.md` restores it whenever you want.

   New id, fresh session, and the prompt from step 3 word for word. Verify, run `/context` and note the Memory files figure again, `/exit`, read the row, and note it as the **lean run**.

5. **Compare and attribute.** Three runs and two changes, so each difference is one change:

   ```
   total  = Input + Output + Cache read + Cache write
   drop   = (bloated total - lean total) / bloated total
   prompt = bloated total - scoped total     # naming the files, no overview history
   rules  = scoped total - lean total        # trimming CLAUDE.md
   ```

   What each run should have produced:

   - **The scoped run, step 3, is where the drop happens.** Expect its total at a fraction of the bloated run's, with fewer Requests, a second look that shows one or two file reads instead of a walk through the package, and both commands green. Almost the entire drop is in this difference.
   - **The lean run, step 4, is a small step below the scoped run.** Trimming saves the same number of tokens on every request, so the saving is the two Memory files figures apart, times the lean run's Requests. With a thousand tokens trimmed and five requests, that is five thousand tokens, a few percent of the drop. Expect the same Requests figure as the scoped run, since only the rules file changed, and both commands green. If the rules figure is far from that prediction, the two runs differed in something else; compare their Requests and their second looks.

   The dollar share of the rules file is smaller than its token share: after the first request it sits in the cached prefix at a tenth of the price.

   The prompt figure is two changes in one, naming the files and dropping the overview history. The second looks separate them roughly: the bloated run's per-turn table shows what the overview cost on its own and how much history every later request carried, and its file reads show what the vague prompt made the agent open. Then compare the cache read shares across the three runs.

## Done when

- Three T6 runs noted, with the drop split between the prompt and the rules file
- The lean run's acceptance tests pass and `make test` is still green

A token drop with a red suite is a failed exercise, and a useful one. Say so in chat if it happens to you.

## Expect

A drop between 40 and 70%, nearly all of it from the prompt. The rules file comes to a few percent of the tokens and less of the cost, which is the opposite of what most people guess. If you are over 90%, check your tests: you have probably scoped away something the task needed.

## If you get stuck

- **You trimmed the rules file mid-session and nothing changed.** Claude Code read it once at startup and is still holding the long version. Finish the session; the lean run starts with the trimmed file.
- **The scoped or lean run changed only one file.** T6 spans parser and validator. An agent shown only the validator writes a defensive patch that hides the problem. A fix that passes `make task T=t6` but leaves the parser alone is worth reading closely.
- **You reset `src/orderly/ingest` and the tests are still green.** The agent fixed it somewhere else. `git status` shows where.

The reference answers are in [solution/solution.md](solution/solution.md).

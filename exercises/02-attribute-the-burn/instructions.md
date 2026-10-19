# Exercise 2: Break Down Your Burn

**Section 2 · 10 minutes · work alone**

## Objective

Exercise 1 gave you a total. This exercise turns it into an attribution. By
the end you will know which *kind* of work costs you the most per completed
task, and which single controllable thing is your biggest sink.

## Before you start

Nothing new to install, and nothing to reset. The T1 and T2 fixes from
Exercise 1 can stay in the working tree; the tasks below do not touch the
same files. Their rows are already on the worksheet, and this exercise reuses
T1 as its bug fix.

One habit to adopt from here on: after every agent run, look at `git status`
before you record the row. Agents touch more than the file the task names,
sometimes helpfully and sometimes not, and whatever they touched is part of
what the run cost.

## Steps

1. **Run three more tasks, one of each remaining kind.** In any order:

   | Task | Kind | What it is | Done when |
   |---|---|---|---|
   | T4 | refactor | extract the duplicated retry logic into the existing helper | `make task T=t4` and `make test` green |
   | T5 | feature | `limit` and `offset` pagination on `list_orders` | `make task T=t5` and `make test` green |
   | T7 | exploration | where is rate limiting, and how do I change the limit | an answer naming the file, the constant, and the second way to change it |

   T7 is read-only. You are paying for an answer, not a diff. Full
   descriptions are in [TASKS.md](../../TASKS.md).

   If you want a starting point, these are enough for the agent to do each
   task. Your own wording is still the point.

   > **T4** The same retry loop with exponential backoff is copy-pasted into
   > the methods of `src/orderly/integrations/payments.py`, `shipping.py` and
   > `inventory.py`. `src/orderly/utils/retry.py` already has a
   > `call_with_retry` helper that nothing uses. Replace the inline loops
   > with it, without changing behaviour.

   > **T5** `list_orders` in `src/orderly/api/orders.py` returns every order.
   > Add `limit` and `offset` parameters, and include `total` and `has_more`
   > in the response. `src/orderly/utils/pagination.py` already has the
   > clamping and slicing helpers.

   > **T7** Where is rate limiting implemented in this codebase, and how do I
   > change the limit? In how many ways can it be changed?

   T7's prompt is unscoped on purpose. What an unconstrained search costs is
   the finding; the cheap way to ask is Section 3's lesson.

   Each task is a session of its own, as in Exercise 1, with one change at
   the end. This exercise only needs the money, so ask `ccusage` for the
   session's totals rather than its full row:

   ```bash
   id=$(uuidgen | tr 'A-Z' 'a-z')
   claude --session-id "$id"
   # work the task, verify in this terminal, /exit
   npx ccusage@latest session --id "$id"      # the number for the row
   ccwhy session "$id"                        # where the session went
   ```

   Four lines come back, and the first is the one you record:

   ```
   Claude Code Session Usage - f5ba87fa-0e08-4d37-b6f1-93393ac5d35e
   Total Cost: $0.47
   Total Tokens: 109,012
   Total Entries: 3
   ```

   `--id` needs the full id, which is why it takes `$id` rather than the
   eight-character prefix the `grep` used; given a prefix it prints nothing
   and exits cleanly, so an empty result means a truncated id, not a missing
   session.

   `ccwhy session` is the second look, and it is where the attribution
   becomes visible: a per-turn table of what each request resent, and a
   count of tool calls. On an exploration task, watch the cache reads grow
   with every turn and count the files the agent read to answer one
   question.

   **The two tools will not agree, and `ccusage` is the one that is right.**
   Claude Code writes one log entry per content block of a response, so a
   response made of a thinking block, a text block and a tool call is logged
   three times, each copy carrying the response's full usage. `ccusage`
   deduplicates by message id. `ccwhy` sums every entry, so its totals run
   1.5 to 2.5 times high depending on how many blocks each response had, its
   per-turn table lists entries rather than requests, with the duplicates
   visibly identical, and it prices with its own flat rates on top. Use it
   for the shape: which turns resent the most, how many files were read.
   Every number on the worksheet comes from `ccusage`.

   Same habits as the baseline. This is still a measurement of how you work
   today, not of how well you can do when you try.

2. **Record `cost_usd`, `attempts` and `tests_pass`** into the `T4`, `T5` and
   `T7` baseline rows. The token columns can stay empty on these rows; the
   two questions below are answered in money and in what the window is made
   of, not in tokens per task. For T7, `tests_pass` means the answer was
   complete.

   Then fill `cost_per_completed_task` for all four kinds, T1 included. With
   one task per kind the arithmetic is short. A task that passed costs its
   row's `cost_usd`, failed attempts included. A task that never passed has
   no completion to divide by, which makes it the most expensive kind by
   definition.

3. **Find the controllable sink.** Two instruments, one question each.

   **What every request is made of.** Inside any Claude Code session:

   ```
   /context
   ```

   It lists the window by category. Map it to the definition below: Memory
   files is your rules file, MCP tools and Skills are your tool definitions,
   Messages is file context and history. System prompt and System tools are
   the vendor's. The largest of *your* categories is your sink.

   **Where it went, across sessions.** In the terminal:

   ```bash
   ccwhy                                  # full report, last 30 days
   ccwhy sessions                         # sessions by cost, with their project
   npx ccusage@latest daily --breakdown   # spend per day, per model
   ```

   `ccwhy`'s "Controllable Token Sinks" section ranks what you can reduce and
   files cache reads under "Fixed Overhead". Note what it lumps: its top
   sink, "Cache creation (CLAUDE.md, MCP, system prompt)", mixes your rules
   file and tools with the vendor's prompt. `/context` is how you split that.

   Its totals are inflated for the reason given in step 1, so use it to rank
   sessions against each other and to name sinks, not for figures. Worksheet
   numbers always come from `ccusage`.

   Cursor and Copilot users: your product's usage dashboard, see
   [INSTALL.md](../../INSTALL.md#usage-analyzers).

   **Why these and not the proxy.** This is an attribution question, by task
   kind and by habit. The proxy counts tokens on the wire and knows nothing
   about which session or task sent them, or what the window was made of.
   `ccusage` prices each session, output included. `/context` shows the
   window's composition. `ccwhy` ranks sessions and names the sinks. Together
   they answer how much, made of what, and why.

4. **Answer two questions in chat:**
   - Which **kind** of task cost you the most per completed task?
   - What is your single biggest **controllable** token sink?

## What "controllable" means

You cannot shrink your vendor's system prompt. You can shrink your rules file,
your tool definitions, your file context and your session history. Only the
second group counts.

## Done when

- Four kinds with a cost per completed task: three new rows plus T1
- A named most-expensive kind of task
- A named controllable sink

## If you get stuck

- **Three tasks in ten minutes is tight.** Two measured honestly beats three
  rushed. Drop T4 first; it is the slowest, and T1, T5 and T7 still give you
  three kinds.
- **`ccwhy` reports nothing.** It reads `~/.claude/projects/`, so it only
  sees Claude Code sessions. Cursor and Copilot users use their dashboards.
- **`/context` shows MCP tools at 0 tokens.** Your tools are loading on
  demand, and the deferred figure is listed separately. Section 5 is about
  exactly that.

The reference answers are in [solution/solution.md](solution/solution.md).

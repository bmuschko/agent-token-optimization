# Exercise 2: Break Down Your Burn

**Section 2 · 10 minutes · work alone**

## Objective

Stop looking at a total and start looking at an attribution. By the end you
will know which *kind* of work costs you the most, and which single
controllable thing is your biggest sink.

## Before you start

Your agent is still routed through the proxy from Exercise 1. If you restarted
anything, run `headroom doctor` again.

## Steps

1. **Run four tasks of four different kinds.** One of each, in any order:

   | Task | Kind | What it is |
   |---|---|---|
   | T1 | bug fix | tier boundary in `discount.py` |
   | T5 | feature | pagination on `list_orders` |
   | T4 | refactor | extract the duplicated retry logic |
   | T7 | exploration | where is rate limiting, and how do I change the limit |

   T7 is read-only. You are looking for an answer, not a diff.

2. **Record a worksheet row for each**, tagged with its kind.

3. **Run the analyzers.**

   ```bash
   npx ccusage@latest session          # how much did I spend
   npx ccusage@latest daily --breakdown
   claude-usage-analyzer               # why did I spend it
   ```

   Cursor and Copilot users: substitute your own dashboard. See
   [INSTALL.md](../../INSTALL.md#usage-analyzers) for what each tool reports
   and what the substitutes are.

4. **Answer two questions in chat:**
   - Which **kind** of task cost you the most per completed task?
   - What is your single biggest **controllable** token sink?

## What "controllable" means

You cannot shrink your vendor's system prompt. You can shrink your rules file,
your tool definitions, your file context and your session history. Only the
second group counts.

## Done when

- Four worksheet rows, each tagged with its kind
- A named most-expensive kind of task
- A named controllable sink

## If you get stuck

- **Four tasks in ten minutes is tight.** Three measured honestly beats four
  rushed. Drop T4 first; it is the slowest.
- **`claude-usage-analyzer` reports nothing.** It reads `~/.claude/projects/`,
  so it only sees Claude Code sessions. Cursor and Copilot users should use
  their dashboards instead.
- **Replay mode.** `replays/mixed-tasks/` has all four kinds pre-run.

The reference answers are in [solution/solution.md](solution/solution.md).

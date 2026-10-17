# Exercise 1: Measure Your Baseline

**Section 1 · 6 minutes · work alone**

## What a baseline is

Every later exercise changes one thing about how your agent works and asks
whether the bill went down. "Down from what" is this exercise.

The baseline is the total your agent spends to take one task from red tests
to green, using the habits you have today, with nothing optimized. Not one
request: the sum of every request the agent makes along the way. Each request
resends the entire context as input tokens: the system prompt, the tool
definitions, the rules file, every file the agent has read, the conversation
so far. So a task costs roughly

```
requests × context size per request
```

Later exercises shrink one factor or the other. This one records the product
before you touch either.

You will measure two tasks and record one row each in
[worksheet.csv](../../worksheet.csv):

| Column | What it is |
|---|---|
| `input_tokens` | everything the agent sent, summed over all requests |
| `output_tokens` | everything the model wrote back |
| `cache_read` | the part of the input served from the prompt cache, at a tenth of the price |
| `cache_write` | the part written into the cache, at 1.25 times the price |
| `cost_usd` | the four above, priced |
| `attempts` | how many times you sent the agent back after a red test |
| `tests_pass` | whether both test commands ended green |

`cost_usd` covers every attempt, the failed ones included. A fix that took
three tries cost three tries, and that is the number that goes on the row.

Input will dwarf output by an order of magnitude. That is normal. Input is
where the volume lives, and it is the lever the rest of the course pulls.

## The tool, and why

**Claude Code: `ccusage`.** Claude Code writes the usage figures the API
returns for every request into its session logs under `~/.claude/projects/`.
Those are the numbers Anthropic bills on. `ccusage` reads them and prints one
line per session with every column above. Nothing to install, nothing to
route, nothing to reset:

```bash
npx ccusage@latest session
```

Because it reports per session, you run **one fresh session per task**. One
line is then one task.

Why not the alternatives, one line each. `/context` shows what is in the
window right now, not what a task cost in total. `/cost` only reports on
API-key billing, not on subscription plans. The Headroom proxy counts tokens
on the wire for any agent, but it reports savings rather than spend, never
sees output tokens, and keeps one cumulative ledger. It earns its setup in
Exercise 3, where you need per-request detail. Not here.

**Cursor and GitHub Copilot:** your product's usage dashboard, read per
session. Copilot's per-request view is only in the VS Code Chat Debug View.

A note on the dollar figure. `ccusage` prices tokens at API list rates. On a
subscription plan you did not pay that amount, but it is the right unit for
comparison, and it is the same unit on every later row.

## Steps

Run every command from the repository root. The tests need the Makefile
there, and the agent needs `src/` inside its working directory.

1. **Look at the starting line, in a second terminal.** Before the agent
   touches anything, see the failure you are about to pay to fix:

   ```bash
   make task T=t1        # expect: 3 failed, 1 passed
   ```

   It fails at exactly the boundaries the task describes, $100.00, $500.00
   and $5,000.00, each landing one tier too low. That is the before.

   This run is not an attempt and costs no tokens. Whether you paste its
   output into your prompt is part of your habits: do what you would normally
   do.

2. **Start a fresh session for T1, with an id you chose.** In your terminal,
   at the repository root:

   ```bash
   id=$(uuidgen | tr 'A-Z' 'a-z')
   claude --session-id "$id"
   ```

   `ccusage` identifies sessions by id and nothing else, so picking the id
   yourself is what lets step 5 find this session's row no matter what other
   sessions are open. Keep using this terminal; `$id` has to still be there
   after you exit. PowerShell: `$id = [guid]::NewGuid().ToString()`.

   Fresh means a new session: not `--resume`, and not `/clear` inside an old
   one. It must start empty so that its totals are T1 and nothing else.

3. **Work T1 the way you normally would.** The task, from
   [TASKS.md](../../TASKS.md): the volume discount tiers in
   `src/orderly/pricing/discount.py` are documented as inclusive of their
   thresholds, but an order of exactly $100.00 does not get the 5% rate.

   Phrase the prompt as you naturally would; your own wording is the point.
   If you want a starting point, this is enough for the agent to find and fix
   the bug:

   > The volume discount tiers in `src/orderly/pricing/discount.py` are
   > supposed to be inclusive of their thresholds, but an order of exactly
   > $100.00 doesn't get the 5% rate. Fix the off-by-one bug.

   Use the model you normally use. Let the agent open whatever it normally
   opens, including files it only looks at. Do not scope it tighter than
   usual, and do not read the solution first. It contains the fix, and
   knowing the fix changes how you prompt, which is the one thing this
   exercise cannot recover from.

4. **Verify, in a second terminal.** When the agent says it is done:

   ```bash
   make task T=t1        # acceptance tests for T1
   make test             # regression suite, must stay green
   ```

   Both green: T1 is done. Either red: go back to the agent, tell it what
   failed, and add one to `attempts`. Run these yourself rather than asking
   the agent to. The agent running them puts the output into the context you
   are measuring.

5. **End the session and read the line.** In the agent, `/exit`. Back in the
   same terminal, `$id` is the session you just left; pull its row:

   ```bash
   COLUMNS=200 npx ccusage@latest session | grep -E "^│ Session|${id:0:8}"
   ```

   That prints the header and your row. This one is a real T1 run on a
   frontier model, five requests end to end; your numbers will differ, the
   shape is what to recognize:

   ```
   │ Session      │ Agent  │ Models      │ Input │ Output │ Cache Create │ Cache Read │ Total Tokens │ Cost (USD) │
   │ f5ba87fa-... │ Claude │ - fable-5-1 │    66 │    643 │       20,760 │     87,543 │      109,012 │      $0.47 │
   ```

   Copy Input, Output, Cache Create, Cache Read and Cost into the
   `T1,bug,baseline` row as `input_tokens`, `output_tokens`, `cache_write`,
   `cache_read` and `cost_usd`. Add the model, `attempts` and `tests_pass`.

   `COLUMNS=200` stops the table from wrapping the id across lines, which
   would defeat the `grep`.

6. **Repeat for T2 in a new session.** Look at the starting line first,
   `make task T=t2`, then a new id and `claude --session-id "$id"` again,
   same rules. The task:
   add a `--format json` flag to the `report` command in `src/orderly/cli.py`,
   keeping text as the default. The summary dictionary is already built by
   `build_summary`. Verify with `make task T=t2` and `make test`, exit, and
   run the same two commands to read the row into `T2,feature,baseline`.

7. **Post your combined total for T1 plus T2 in chat**: input tokens and
   cost.

## Do not optimize anything yet

This is the single most important instruction in the exercise. The temptation
to tidy your context before you measure is strong, and a flattering baseline
makes everything you do afterwards look worse than it is.

## Done when

- Two complete worksheet rows, including attempts and pass/fail
- A combined total posted in chat

Tests passing is not required. A failed baseline is still a baseline, and an
expensive one is the most useful kind.

## If you get stuck

- **`ccusage` shows no sessions, or not yours.** It reads
  `~/.claude/projects/`, so you must be on the machine and user account the
  session ran under. The first run downloads the package and is slow.
- **`make` or `uv` is not found.** `uv` installs in one command, see
  [INSTALL.md](../../INSTALL.md#prerequisites). On Windows there is no
  `make`; run the underlying commands, `uv run pytest` and
  `uv run pytest tests/tasks/test_t1_*.py -v`.
- **You reused a session by mistake.** That line now covers more than one
  task. Redo that task in a fresh session. It costs a few minutes, and a mixed
  line is worth nothing.
- **You are out of time.** A partial row is a usable baseline. Record what you
  have and move on.

The reference answers are in [solution/solution.md](solution/solution.md).
Read them after you have your own number, not before.

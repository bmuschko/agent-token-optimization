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

You will measure two tasks and note these figures for each. A scratch file
or a few lines in your notes is enough; Exercises 2 and 3 compare against
them:

| Figure | What it is |
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

**`tokscale`, for every agent.** Each coding agent writes the usage figures
its API returns into a local session log: Claude Code under
`~/.claude/projects/`, Codex CLI under `~/.codex/sessions/`, Copilot CLI under
`~/.copilot/`, Gemini CLI under `~/.gemini/tmp/`, and so on for some sixty
others. Those are the numbers the provider bills on.
[tokscale](https://github.com/junhoyeo/tokscale) reads all of those logs,
prices every one of them from the same public price table, and prints one row
per session. Nothing to install, nothing to route, nothing to reset:

```bash
COLUMNS=200 npx tokscale@latest --light --no-spinner --today --group-by client,session,model
```

`COLUMNS=200` matters. In a terminal narrower than about 100 columns tokscale
silently drops the Input and Output columns and prints only a combined
total. On Windows, maximize the terminal window instead.

One instrument for every agent is the reason for the choice. The rows you
record today are comparable with rows from any other agent tokscale reads, so
if you later wonder whether Codex, Copilot or Gemini would do the same task
for less, you run it there and read the answer off the same table. Nothing
about the method changes.

Because it reports per session, you run **one fresh session per task**. One
row is then one task.

Why not the alternatives, one line each. `/context` shows what is in the
window right now, not what a task cost in total. `/cost` only reports on
API-key billing, not on subscription plans. `ccusage` gives the same session
view, but only for Claude Code. The Headroom proxy counts tokens on the wire
for any agent, but it reports savings rather than spend, never sees output
tokens, and keeps one cumulative ledger. It earns its setup in Exercise 5,
where you need per-request detail. Not here.

**Where your agent sits.** How you find your session's row depends on
whether you can name the session before it starts:

- **Claude Code** lets you choose the session id on the command line, so you
  can pull your row by id no matter what else is in the log.
- **Codex CLI, Copilot CLI, Gemini CLI** assign their own id. You list the
  sessions before the task and again after; the row that appeared is yours.
- **Cursor** writes no local session log. tokscale pulls Cursor's usage from
  Cursor's own API, with no session boundaries, so you read today's total
  before and after the task and subtract.
- **Copilot in VS Code** is not something tokscale can read. Use the per
  request figures in the VS Code Chat Debug View and add them up by hand.

The steps below spell out each path.

A note on the dollar figure. tokscale prices tokens at API list rates, taken
from the LiteLLM price table. On a subscription plan you did not pay that
amount, but it is the right unit for comparison, and it is the same unit on
every later row.

## Steps

Run every command from the repository root. The tests need the Makefile
there, the agent needs `src/` inside its working directory, and the helper in
step 5 runs through `uv`.

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

2. **Start a fresh session for T1.** Fresh means a new session: not a resume,
   and not a clear inside an old one. It must start empty so that its totals
   are T1 and nothing else.

   **Claude Code.** In your terminal, at the repository root, pick the id
   yourself and start the agent with it:

   ```bash
   id=$(uuidgen | tr 'A-Z' 'a-z')
   claude --session-id "$id"
   ```

   tokscale identifies sessions by id and nothing else, so picking the id
   yourself is what lets step 5 find this session's row no matter what other
   sessions are open. Keep using this terminal; `$id` has to still be there
   after you exit. PowerShell: `$id = [guid]::NewGuid().ToString()`.

   **Codex CLI, Copilot CLI, Gemini CLI.** Take a snapshot of the sessions
   tokscale already knows about, so the new one stands out afterwards:

   ```bash
   COLUMNS=200 npx tokscale@latest --light --no-spinner --today --group-by client,session,model
   ```

   Then start the agent as you normally do, `codex`, `copilot` or `gemini`,
   at the repository root.

   **Cursor.** Connect tokscale to your Cursor account once. It picks up the
   login from the Cursor desktop app, or asks for a browser session token:

   ```bash
   npx tokscale@latest cursor login
   npx tokscale@latest cursor status
   ```

   Then take the before snapshot. The sync pulls your latest usage from
   Cursor's API; the report prints today's total:

   ```bash
   npx tokscale@latest cursor sync
   COLUMNS=200 npx tokscale@latest --light --no-spinner --today --client cursor
   ```

   Note the Input, Output, Cache Write, Cache Read and Cost on the Total
   line, then open a new chat in Cursor.

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

5. **End the session and read the row.** Exit the agent: `/exit` in Claude
   Code, Codex CLI and Copilot CLI, `/quit` in Gemini CLI. Then, back in the
   same terminal, pull the row.

   **Claude Code.** `$id` is the session you just left. Ask tokscale for
   today's sessions as JSON and let the helper pick yours out:

   ```bash
   npx tokscale@latest --json --no-spinner --today --group-by client,session,model \
     | uv run python scripts/session_row.py "$id"
   ```

   The helper exists because the per-session table tokscale prints only has
   a combined token total; the cache split listed above is in its JSON. This
   one is a real T1 run on a frontier model, five requests end to end; your
   numbers will differ, the shape is what to recognize:

   ```
   session=f5ba87fa-2c1e-4f0b-9a7d-3e8c5b6d1a20 client=claude model=claude-fable-5-1
   input_tokens=66 output_tokens=643 cache_read=87543 cache_write=20760 cost_usd=0.47
   ```

   Write the five numbers down as your T1 baseline, with the model,
   `attempts` and `tests_pass` next to them.

   **Codex CLI, Copilot CLI, Gemini CLI.** List the sessions again and
   compare with the snapshot from step 2:

   ```bash
   COLUMNS=200 npx tokscale@latest --light --no-spinner --today --group-by client,session,model
   ```

   The row that was not there before is your session.

   **Cursor.** Sync again, print today's total again, and subtract the
   before snapshot column by column:

   ```bash
   npx tokscale@latest cursor sync
   COLUMNS=200 npx tokscale@latest --light --no-spinner --today --client cursor
   ```

   Cursor's API can lag by a few minutes. If the total has not moved, wait
   and sync once more before you conclude the task was free.

6. **Repeat for T2 in a new session.** Look at the starting line first,
   `make task T=t2`, expect 2 failed, 1 passed, then start a new session
   exactly as in step 2: a new id and `claude --session-id "$id"` for Claude
   Code, a fresh snapshot for the other CLIs, a fresh sync and total for
   Cursor. The task: add a `--format json` flag to the `report` command in
   `src/orderly/cli.py`, keeping text as the default. The summary dictionary
   is already built by `build_summary`.

   As with T1, phrase it your own way. If you want a starting point, this is
   enough for the agent to add the feature:

   > Add a `--format json` option to the `report` command in
   > `src/orderly/cli.py`. Text output stays the default. With `--format json`
   > the command should print the summary that `build_summary` already
   > returns as JSON, and the existing `--status` and `--region` filters
   > should keep working.

   Verify with `make task T=t2` and `make test`, exit, and read the row the
   same way as your T1 baseline.

7. **Post your combined total for T1 plus T2 in chat**: input tokens, cost,
   and which agent you ran.

## Do not optimize anything yet

This is the single most important instruction in the exercise. The temptation
to tidy your context before you measure is strong, and a flattering baseline
makes everything you do afterwards look worse than it is.

## Done when

- T1 and T2 each noted with the five figures, attempts and pass/fail
- A combined total posted in chat

Tests passing is not required. A failed baseline is still a baseline, and an
expensive one is the most useful kind.

## If you get stuck

- **tokscale shows no sessions, or not yours.** It reads the agent's log
  directory on this machine and user account, so you must run it where the
  session ran. See which directories it scanned and whether they exist:

  ```bash
  npx tokscale@latest clients
  ```

  The first run downloads the package and the price table and is slow.
- **The helper says there is no such session.** Your session may have
  started before midnight local time. Drop `--today` from the tokscale
  command, or replace it with `--since 2026-10-20` using the date you
  started.
- **tokscale warns that some usage is unpriced.** The cost column may then
  be incomplete, usually because a model is too new for the price table.
  Record the token columns, which are exact, and see which model is affected:

  ```bash
  npx tokscale@latest pricing explain --no-spinner
  ```
- **`make` or `uv` is not found.** `uv` installs in one command, see
  [INSTALL.md](../../INSTALL.md#prerequisites). On Windows there is no
  `make`; run the underlying commands, `uv run pytest` and
  `uv run pytest tests/tasks/test_t1_*.py -v`. The helper runs the same way,
  `uv run python scripts\session_row.py $id`.
- **You reused a session by mistake.** That row now covers more than one
  task. Redo that task in a fresh session. It costs a few minutes, and a mixed
  row is worth nothing.
- **You are out of time.** A partial row is a usable baseline. Record what you
  have and move on.

The reference answers are in [solution/solution.md](solution/solution.md).
Read them after you have your own number, not before.

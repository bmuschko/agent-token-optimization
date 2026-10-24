# Exercise 1: Measure Your Baseline

**Section 1 · 6 minutes · work alone**

## What a baseline is

Every later exercise changes one thing about how your agent works and asks whether the bill went down. This exercise records the "down from what".

The baseline is what your agent spends to take one task from red tests to green with your habits as they are today, nothing optimized. It is the sum of every request the agent makes, and each request resends the whole context: the system prompt, the tool definitions, the rules file, every file read so far, the conversation so far. A task therefore costs roughly

```
requests × context size per request
```

Later exercises shrink one factor or the other. You will measure two tasks and note these figures for each; a scratch file is enough, Exercises 2 and 3 compare against them.

| Figure | What it is |
|---|---|
| Input | everything the agent sent, summed over all requests |
| Output | everything the model wrote back |
| Cache read | the part of the input served from the prompt cache, at a tenth of the price or less, depending on the model |
| Cache write | the part written into the cache, at 1.25 times the price |
| Cost | the four above, priced, in US dollars |
| Requests | how many times the agent called the model; each call resends the whole window |
| Attempts | how many times you sent the agent back after a red test, counted by hand |
| Tests pass | whether both test commands ended green, noted by hand |

Cost covers every attempt, the failed ones included. Input will dwarf output by an order of magnitude. That is normal, and input is the lever the rest of the course pulls.

## The tool

Each agent writes the usage its API returns into a local session log: Claude Code under `~/.claude/projects/`, Codex CLI under `~/.codex/sessions/`, Copilot CLI under `~/.copilot/`, Gemini CLI under `~/.gemini/tmp/`, and some sixty others. [tokscale](https://github.com/junhoyeo/tokscale) reads those logs, prices them from one public price table, and prints one row per session. Nothing to install, route or reset:

```bash
COLUMNS=200 npx tokscale@latest --light --no-spinner --today --group-by client,session,model
```

`COLUMNS=200` keeps the Input and Output columns in a terminal narrower than about 100 columns. On Windows, maximize the window instead.

One instrument for every agent is the point: your rows are comparable with rows from any other agent, so if you later wonder whether Codex, Copilot or Gemini would do the task for less, you run it there and read the same table. Because tokscale reports per session, you run **one fresh session per task**, so one row is one task.

The alternatives fall short. `/context` shows the window right now, not what a task cost. `/cost` only reports API-key billing. `ccusage` is Claude Code only. The Headroom proxy reports savings rather than spend, never sees output tokens, and earns its setup in Exercise 5.

How you find your row depends on whether you can name the session before it starts:

- **Claude Code** lets you choose the session id, so you pull the row by id.
- **Codex CLI, Copilot CLI, Gemini CLI** assign their own id. List the sessions before and after the task; the row that appeared is yours.
- **Cursor** writes no local log. tokscale pulls today's total from Cursor's API, so you read it before and after and subtract.
- **Copilot in VS Code** writes its chat sessions under VS Code's workspace storage, which tokscale reads and lists under the Copilot client. Those rows carry input and output only, no cache split, so the cost column prices every input token at full rate. Find your row as the CLIs do: list before and after.

tokscale prices tokens at API list rates from the LiteLLM table. On a subscription you did not pay that amount, but it is the same unit on every row, which is what comparison needs.

## Steps

Run every command from the repository root: the tests need the Makefile there, the agent needs `src/` in its working directory, and the helper in step 5 runs through `uv`.

1. **Look at the starting line, in a second terminal.** `make task T=t1` fails 3 of 4 tests, at exactly the $100.00, $500.00 and $5,000.00 boundaries the task describes. This run is not an attempt and costs no tokens. Whether you paste its output into your prompt is part of your habits.

2. **Start a fresh session for T1.** Not a resume and not a clear inside an old one: it must start empty so its totals are T1 and nothing else.

   **Claude Code.** Pick the id yourself and keep using this terminal; `$id` has to still be there after you exit. PowerShell: `$id = [guid]::NewGuid().ToString()`.

   ```bash
   id=$(uuidgen | tr 'A-Z' 'a-z')
   claude --session-id "$id"
   ```

   **Codex CLI, Copilot CLI, Gemini CLI, Copilot in VS Code.** Snapshot the sessions tokscale already knows, then start `codex`, `copilot` or `gemini` as you normally do, or open a new chat in VS Code.

   ```bash
   COLUMNS=200 npx tokscale@latest --light --no-spinner --today --group-by client,session,model
   ```

   **Cursor.** Connect tokscale to your account once with `npx tokscale@latest cursor login`. Then take the before snapshot, note the Total line, and open a new chat in Cursor.

   ```bash
   npx tokscale@latest cursor sync
   COLUMNS=200 npx tokscale@latest --light --no-spinner --today --client cursor
   ```

3. **Work T1 the way you normally would.** The task, from [TASKS.md](../../TASKS.md): the volume discount tiers in `src/orderly/pricing/discount.py` are documented as inclusive of their thresholds, but an order of exactly $100.00 does not get the 5% rate. Phrase it your own way; this is enough for the agent to find and fix the bug:

   > The volume discount tiers in `src/orderly/pricing/discount.py` are supposed to be inclusive of their thresholds, but an order of exactly $100.00 doesn't get the 5% rate. Fix the off-by-one bug.

   Use your usual model, let the agent open whatever it normally opens, and do not read the solution first. Knowing the fix changes how you prompt, which is the one thing this exercise cannot recover from.

4. **Verify, in a second terminal.** Run these yourself; the agent running them puts the output into the context you are measuring.

   ```bash
   make task T=t1        # acceptance tests for T1
   make test             # regression suite, must stay green
   ```

   Both green: T1 is done. Either red: tell the agent what failed and add one to your attempts.

5. **End the session and read the row.** `/exit` in Claude Code, Codex CLI and Copilot CLI, `/quit` in Gemini CLI. Then, in the same terminal, pull the row.

   **Claude Code.** The helper picks your session out of tokscale's JSON, which has the cache split the table lacks:

   ```bash
   npx tokscale@latest --json --no-spinner --today --group-by client,session,model \
     | uv run python scripts/session_row.py "$id"
   ```

   A real T1 run on a frontier model, five requests end to end. Your numbers will differ; the shape is what to recognize:

   ```
   session=f5ba87fa-2c1e-4f0b-9a7d-3e8c5b6d1a20 client=claude model=claude-fable-5-1
   Input 66 · Output 643 · Cache read 87,543 · Cache write 20,760 · Cost $0.47 · Requests 5
   ```

   Note the five numbers as your T1 baseline, with the model, your attempts and whether the tests passed.

   **Codex CLI, Copilot CLI, Gemini CLI, Copilot in VS Code.** Run the snapshot command from step 2 again. The row that was not there before is your session. A VS Code row shows zero in both cache columns; that is the log, not your usage.

   **Cursor.** Sync and print today's total again, and subtract the before snapshot column by column. Cursor's API can lag by a few minutes; if the total has not moved, sync once more before you conclude the task was free.

6. **Repeat for T2 in a new session.** `make task T=t2` fails 2 of 3. Start a new session exactly as in step 2. The task: add a `--format json` flag to the `report` command in `src/orderly/cli.py`, keeping text as the default; `build_summary` already builds the summary dictionary. Phrase it your own way; this is enough for the agent to add the feature:

   > Add a `--format json` option to the `report` command in `src/orderly/cli.py`. Text output stays the default. With `--format json` the command should print the summary that `build_summary` already returns as JSON, and the existing `--status` and `--region` filters should keep working.

   Verify with `make task T=t2` and `make test`, exit, and read the row as you did for T1.

7. **Post your combined total for T1 plus T2 in chat**: input tokens, cost, and which agent you ran.

## Do not optimize anything yet

This is the most important instruction in the exercise. The temptation to tidy your context before you measure is strong, and a flattering baseline makes everything you do afterwards look worse than it is.

## Done when

- T1 and T2 each noted with the five figures, attempts and pass/fail
- A combined total posted in chat

Tests passing is not required. A failed baseline is still a baseline, and an expensive one is the most useful kind.

## If you get stuck

- **tokscale shows no sessions, or not yours.** It reads the agent's log directory on this machine and user account, so run it where the session ran. `npx tokscale@latest clients` lists the directories it scanned. The first run downloads the package and the price table and is slow.
- **The helper says there is no such session.** It may have started before midnight local time. Drop `--today`, or replace it with `--since` and the date you started.
- **tokscale warns that some usage is unpriced.** A model is too new for the price table. Record the token columns, which are exact; `npx tokscale@latest pricing explain --no-spinner` names the model.
- **`make` or `uv` is not found.** `uv` installs in one command, see [INSTALL.md](../../INSTALL.md#prerequisites). On Windows there is no `make`; run `uv run pytest` and `uv run pytest tests/tasks/test_t1_*.py -v` directly, and the helper as `uv run python scripts\session_row.py $id`.
- **You reused a session by mistake.** That row covers more than one task. Redo the task in a fresh session; a mixed row is worth nothing.
- **You are out of time.** A partial row is a usable baseline. Record what you have and move on.

The reference answers are in [solution/solution.md](solution/solution.md). Read them after you have your own number, not before.

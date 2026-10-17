# Troubleshooting

Ordered by how often each one actually happens.

## The token counter reads zero

The proxy is running but your agent is not routed through it.

```bash
headroom doctor
```

If `doctor` is green and the counter is still zero, you probably started the
agent in a different shell from the one that exported `ANTHROPIC_BASE_URL`. Use
`headroom wrap <agent>` instead, which handles the environment for you.

## `doctor` says `claude: not routed` while the session clearly works

You ran `doctor` from a different directory than `headroom wrap`. Both read
`.claude/settings.local.json` relative to their own working directory, so a
wrap launched inside an exercise folder is invisible to a
`doctor` run at the repository root, and the other way round. Run everything
from the repository root. The `savings` row is right from any directory,
because it comes from the proxy's own counters.

## `headroom wrap claude` starts an older Claude Code

Any of these when you first launch through `headroom wrap`, in Exercise 3:

- A **Settings Error** dialog at launch naming a hook event such as
  `StopFailure` as an invalid key
- `/model` lists Opus 4.6, Sonnet 4.6 and Haiku 4.5 only, with your usual
  model shown as "Custom model"
- "There's an issue with the selected model", and the proxy log in
  `~/.headroom/logs/proxy-8787.log` shows `status=404 ... model: fable`

`headroom wrap` launches whichever `claude` is first on PATH **in the terminal
you run it from**, which is often not the one your other terminals use. A tab
opened before you installed or upgraded Claude Code still has the old PATH, so
try a fresh shell first. Then check in that same terminal:

```bash
which claude && claude --version
```

If the version is behind the one that works elsewhere, upgrade or remove the
stale install. For an npm copy that is `npm install -g
@anthropic-ai/claude-code@latest`, or `npm uninstall -g
@anthropic-ai/claude-code` so PATH falls through to the native one. Claude
Code's auto-updater may already have replaced the files while the old process
kept running, in which case quitting and relaunching is the whole fix. Either
way, run `headroom savings --reset` again before you measure.

## A download is blocked, or SSL verification fails

Almost always an SSL-inspecting corporate proxy. This is the single most common
setup problem and the reason this repo asks you to install a day ahead.

- Try from a personal network to confirm that is the cause.
- Ask IT for the corporate CA bundle and point `pip` and `npm` at it.

## `make test` fails on a fresh clone

It should not. Check in this order:

1. Is `uv` on your PATH? `uv --version`. If not, see
   [INSTALL.md](INSTALL.md#prerequisites).
2. Did `uv sync` finish without errors? Run it again; it is idempotent.
3. On Windows, `make` does not exist. Run `uv run pytest` directly.

There is no virtual environment to activate. `make test` runs `uv run pytest`,
which uses the project environment whether or not your shell knows about it.
If all three are fine and the suite still fails, open an issue with the output
of `make verify`.

## `make task T=t1` fails and I have not started yet

That is correct and expected. The acceptance tests are red on a fresh clone;
making them green is the task. See [TASKS.md](TASKS.md).

## `claude-usage-analyzer` reports nothing

It reads `~/.claude/projects/`, so it only sees Claude Code sessions. Cursor and
Copilot users should use their own dashboards. The exercises say where.

## `npx ccusage` is slow the first time

It downloads the package before running. Run it once before the session so the
cache is warm.

## My costs went *up* after I optimized

Two usual causes, both covered in Section 3:

- **You edited the rules file mid-session.** It sits near the top of the
  prefix, so changing it invalidates the cache below it and you pay the 1.25x
  write rate on everything.
- **You switched models mid-task.** Same mechanism. Switch at task boundaries.

## The T8 test passes sometimes

It should fail consistently. If it passes, your machine may be running the
thread pool with fewer workers than requested. Try:

```bash
make task T=t8
```

a few times. If it passes every time, note it and move on; the fix is still the
fix, and the solution explains why.

## Tests pass but my agent clearly broke something

Good. That is the lesson, and it is worth saying out loud: the suite is a
floor, not a proof. Read the diff.

## Something else

Open an issue at
[github.com/bmuschko/agent-token-optimization/issues](https://github.com/bmuschko/agent-token-optimization/issues)
with the output of `make verify`.

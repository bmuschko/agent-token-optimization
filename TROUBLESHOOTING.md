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

## A download is blocked, or SSL verification fails

Almost always an SSL-inspecting corporate proxy. This is the single most common
setup problem and the reason this repo asks you to install a day ahead.

- Try from a personal network to confirm that is the cause.
- Ask IT for the corporate CA bundle and point `pip` and `npm` at it.
- If neither is possible, use `REPLAY_MODE=true` and work from
  [replays/](replays/). You will still be able to do every exercise.

## `make test` fails on a fresh clone

It should not. Check in this order:

1. Are you in the virtual environment? `which python3`
2. Did `pip install -r requirements.txt` finish without errors?
3. Is your Python 3.10 or later? `python3 --version`

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

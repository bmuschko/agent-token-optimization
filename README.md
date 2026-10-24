# agent-token-optimization

Course repository for **Cutting Token Costs with AI Coding Agents**, an O'Reilly live training by [Benjamin Muschko](https://www.oreilly.com/pub/au/7768).

You will drive your own coding agent against this repository for two hours, routed through a local proxy so you can see every token, and measure what your habits actually cost.

## Start here

1. **[INSTALL.md](INSTALL.md)** - install everything, a day before the session
2. Run `make verify` - it should print a green check
3. **[exercises/](exercises/)** - the six hands-on exercises, in order

Please do step 1 at least a day ahead, especially on a corporate network. The first ten minutes of a live session is the worst possible time to discover that an SSL-inspecting proxy is blocking a download.

## What is in here

| Path | What it is |
|---|---|
| [`src/orderly/`](src/orderly) | A small order service. 60-plus modules, so loading all of it is expensive. |
| [`tests/`](tests) | The regression suite. Green on a fresh clone and it must stay that way. |
| [`tests/tasks/`](tests/tasks) | Acceptance tests for the seeded tasks. Red until you do the work. |
| [`exercises/`](exercises) | Six exercises, each with `instructions.md` and a `solution/`. |
| [`TASKS.md`](TASKS.md) | The eight tasks T1 to T8 you work with your agent. |

## The two commands

```bash
make test             # regression suite, must stay green
make task T=t1        # acceptance tests for one task
```

A task is done when its acceptance tests pass **and** the regression suite is still green. Never one without the other. That rule is the spine of the whole course: a token saving that breaks your tests is not a saving.

## About `CLAUDE.md`

The rules file in this repository is deliberately overgrown. It is roughly ninety lines, most of which earn nothing, and it is the raw material for Exercise 3. Do not take it as a model to copy. The lean version that survives the exercise is in [`exercises/03-context-discipline/solution/CLAUDE.lean.md`](exercises/03-context-discipline/solution/CLAUDE.lean.md).

## Cost

Budget roughly **$3** of your own token usage for the full session.

## Which agent

Claude Code, Cursor, or GitHub Copilot. Any one is fine. Every exercise reads its numbers from the same tool, tokscale, and reads the window from the agent's own view. Two limits to know before you choose: Copilot in VS Code logs input and output tokens only, with no cache split, so its rows price every input token at full rate; and the Headroom proxy in Exercises 5 and 6 cannot see Cursor's traffic, which goes through Cursor's own servers, so Cursor users read those two exercises from the context indicator and the usage dashboard instead.

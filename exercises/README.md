# Exercises

Six hands-on exercises, in the order they run during the course. Each folder has `instructions.md` and a `solution/` with `solution.md` and any reference files.

| # | Exercise | Section | Time |
|---|---|---|---|
| 1 | [Establish your baseline](01-baseline-measurement/instructions.md) | 1 | 6 min |
| 2 | [Break down your burn](02-attribute-the-burn/instructions.md) | 2 | 10 min |
| 3 | [Scope it down and measure](03-context-discipline/instructions.md) | 3 | 14 min |
| 4 | [Escalate and compare](04-escalate-and-compare/instructions.md) | 4 | 14 min |
| 5 | [Measure the tool tax](05-tool-definition-tax/instructions.md) | 5 | 10 min |
| 6 | [Compaction, memory and your plan](06-compaction-and-memory/instructions.md) | 5 | 6 min |

## Read the solutions after you have your own number

Every solution opens with what the numbers usually look like. Reading that first anchors you to someone else's result and costs you the exercise.

## The two commands every exercise uses

```bash
make test             # regression suite, must stay green
make task T=t1        # acceptance tests for one task
```

Both are thin wrappers over `uv run pytest`. On Windows, where `make` is absent, run `uv run pytest` and `uv run pytest tests/tasks/test_t1_*.py -v` directly.

A task is done when its acceptance tests pass **and** the regression suite is still green. Never one without the other.

## Which tool measures what, and why

Every exercise measures a delta, and a delta only means something if both sides come from the same instrument. The course uses four tools, one per question. Each exercise says which one it uses and why, at the point where you read the number.

| Question | Tool | Exercises |
|---|---|---|
| How many input tokens did the agent send? | `headroom savings` | 5, 6 |
| What did it cost, and how much was output? | `npx tokscale@latest` | 1, 2, 3, 4 |
| What made one session expensive? | `ccwhy` on Claude Code, the per-agent views in Exercise 2 | 2 |
| What is in the window right now? | `/context` | 2, 5 |

The rule underneath: **every number you record comes from `tokscale`; the proxy is for per-turn views.**

`headroom savings` counts every input token the proxy forwarded, per request, with the cached history that is resent every turn included, and it does so for any agent. That makes it the instrument for the per-turn question in Exercise 6 and in Exercise 5. It reports savings rather than spend: in passthrough mode the line reads `saved 0 / N tokens`, and `N` is your number. The ledger behind it is cumulative and global, so run `headroom savings --reset` before every measured run.

`tokscale` prices a whole session, output tokens and cache read and write included, none of which the proxy reports, and it does so for every agent. One session per run keeps it isolated.


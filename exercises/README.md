# Exercises

Six hands-on exercises, in the order they run during the course. Each folder
has `instructions.md` and a `solution/` with `solution.md` and any reference
files.

| # | Exercise | Section | Time |
|---|---|---|---|
| 1 | [Establish your baseline](01-baseline-measurement/instructions.md) | 1 | 6 min |
| 2 | [Break down your burn](02-attribute-the-burn/instructions.md) | 2 | 10 min |
| 3 | [Scope it down and measure](03-context-discipline/instructions.md) | 3 | 14 min |
| 4 | [Route and compare](04-model-routing/instructions.md) | 4 | 14 min |
| 5 | [Measure the tool tax](05-tool-definition-tax/instructions.md) | 5 | 10 min |
| 6 | [Compaction, memory and your plan](06-compaction-and-memory/instructions.md) | 5 | 6 min |

The instructor demo script is in [instructor-demo](../instructor-demo/).

## Read the solutions after you have your own number

Every solution opens with what the numbers usually look like. Reading that
first anchors you to someone else's result and costs you the exercise.

## The two commands every exercise uses

```bash
make test             # regression suite, must stay green
make task T=t1        # acceptance tests for one task
```

A task is done when its acceptance tests pass **and** the regression suite is
still green. Never one without the other.

## If you cannot run your agent live

```bash
export REPLAY_MODE=true
```

Every exercise then works against the recorded sessions in
[replays/](../replays/). Absolute numbers differ from a live run. The deltas,
which are what the exercises measure, hold.

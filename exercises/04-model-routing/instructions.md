# Exercise 4: Route and Compare

**Section 4 · 14 minutes · work alone**

## Objective

Measure escalate-on-failure against frontier-everything on your own task mix,
on both cost and pass rate. You are not being told which wins. You are
measuring which wins for you.

## Steps

### Run A, the control

Work **T1 through T6** entirely on your **frontier** model. Record total cost
and pass rate.

### Run B, the routed version

Reset the repo (`git checkout -- src tests` or `git stash`) and work the same
six tasks on the **cheapest capable** model, escalating a task to the frontier
model only after its acceptance tests fail **twice**.

### Compare

| | Run A | Run B |
|---|---|---|
| Total cost | | |
| Tasks passing | | |
| **Cost per completed task** | | |

Post your two cost-per-completed-task numbers in chat, **even if B lost**.

## The tasks

| Task | Kind | Verify |
|---|---|---|
| T1 | bug, one file | `make task T=t1` |
| T2 | feature, one file | `make task T=t2` |
| T3 | bug, two files | `make task T=t3` |
| T4 | refactor, three files | `make task T=t4` |
| T5 | feature, two files | `make task T=t5` |
| T6 | test coverage | `make coverage` |

T6 is done when `src/orderly/pricing/currency.py` reaches 95% line coverage. It
starts at 52%.

## What "cheapest capable" means

Not the cheapest model on the menu. The cheapest model that passes T1, T2 and
T6 on the first attempt. Find that model and pin it.

## Done when

Two complete runs and a defensible answer to: which route would you use on
Monday, and for which kinds of task?

## Expect

**Run B takes longer in wall-clock time even when it costs less.** That latency
is a real cost. Write it down next to the money.

If you are running short, cut the task list to T1, T2, T5 and T6. Never cut the
control run; without it you have nothing to compare against.

## If you get stuck

- **Escalating mid-task made things more expensive.** Switching models
  invalidates the prefix cache. Escalate at a task boundary, not in the middle
  of a turn.
- **Replay mode.** `replays/routing/` has both runs across all six tasks.

The reference answers are in [solution/solution.md](solution/solution.md).

# Exercise 4: Escalate and Compare

**Section 4 · 14 minutes · work alone**

## Objective

Section 4 said the model and the effort setting are the two biggest dials you control, and that the cheapest policy is to start low and spend more only on the tasks that fail. This exercise measures that policy against running everything on the frontier, on your own tasks, on both axes: cost per completed task and pass rate. You are not being told which wins. You are measuring which wins for you.

## Before you start

Nothing new to install. Reset the repository so both runs start from the same tree, and reset it again between the runs:

```bash
git checkout -- src tests
make test             # green
```

Pick the two settings for the runs before you start, so you are not choosing mid-task:

- **The frontier setting** for Run A: the strongest model your tool offers, at its default effort.
- **The cheap setting** for Run B: the cheapest capable model from the tier slide, Haiku 5.5, GPT-6 Luna or Composer 2.5, at its default effort. If your tool does not let you pick the model, use your usual model at **low effort** instead; the policy is the same on either dial, and Anthropic's published measurement is on the effort one.

Where to set them:

| Agent | Model | Effort |
|---|---|---|
| Claude Code | `/model`, or `claude --model <name>` when starting the session | `/effort low` or `/effort high`, at the start of the session |
| Copilot in VS Code | the model picker above the chat input, per request | not exposed on every model; use the model dial |
| Copilot CLI | `/model` | not exposed on every model; use the model dial |
| Cursor | the model picker; pick a model explicitly rather than Auto, so you know which one ran | not exposed; use the model dial |

"Cheapest capable" means the cheapest model that passes T1 on the first attempt. If your cheap setting fails T1, step up one tier and start Run B again from there; that tier is your floor, and it is worth noting.

## The measurement

Each attempt at a task is its own session, started, verified and read exactly as in Exercise 1, so each lands on its own tokscale row. Run A is one row per task. Run B is one row per task plus one row for every escalation, because an escalation is a **fresh session** on the stronger setting, not the same session with the model switched: switching mid-session rewrites the cache, and a fresh session builds a short one. A run's cost is the sum of its rows, failed attempts included.

A task **passes** when `make task` and `make test` are both green. Cost per completed task is the run's cost divided by the tasks that passed, as in Exercise 2.

Write down the wall-clock time of each run as well. Latency is the cost the money column does not show, and the cheap-first policy pays it on every failure.

After Run B, one more view: grouping tokscale by model instead of session splits the run's spend by model, which is how much of it the escalations ate.

```bash
COLUMNS=200 npx tokscale@latest --light --no-spinner --today --group-by client,model
```

## Steps

1. **Run A, frontier only.** The control, on the frontier setting. Work three tasks, one per cost situation from Section 2, each in a fresh session:

   | Task | Situation | Verify |
   |---|---|---|
   | T1 | a change in one known place | `make task T=t1` |
   | T4 | a change across two files | `make task T=t4` |
   | T3 | a change across three files, with a structural acceptance test | `make task T=t3` |

   Use the same prompt for a task in both runs, so the setting is the only difference. These are scoped the way Exercise 3 taught; phrase them your own way if you like, but keep the file names.

   > **T1** The volume discount tiers in `src/orderly/pricing/discount.py` are supposed to be inclusive of their thresholds, but an order of exactly $100.00 doesn't get the 5% rate. Fix the off-by-one bug. Verify with `make task T=t1` and `make test`.

   > **T4** `list_orders` in `src/orderly/api/orders.py` returns every order. Add `limit` and `offset` parameters, and include `total` and `has_more` in the response. `src/orderly/utils/pagination.py` already has the clamping and slicing helpers; use them. Verify with `make task T=t4` and `make test`.

   > **T3** The same retry loop with exponential backoff is copy-pasted into the methods of `src/orderly/integrations/payments.py`, `shipping.py` and `inventory.py`. `src/orderly/utils/retry.py` already has a `call_with_retry` helper that nothing uses. Replace every inline loop with it, without changing behaviour, and do not write a new helper. `tests/test_integrations.py` must stay green. Verify with `make task T=t3` and `make test`.

   T3's "do not write a new helper" is deliberate: cheap models often write a second helper, which the structural test cannot catch, and both runs should be held to the same bar.

   Read each session's row and note cost, attempts and pass or fail.

2. **Reset.** `git checkout -- src tests`, then `make test` to confirm green and `make task T=t1` to confirm red.

3. **Run B, escalate on failure.** Same tasks, same order, fresh session each, starting on the cheap setting. A task moves up a tier only when its tests say so. For every task:

   1. Attempt it on the cheap setting. Verify. If both commands are green, note the row and move on.
   2. If a test is red, attempt it once more on the **same** setting, in a new session, with the failing test output in the prompt. This second attempt is the course's addition; Anthropic's measured policy escalates on the first failure, and you can skip this step to match it.
   3. If it is still red, **escalate**: a fresh session on the next tier up, with the failing test output in the prompt. With only two tiers in play that is the frontier setting; note that it is a two-tier jump.

   For both the retry and the escalation, send the task's prompt again with one paragraph added at the end, and paste the test output verbatim rather than describing it:

   > The previous attempt left these tests failing:
   > ```
   > <paste the failing test output>
   > ```
   > Fix that without undoing what already passes.

   Every attempt is a row. Note all of them, including the ones that failed.

4. **Compare.**

   | | Run A, frontier only | Run B, escalate on failure |
   |---|---|---|
   | Total cost, all attempts | | |
   | Tasks passing, of 3 | | |
   | **Cost per completed task** | | |
   | Wall-clock time | | |
   | Tasks that escalated | | |

5. **Post in chat:** both cost-per-completed-task numbers, both pass counts, and which tasks escalated, **even if B lost**. Then answer for yourself: which setting would you use on Monday, and for which of the three situations?

## Done when

- Two complete runs over the same tasks, every attempt noted
- Cost per completed task and pass rate for each
- An answer to: which setting on Monday, and for what

## Expect

Run B usually wins on cost at the same pass rate, with the escalations clustered on T3. Anthropic's measurement of the same policy on the effort dial, Opus 5.5 on SWE-bench Pro, came out about 40% cheaper than everything at high, at a slightly better pass rate. Yours may not: the ranking flips by task mix, and a mostly-hard mix turns the cheap attempt into a tax on every task. A Run B that lost is a legitimate result and the most useful one in the room, provided you say what your mix looked like.

**Run B takes longer in wall-clock time even when it costs less.** Every failure costs two runs of time. Write it down next to the money.

## If you get stuck

- **Three tasks per run is still too many.** Drop T3 from both runs. T1 and T4 give you the cheap and the mid situation; you lose the task most likely to escalate, so say so when you post.
- **Escalating mid-session made things more expensive.** Switching models or, on most models, effort invalidates the prefix cache. Escalate as a fresh session; it is its own row and its own cache.
- **Your tool exposes neither model nor effort.** You cannot run this exercise's comparison. Run the three tasks once, note the rows, and compare cost per completed task against your neighbour's two runs in chat.
- **The cheap setting passed everything.** That is a result: your floor is lower than you thought. Post it.

The reference answers are in [solution/solution.md](solution/solution.md).

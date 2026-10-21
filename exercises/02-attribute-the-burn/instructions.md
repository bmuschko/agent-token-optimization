# Exercise 2: Break Down Your Burn

**Section 2 · 10 minutes · work alone**

## Objective

Exercise 1 gave you a total. This exercise turns it into an attribution: which *kind* of work costs you the most per completed task, and which single controllable thing is your biggest sink.

## Before you start

Nothing to install or reset. The T1 and T2 fixes can stay in the working tree; the tasks below touch other files, and their numbers count here.

From now on, check `git status` after every run before noting the numbers. Whatever the agent touched is part of what the run cost.

The two questions need different evidence. Cost per kind is one number per session, and tokscale gives it for every agent as in Exercise 1. The sink needs two views tokscale does not have, what the window was made of and which tool calls filled it, and both live in the agent's own session log.

## Steps

1. **Run three more tasks, one of each remaining kind**, in any order:

   | Task | Kind | What it is | Done when |
   |---|---|---|---|
   | T3 | refactor | extract the duplicated retry logic into the existing helper | `make task T=t3` and `make test` green |
   | T4 | feature | `limit` and `offset` pagination on `list_orders` | `make task T=t4` and `make test` green |
   | T5 | exploration | where is rate limiting, and how do I change the limit | an answer naming the file, the constant, and the second way to change it |

   Full descriptions are in [TASKS.md](../../TASKS.md). Starting prompts, in case you want them:

   > **T3** The same retry loop with exponential backoff is copy-pasted into the methods of `src/orderly/integrations/payments.py`, `shipping.py` and `inventory.py`. `src/orderly/utils/retry.py` already has a `call_with_retry` helper that nothing uses. Replace the inline loops with it, without changing behaviour.

   > **T4** `list_orders` in `src/orderly/api/orders.py` returns every order. Add `limit` and `offset` parameters, and include `total` and `has_more` in the response. `src/orderly/utils/pagination.py` already has the clamping and slicing helpers.

   > **T5** Where is rate limiting implemented in this codebase, and how do I change the limit? In how many ways can it be changed?

   T5 is read-only and its prompt is unscoped on purpose: what an unconstrained search costs is the finding. Each task is a fresh session, started, verified and read exactly as in Exercise 1, with the same habits. This still measures how you work today.

2. **Note the cost, your attempts and whether the tests passed** for each. For T5, passing means the answer was complete.

   Then compute cost per completed task for all four kinds, T1 and T2 included. A kind's figure is the combined cost of its tasks, failed attempts included, over the number that passed, so the feature kind covers T2 and T4. A kind with no completion is the most expensive by definition.

3. **Find the controllable sink.** Two views, one question each.

   **What every request is made of**, inside a session of your agent:

   | Agent | Where |
   |---|---|
   | Claude Code | `/context` |
   | Copilot CLI | `/context`, and `/usage` for the session's totals |
   | Copilot in VS Code | hover the context window control in the chat input; the Agent Debug Logs add tool calls and the cache hit rate |
   | Cursor | the context indicator in the chat input |

   The rules file, your tool definitions, file context and history are yours; the system prompt and built-in tools are the vendor's. The largest of *your* categories is your sink.

   **What filled it**, from the session log:

   - **Claude Code.** `ccwhy session "$id"` prints a per-turn table of what each request resent and the tools it ran. Count the files read to answer T5. Install via [INSTALL.md](../../INSTALL.md#usage-analyzers).
   - **Copilot CLI.** The helper reads the log under `~/.copilot/session-state/` and prints requests, tokens and every file opened:

     ```bash
     uv run python scripts/copilot_session.py          # the newest session
     uv run python scripts/copilot_session.py 3ea9a2   # or by id prefix, from /session
     ```

   - **Copilot in VS Code.** [Agent Session Viewer](https://github.com/cuteribs/agent-session-viewer) turns the chat session files into a timeline with per-message tokens and tool calls: `npx @cuteribs/agent-session-viewer`.
   - **Cursor.** The transcript under `~/.cursor/projects/<project>/agent-transcripts/<id>/` lists every tool call but no tokens. The tokens are per request on the dashboard's usage page, which `tokscale cursor sync` also pulls. Join the two by time.

   > [!TIP]
   > **`ccwhy` runs 1.5 to 2.5 times above tokscale**, because Claude Code logs one entry per content block and `ccwhy` sums them all. Use it for the shape, which turns resent the most and which files were read. Every number you record comes from tokscale.

   The proxy is no help here: it counts tokens on the wire without knowing which session sent them or what the window held, and it cannot see Copilot or Cursor at all.

4. **Answer two questions in chat:**
   - Which **kind** of task cost you the most per completed task?
   - What is your single biggest **controllable** token sink?

## What "controllable" means

You cannot shrink your vendor's system prompt. You can shrink your rules file, your tool definitions, your file context and your session history. Only the second group counts.

## Done when

- Four kinds with a cost per completed task, from three new sessions plus T1 and T2
- A named most-expensive kind of task
- A named controllable sink

## If you get stuck

- **Three tasks in ten minutes is tight.** Drop T3 first; it is the slowest, and T1, T4 and T5 still give you three kinds.
- **`ccwhy` reports nothing.** It only reads `~/.claude/projects/`. Every other agent has its own path in step 3.
- **`/context` shows MCP tools at 0 tokens.** Your tools load on demand and the deferred figure is listed separately. Section 5 is about exactly that.

The reference answers are in [solution/solution.md](solution/solution.md).

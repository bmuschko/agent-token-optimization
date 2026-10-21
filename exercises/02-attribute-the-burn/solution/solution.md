# Solution: Break Down Your Burn

## The answer depends on one thing: did the agent read, or search?

There are two rankings, and the tool calls of your T5 session tell you which one you got: the Tools Used line of `ccwhy session` on Claude Code, the tools line of `scripts/copilot_session.py` on Copilot CLI, the transcript on Cursor.

**If the agent read its way there, exploration wins**, usually by a wide margin, although T5 produces no code at all. An agent that browses opens file after file until it finds rate limiting, a path through 60-plus source files, each one resent on every request that follows. The tool calls show a long list of file reads.

**If the agent searched first, the refactor wins.** One `grep` for `rate.?limit` returns the file, one read answers the question, and T5 lands near the bug fix. The tool calls show a few shell calls and a single read. T3 then takes the top spot because it has to see three files to change three files. Claude Code searches first by default, so in a Claude Code room this is the common outcome.

The two rankings, in cost per completed task:

| Kind | Agent read | Agent searched | Why |
|---|---|---|---|
| Bug fix (T1) | middling | lowest | cheap once located, expensive while searching |
| Refactor (T3) | high | highest | touches three files, needs to see all of them |
| Feature (T2, T4) | middling | middling | bounded, one or two files plus a test; if T2 cost far more, its agent fell for the exporters trap from Exercise 1 |
| Exploration (T5) | highest | middling | all retrieval, so its cost is set by how it retrieves |

Either way, exploration spends more tokens than a one-line fix for zero lines of code, and the only variable is retrieval strategy. That is the lever Section 3 pulls. If your agent searched first, the finding is that the habit is cheap because the tool already has it. If it browsed, the finding is the size of the tax.

## T5 reference answer

Rate limiting lives in `src/orderly/api/middleware/rate_limit.py`. The limit is a module-level constant:

```python
WINDOW_REQUEST_LIMIT = 120
WINDOW_SECONDS = 60
```

`RateLimiter` takes both as constructor arguments defaulting to those constants, so there are two ways to change it: edit the constant for everywhere, or pass `limit=` for one caller. A complete answer names the file, the constant and the constructor argument.

**The cheap way to find it.** One search, then one read:

```bash
grep -rln "rate" src/orderly --include='*.py'
```

An agent that browses instead reads `config.py`, `errors.py`, the whole `api/` tree and several services before landing on the right file. An agent that searches first does exactly this, in one tool call, without being told.

## The controllable sink people name

In most cohorts the top answer is **MCP tool definitions**, then **the rules file**. Both are fixed overhead paid on every request whether or not they help the task. Tool definitions are Section 5, the rules file Section 3.

`ccwhy` lists them as one line, "Cache creation (CLAUDE.md, MCP, system prompt)", which names the fixed prefix as the sink without separating your rules file and tools from the vendor's prompt. `/context` makes that split, which is why the two views are run together: one says how much, the other says made of what.

## Common wrong turns

- **Ranking kinds by cost without looking at whether the tests passed.** A cheap run for a task that never passed is spend with nothing completed. It ranks first, not last.
- **Treating the vendor system prompt as a sink.** It is overhead, but not yours to cut.
- **Measuring T5 by output tokens.** Exploration produces almost no output. All of its cost is on the input side, which is why it is invisible to people who watch the wrong number.

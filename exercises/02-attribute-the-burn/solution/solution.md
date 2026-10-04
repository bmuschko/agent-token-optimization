# Solution: Break Down Your Burn

## The answer most people get

**Exploration wins**, usually by a wide margin, and it surprises people because
T7 produces no code at all.

The reason is retrieval, not reasoning. Asked where rate limiting lives, an
agent with no constraints reads its way across the repo until it finds
something. On this project that is 60-plus source files. The same question,
asked with a `Grep` first, costs a fraction of it.

A typical attribution, in cost per completed task:

| Kind | Relative cost | Why |
|---|---|---|
| Exploration (T7) | highest | reads widely to answer one question |
| Refactor (T4) | high | touches three files, needs to see all of them |
| Bug fix (T1) | middling | cheap once located, expensive while searching |
| Feature (T5) | middling | bounded, two files plus a test |

If your own ranking differs, that is a finding worth saying out loud. The most
common variation: people who already work in tightly scoped sessions see
exploration drop to the middle, because their habits are already doing the
work Section 3 is about to teach.

## T7 reference answer

Rate limiting lives in `src/orderly/api/middleware/rate_limit.py`. The limit is
the module-level constant:

```python
WINDOW_REQUEST_LIMIT = 120
WINDOW_SECONDS = 60
```

`RateLimiter` takes both as constructor arguments defaulting to those
constants, so there are two ways to change it: edit the constant to change it
everywhere, or pass `limit=` when constructing the limiter to change it for one
caller. A complete answer names the file, the constant, and the fact that the
constructor argument exists.

**The cheap way to find it.** One targeted search, then one file read:

```bash
grep -rn "rate" src/orderly --include=*.py -l
```

That returns a handful of paths. Reading one of them answers the question. An
agent told to "find where rate limiting is implemented" without that nudge will
often read `config.py`, `errors.py`, the whole `api/` tree and several services
before landing on the right file.

## The controllable sink people name

In most cohorts the top answer is **MCP tool definitions**, followed by **the
rules file**. Both are fixed overhead: you pay them on every request in the
session whether or not they contribute anything to the task at hand. Tool
definitions are Section 5. The rules file is Section 3.

`claude-usage-analyzer` names these directly in its "Controllable Token Sinks"
section, which is why it is worth running alongside `ccusage` rather than
instead of it. One answers how much, the other answers why.

## Common wrong turns

- **Comparing raw totals instead of cost per completed task.** A refactor that
  took one attempt can look worse than a bug fix that took three, until you
  divide by tasks completed.
- **Treating the vendor system prompt as a sink.** It is overhead, but it is
  not yours to cut. Ignore it.
- **Measuring T7 by output tokens.** Exploration produces almost no output. All
  of its cost is on the input side, which is exactly why it is invisible to
  people who watch the wrong number.

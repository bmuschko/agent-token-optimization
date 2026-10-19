# Solution: Break Down Your Burn

## The answer depends on one thing: did the agent read, or search?

There are two rankings, and the "Tools Used" line of `ccwhy session` tells
you which one you got.

**If the agent read its way there, exploration wins**, usually by a wide
margin, and it surprises people because T7 produces no code at all. Asked
where rate limiting lives, an agent that browses opens file after file until
it finds something. On this project that is a path through 60-plus source
files, every one of them resent on every request that follows. The Tools Used
line shows a long list of Reads.

**If the agent searched first, the refactor wins.** A `grep -l` for
`rate.?limit` returns the file list in one call, one `cat` answers the
question, and T7 lands near the bug fix. The Tools Used line shows a handful
of Bash or Grep calls and a single file read. T4 then takes the top spot for
the plain reason that it has to see three files to change three files.
Claude Code's current default is to search first, so in a room running Claude
Code this is the more common outcome. In a room running an agent that
browses, the first one is.

The two rankings, in cost per completed task:

| Kind | Agent read | Agent searched | Why |
|---|---|---|---|
| Bug fix (T1) | middling | lowest | cheap once located, expensive while searching |
| Refactor (T4) | high | highest | touches three files, needs to see all of them |
| Feature (T5) | middling | middling | bounded, two files plus a test |
| Exploration (T7) | highest | middling | all retrieval, so its cost is set by how it retrieves |

Either way the same thing is true and worth saying out loud: exploration
spends more tokens than a one-line fix for zero lines of code, and the only
variable is retrieval strategy. That is the lever Section 3 pulls, and an
agent that searched first has already pulled it. If yours did, the finding
is that the habit is cheap to adopt because the tool already has it. If
yours browsed, the finding is the size of the tax.

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
grep -rln "rate" src/orderly --include='*.py'
```

That returns a handful of paths. Reading one of them answers the question. An
agent that browses rather than searches will read `config.py`, `errors.py`,
the whole `api/` tree and several services before landing on the right file.
An agent that searches first does exactly what the command above does, in one
tool call, without being told. `ccwhy session`'s Tools Used line shows which
yours did.

## The controllable sink people name

In most cohorts the top answer is **MCP tool definitions**, followed by **the
rules file**. Both are fixed overhead: you pay them on every request in the
session whether or not they contribute anything to the task at hand. Tool
definitions are Section 5. The rules file is Section 3.

`ccwhy` lists them under "Controllable Token Sinks", though as one line,
"Cache creation (CLAUDE.md, MCP, system prompt)". It tells you the fixed
prefix is the sink without separating your rules file and tools from the
vendor's prompt. `/context` makes that split, which is why the two are run
together: one says how much and why, the other says made of what.

## Common wrong turns

- **Ranking kinds by `cost_usd` without looking at `tests_pass`.** A cheap row
  for a task that never passed is not a cheap kind. It is spend with nothing
  completed, and it ranks first, not last.
- **Treating the vendor system prompt as a sink.** It is overhead, but it is
  not yours to cut. Ignore it.
- **Measuring T7 by output tokens.** Exploration produces almost no output. All
  of its cost is on the input side, which is exactly why it is invisible to
  people who watch the wrong number.

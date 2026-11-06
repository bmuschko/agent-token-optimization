# Solution: Shrink a Tool Result

## What the numbers usually look like

Measured on a fresh clone of the course repo:

| Run | Size | About |
|---|---|---|
| `uv run pytest tests/tasks -v`, all acceptance tests red | 12,300 characters | 3,000 tokens |
| the same, through the docs hook (`grep -A 5 -E '(FAIL\|ERROR\|error:)' \| head -100`) | 3,200 characters | 800 tokens |
| the same, summary lines only (`grep -E '^(FAILED\|ERROR)\|passed\|failed'`) | 1,200 characters | 300 tokens |
| `uv run pytest -v`, the regression suite, all green | 1,800 characters | 450 tokens |

So the before delta is roughly 3,000 tokens and the after is 300 to 800, a four to ten times cut, and the agent's answer to "which tasks still fail" is the same every time because the lines it needs survive every filter. With tasks already passing from earlier exercises the log is shorter and the ratio similar.

Three thousand tokens is not much on its own. It is in the window for every later request of the session, so a 30-turn session carries it 30 times, and on a real repo the same log is 50 KB.

## Which cut holds

| Cut | Holds? | Why |
|---|---|---|
| `PreToolUse` hook | Every time | The command is rewritten before it runs; the model never sees the full log and cannot forget |
| Rules-file line | Usually on the first run, drifts later | It is an instruction the model weighs against everything else in the window; and Claude Code reads the file only at session start and on `/compact`, so a mid-session edit changes nothing until then |
| The prompt | Only when you write it | Nothing persists; next task, next person, the log is back |

The hook is the one to keep where it exists. Elsewhere the rules line is the best available, with the habit of checking the transcript the first few times. The prompt is for one-off situations.

## What to do with it, in order

1. **Narrow the request** when you can: the specific prompt, the summary flag. Costs nothing, cannot lose information you chose to keep.
2. **Automate the narrowing** so nobody has to remember: the hook in Claude Code, a rules line elsewhere. The same pattern filters build output, lint output, anything with a known noise shape.
3. **Route the noisy step to a subagent** when it is noisy by nature (a full CI log, a doc fetch): the output lives in the subagent's window and only the summary comes back.
4. **Compress what is left**, which is what the Headroom demo shows next, and what Exercise 6 measures through the proxy.

## Where this does not help

- **Outputs already small.** Filtering a 400-token result buys nothing; the regression suite on this repo is an example.
- **Filters that are too tight.** `grep FAILED` alone drops the summary line and the agent loses the count. The "done when" check exists for this.
- **Results you need in full.** A diff you are about to review is not noise. Filter the things you read past, not the things you read.

## The tool-definition leftover

If "Before you start" had you disable servers, the tools line in your context view is the before-and-after. For Claude Code, Codex and Copilot CLI users there was nothing to do: tool definitions are deferred by default and the line was already small. For scale, Anthropic's [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) puts a 50-plus-tool setup at about 72,000 tokens when loaded up front and the same request at about 8,700 with tool search on.

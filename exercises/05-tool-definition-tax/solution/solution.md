# Solution: Measure the Tool Tax

## What the numbers usually look like

| Servers connected | Typical definition overhead |
|---|---|
| 0 | nothing |
| 1 to 3 | 3,000 to 15,000 tokens |
| 5 | roughly 55,000 tokens |
| 10 or more | 100,000-plus, often most of the window |

The 55,000 figure for a five-server setup is Anthropic's, from
[Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use).
With tool search enabled the same setup carries about 8,700 tokens, an 85% cut,
with the full library still reachable on demand.

Most people underestimate their own number before measuring, because plugins,
skills and agents register tools too. The count in your settings panel is not
the count in your context.

## The result worth landing

Tool selection accuracy on Anthropic's MCP evaluations went **up** when the
definitions came out of context:

| Model | All tools loaded | Tool search enabled |
|---|---|---|
| Opus 4 | 49% | 74% |
| Opus 4.5 | 79.5% | 88.1% |

This is the strongest claim in the course and it is counterintuitive: removing
context made the agent better, not merely cheaper. The mechanism is mundane.
Picking the right tool out of four hundred is a harder problem than picking out
of ten, for a model as much as for a person.

## What to actually do, in order

1. **Remove servers you do not use.** Free, immediate, no feature flags.
2. **Keep two or three high-frequency tools always loaded**, defer the rest.
   Getting this split wrong is where the latency cost shows up: a tool search
   round trip on every request is worse than carrying ten definitions.
3. **Only then** worry about compressing what the tools return. That is
   Exercise 6 territory.

## Where this does not help

Say this part out loud, because the numbers above oversell it for some setups:

- **Few tools connected.** Deferring six tools saves nothing worth the round
  trip.
- **Retrieval misses.** Search adds a step, and a wrong pick costs you twice.
  Independent reports of retrieval accuracy in production have been noticeably
  less flattering than the vendor evaluations.
- **Latency-sensitive work.** Every indirection adds a round trip.

## The side task answer

For anyone with no MCP servers: reading
`src/orderly/api/middleware/rate_limit.py` costs roughly 700 to 900 tokens.
Grepping for `rate` across `src/orderly` and reading only the matching lines
costs well under 200, and answers the T7 question just as completely.

That ratio is the whole of Section 3 in miniature, and it holds whether or not
you have a single MCP server connected.

## What compression actually buys you

Once the definitions are out of context, the next question is always whether to
compress what the tools return. Run it yourself before you believe a number:

```bash
headroom savings            # durable report
headroom dashboard          # live view, proxy must be running
make test                   # the only verdict that counts
```

The headline claim for tool output compression is 60 to 95% fewer tokens. That
figure describes **JSON-heavy payloads**. On coding agent traffic the same
project reports roughly **15 to 20%**. Both numbers are true, and only one
describes your workload.

Take the generous half seriously, though, because cynicism is not the lesson. A
real 18% on a bill you are already paying, with no behaviour change, is worth
having. What makes it worth having is the test suite going green afterwards,
not the token counter going down.

## Questions this raises

- **Is the compression lossy?** Originals are stored locally and the model can
  retrieve the full text when it needs it. The honest answer to whether that is
  safe enough for your repo is your own test suite, not the architecture.
- **Why not just use compression and skip the rest?** Because it addresses one
  row of the decision tree, the outputs you do not control. Context discipline
  and model routing are bigger, cheaper, and free.
- **Does it work with Cursor or Copilot?** `headroom wrap cursor` prints a
  config to paste. `headroom wrap copilot` starts the proxy and launches.

## Common wrong turns

- **Measuring in absolute tokens only.** The percentage is what makes it stick.
- **Disabling a server you actually need mid-session.** That is a prefix
  change; it invalidates the cache and costs you a full rewrite. Toggle servers
  between sessions.
- **Treating the 85% as your number.** It describes a five-server setup. Yours
  is whatever you just measured.

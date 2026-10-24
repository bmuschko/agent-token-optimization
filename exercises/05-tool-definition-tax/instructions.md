# Exercise 5: Measure the Tool Tax

**Section 5 · 10 minutes · work alone**

## Objective

Put a number on the MCP tool definitions your agent loads before you type a character, then cut it and measure again.

## Before you start: the proxy enters here

Everything so far was read from the agent's own session logs. The last two exercises need the Headroom proxy: this one for agents other than Claude Code, Exercise 6 for everyone. Start it now, in one terminal at the repository root, in passthrough mode so it measures without changing anything:

```bash
headroom proxy --no-optimize
```

In a second terminal, also at the root, confirm it is up and launch your agent through it:

```bash
headroom doctor                                     # proxy, readiness, version must pass
headroom wrap claude --no-proxy --project-settings  # or: codex | copilot | cursor
```

`doctor`'s `claude` row turns green only when run from the directory you launched `wrap` in. The `savings` row, which names how long ago the proxy saw a request, is the check that works from anywhere.

## Steps

1. **Measure the tax.**

   **Claude Code** reports it directly:

   ```
   /context
   ```

   Look for the tool definitions line and note it as a **percentage of the window**, not just an absolute number.

   **Why `/context` and not the proxy.** The tax is a share of the window, and only the agent knows what is in its window. The proxy sees requests on the wire; it cannot tell tool schemas from conversation, and with on-demand tool loading the deferred schemas never cross the wire at all. `/context` reports the window itself, with tool definitions as their own line.

   **Copilot CLI** has `/context` too, and **Cursor** shows the same thing when you click the context ring: the Tools and MCP buckets, as tokens and as a share of the window. Read those.

   **Copilot in VS Code** has no breakdown, so measure by difference: send an identical trivial request in two fresh chats, once with your MCP servers enabled and once with them disabled, and compare the context token figure in the context window control. If you launched the CLI through the proxy, the same diff works from `headroom savings`, reset between the two readings so each stands alone:

   ```bash
   headroom savings --reset
   # one trivial request, servers enabled
   headroom savings          # before
   headroom savings --reset
   # the same request, servers disabled
   headroom savings          # after
   ```

   The proxy diff does not work for Cursor; its requests never pass through a local proxy.

2. **Record it as a share of a typical request.** "31% of every request I send" is a number you will remember. "18,400 tokens" is not.

3. **Cut it**, using whichever of these your tooling supports:

   - **Check that deferred loading is on.** Claude Code, Cursor and Copilot CLI all defer MCP tool definitions by default now: only the tool names ride along until a tool is used, and `/context` lists the deferred figure on its own line. If your tax is a large share of the window, something is loading up front, and Claude Code's `/context` says which.
   - **Disable every server you have not used in a month.** With deferral on, this is the cut that is left, and it is the larger one anyway: the names, the server instructions and the attention they take are paid whether or not the schemas load.

4. **Measure again. Post before and after in chat.**

## If you have no MCP servers connected

Your tax is zero and that is a legitimate result. Use the time on a side task instead: measure what `Read`ing `src/orderly/api/middleware/rate_limit.py` costs against `Grep`ping for `rate` across `src/orderly`, answering the same T5 question both ways.

## Done when

- A before number, as a percentage of a request
- An after number
- One sentence naming what you removed

## If you get stuck

- **Deferred loading is off or unavailable**, for example on some cloud-provider deployments. Fall back to disabling unused servers. Note which tools you lost access to; that is the real trade-off.
- **You cannot tell which servers are loaded.** Claude Code: `/mcp`. Cursor and Copilot: your MCP settings panel.

The reference answers are in [solution/solution.md](solution/solution.md).

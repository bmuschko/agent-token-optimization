# Exercise 5: Measure the Tool Tax

**Section 5 · 10 minutes · work alone**

## Objective

Put a number on the MCP tool definitions your agent loads before you type a
character, then cut it and measure again.

## Steps

1. **Measure the tax.**

   **Claude Code** reports it directly:

   ```
   /context
   ```

   Look for the tool definitions line and note it as a **percentage of the
   window**, not just an absolute number.

   **Other agents**: send an identical trivial request twice, once with your
   MCP servers enabled and once with them disabled, and diff the input token
   count the proxy reports.

   ```bash
   headroom stats     # before and after
   ```

2. **Record it as a share of a typical request.** "31% of every request I send"
   is a number you will remember. "18,400 tokens" is not.

3. **Cut it**, using whichever of these your tooling supports:

   - **Deferred loading / tool search**, if your agent exposes it. Mark the
     long tail of tools `defer_loading: true` and keep your two or three
     highest-frequency tools always loaded.
   - **Otherwise, disable every server you have not used in a month.** This is
     not a consolation prize. It is often the larger win and it is available
     to everyone today.

4. **Measure again. Post before and after in chat.**

## If you have no MCP servers connected

Your tax is zero and that is a legitimate result. Use the time on a side task
instead: measure what `Read`ing `src/orderly/api/middleware/rate_limit.py`
costs against `Grep`ping for `rate` across `src/orderly`, answering the same
T7 question both ways.

## Done when

- A before number, as a percentage of a request
- An after number
- One sentence naming what you removed

## If you get stuck

- **Deferred loading is not available in your version.** Fall back to disabling
  unused servers. Note which tools you lost access to; that is the real
  trade-off.
- **You cannot tell which servers are loaded.** Claude Code: `/mcp`. Cursor and
  Copilot: your MCP settings panel.
- **Replay mode.** `replays/tool-tax/` has a five-server session before and
  after deferred loading.

The reference answers are in [solution/solution.md](solution/solution.md).

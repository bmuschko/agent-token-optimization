# Exercise 6: Tool Output Compression

**Section 5 · 7 minutes · work alone**

## Objective

Put the Headroom proxy between your agent and the API, send the same noisy tool result through it that Exercise 5 measured, and read what compression saved and whether the answer survived.

## Before you start: the proxy enters here

This is the one exercise that needs the Headroom proxy. You installed it from [INSTALL.md](../../INSTALL.md#headroom-the-measuring-proxy) before the course; if not, do that first, it is one command.

Remove whatever Exercise 5 left behind, so the test log arrives unfiltered and compression has something to work on:

```bash
rm -f .claude/settings.local.json     # the hook
git checkout -- CLAUDE.md             # the rules line; or AGENTS.md, .github/copilot-instructions.md
```

Cursor users: the proxy cannot see your requests, which go through Cursor's servers. Pair with a neighbour on a CLI agent for this one; the reading is theirs, the comparison is yours.

## The measurement

Two numbers from `headroom savings`: the tokens the proxy **forwarded** to the API and the tokens it **saved** by compressing before forwarding. The ledger is cumulative and global, so reset it before the measured run. The second half of the measurement is not a number: the agent's answer to the question, compared with the answer it gave in Exercise 5 without the proxy.

## Steps

1. **Start the proxy with optimization on**, confirm it, and launch your agent through it:

   ```bash
   headroom proxy                                      # terminal 1, at the repo root
   headroom doctor                                     # terminal 2: proxy, readiness, version must pass
   headroom savings --reset                            # start the ledger at zero
   headroom wrap claude --no-proxy --project-settings  # or: codex | copilot
   ```

   `doctor`'s `claude` row turns green only when run from the directory you launched `wrap` in; the `savings` row, which names how long ago the proxy saw a request, is the check that works from anywhere. A zero counter after a turn means the agent is not routed through the proxy.

2. **Send the Exercise 5 question**, word for word, in the fresh session `wrap` opened:

   > Run the acceptance tests in `tests/tasks` and tell me which tasks still fail.

   Write down which tasks it said still fail, then `/exit`.

3. **Read the ledger:**

   ```bash
   headroom savings
   ```

   Note forwarded and saved. The saving is almost entirely the test log: the proxy's log compressor drops the repeated lines and keeps the failures, so the model read a short version of what Exercise 5 showed you in full.

4. **Compare the answer** with the one from Exercise 5 step 1. Same failing tasks, or not. That is the half of the result the token counter cannot give you.

5. **If you have a minute left, one more turn** with nothing noisy in it:

   ```bash
   headroom savings --reset
   # one ordinary turn in a fresh session, e.g. "what does utils/retry.py do?"
   headroom savings
   ```

   Expect close to nothing saved. Compression pays on repetitive tool output; on prose and code it barely moves, which is the caveats slide in one reading.

6. **Post in chat**: `forwarded N, saved N, same answer yes|no`.

## Done when

- A forwarded and a saved figure for the acceptance-test turn
- The agent named the same failing tasks as in Exercise 5, or you noted what changed
- Optionally, a second pair for a turn without a tool result

## Expect

The test log is where the saving is. Headroom's own example takes a 10,144-token log dump to 1,260 tokens with the failure line kept; your acceptance log is smaller, so expect a smaller absolute number and a similar shape. Over the whole request the share is lower, because the system prompt, the rules file and the model's own text are not compressed. On the turn in step 5, close to zero.

Compare with Exercise 5: the hook removed the same noise before it ever reached the agent, for free. Compression is for the output you could not filter, and the answer has to survive it, which is what step 4 checks.

## If you get stuck

- **`headroom savings` shows nothing.** The agent is not routed. Run `headroom doctor` from the directory you ran `wrap` in; if the `claude` row is red, start the agent again with `headroom wrap`.
- **Saved is zero.** The hook or rules line is still in place and the log arrived already filtered. Check the "before you start" commands, then rerun.
- **The answer changed.** Write down what it got wrong. It is the most useful result in the room and the caveats slide is about exactly this.
- **Corporate network blocks the proxy.** SSL-inspecting networks are the usual cause. Watch a neighbour's run; the comparison in step 4 is the part to take home.

The reference answers are in [solution/solution.md](solution/solution.md).

# Instructor Demo: Compression in One Command

**Section 5 · 5 minutes · instructor only**

Not a learner exercise. This is the script for the live demo, with the
failure modes already worked out.

## What the room sees

A task whose tools return verbose JSON and log output, run twice, with a live
token counter, ending on a green test suite.

## Script

```bash
# 1. Before. Run the task without the proxy and show the counter.
#    Use T4: its full-suite verification produces genuinely verbose output.
make test

# 2. Wrap the agent in one command.
headroom wrap claude

# 3. Confirm routing before you trust a single number.
headroom doctor

# 4. Replay the same task. Narrate the counter as it moves.

# 5. Show the savings.
headroom stats

# 6. The beat that matters.
make test
```

## Pre-record it

Five minutes is not enough to recover from a live failure. Have the recording
cued and cut to it without apology if anything hangs. Never install anything
live; the proxy should be warm and `headroom doctor` green before the session
starts.

## The line to land

The headline claim is 60 to 95% fewer tokens. That figure describes
**JSON-heavy payloads**. On coding agent traffic the same project reports
roughly **15 to 20%**. Both numbers are true. Only one describes your workload.

So you test it against your repo's suite before you trust it. And then the
generous half, because cynicism is not the lesson: a real 18% on a bill you are
already paying, with no behaviour change, is worth having.

## Anticipated questions

- **"Is the compression lossy?"** Originals are stored locally and the model
  can retrieve full text when it needs them. Say that plainly, then return to
  the point that their test suite is the arbiter, not the architecture diagram.
- **"Why not just use this and skip the rest of the course?"** Because it
  addresses one row of the decision tree, the outputs you do not control.
  Context discipline and model routing are bigger, cheaper and free.
- **"Does it work with Cursor or Copilot?"** `headroom wrap cursor` prints a
  config to paste; `headroom wrap copilot` starts the proxy and launches.

## The persuasive moment

It is `make test` going green, not the token counter. Slow down there.
Everything before it is setup for that one line.

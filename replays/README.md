# Replays

Recorded agent sessions, for anyone who cannot run an agent live during the
course: no API access, a blocked corporate network, or a preference not to
spend tokens.

> **Status: not yet recorded.** The folders below are the ones the exercises
> reference. They have to be captured from a real run against this repo before
> the session, on whichever agent you want represented. Until they exist,
> `REPLAY_MODE=true` has nothing to read and learners without live access cannot
> follow along.

```bash
export REPLAY_MODE=true
```

Every exercise then reads from here instead of calling a model.

| Folder | Used by | What is in it |
|---|---|---|
| `baseline/` | Exercise 1 | T1 and T2 worked with unscoped habits |
| `mixed-tasks/` | Exercise 2 | T1, T4, T5 and T7, one of each kind |
| `scoped/` | Exercise 3 | T3 run twice, bloated and scoped |
| `routing/` | Exercise 4 | T1 to T6 on a frontier model and on a cheap model |
| `tool-tax/` | Exercise 5 | a five-server session before and after deferred loading |
| `compaction/` | Exercise 6 | a 40-turn session before and after `/compact` |

## What replays can and cannot show you

**They can** show the shape of the result: which task type dominates, how much a
scoped run saves, where the tool definitions sit in the window. Every exercise
is answerable from them.

**They cannot** give you your own numbers, which is the real product of the
course. The absolute token counts belong to the machine and the agent that
recorded them. If you can run live for even part of the session, do.

## Recording your own

Replays are captured straight from the proxy:

```bash
headroom proxy --port 8787
# work the task, then copy the session log into a folder here
```

If you record a clean set on an agent that is not represented here, a pull
request is welcome.

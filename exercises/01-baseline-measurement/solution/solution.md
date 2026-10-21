# Solution: Measure Your Baseline

There is no answer key for this exercise. The agent produced the fix, and your deliverable is a number. Read this after you have it; the first section in particular anchors anyone who reads it first.

## What the numbers usually look like

Across a typical cohort, the combined T1 plus T2 baseline lands between 15,000 and 120,000 input tokens. Same two tasks, same repo, same instructions, an eightfold spread. That spread is the point, and it comes from three habits, in descending order of cost:

1. Loading the whole repo, or a large slice of it, for a one-line fix
2. Carrying a session that was already long before T1 started
3. Running a frontier model on a one-character change

Nothing about the tasks themselves explains the difference.

## Reading your row

Two things to look for before the next exercise:

- **Cache write far above cache read.** Your prefix is changing between turns. Section 3 explains why that costs you and what to do about it.
- **Input tokens an order of magnitude above output.** Normal. Input is where the volume lives, and it is the lever Section 3 pulls.

The row for a session you named yourself:

```bash
npx tokscale@latest --json --no-spinner --today --group-by client,session,model \
  | uv run python scripts/session_row.py "$id"
```

Every session from today, one block each, when you did not name it:

```bash
npx tokscale@latest --json --no-spinner --today --group-by client,session,model \
  | uv run python scripts/session_row.py
```

## Comparing agents

tokscale prices every client from the same table, so a Codex row and a Claude Code row for T1 differ in what the agent sent, not in how the tokens were priced. Three cautions before you conclude anything from that:

- **The model dominates.** Two agents on the same frontier model land close together; the same agent on a frontier model and a small one do not. Section 4 separates the agent from the model.
- **Zero cache columns are a logging gap, not free caching.** An agent showing zero cache read and zero cache write is not logging those figures, and the input figure carries the whole prompt. Compare the cost column instead of the split.
- **Cursor rows are a difference of totals**, so anything else that used the account between the two snapshots is in the row.

To learn what T1 costs on another agent, run it there in a fresh session and read the row the same way. The method in [instructions.md](../instructions.md) does not change, only the launch command.

## T1, what the fix is

The tier table is inclusive of its thresholds, so the comparison has to be `>=` rather than `>`. One character, in `rate_for_subtotal`:

```diff
-        if subtotal_cents > threshold * 100:
+        if subtotal_cents >= threshold * 100:
```

**Why the bug is easy to miss.** The regression suite covers $250.00 and $750.00, both comfortably inside a tier, so it stays green while the boundary is wrong. Only `make task T=t1` exercises the thresholds. A green suite is a floor, not a proof.

## T2, what the fix is, and the trap

Two edits in `src/orderly/cli.py`, plus importing `json`. Add the flag to the `report` subparser:

```python
report.add_argument(
    "--format", choices=("text", "json"), default="text",
    help="Output format",
)
```

Then branch on it where the report is written:

```python
if args.format == "json":
    sys.stdout.write(json.dumps(summary, indent=2) + "\n")
else:
    sys.stdout.write(render_text(summary))
```

**The trap.** An agent given the whole repo will often reach for `orderly.reporting.exporters` and add a third exporter there. That is more code than the task needs, costs correspondingly more tokens, and if it changes the default output it fails `test_text_remains_the_default`. A T2 row with a high token count and more than one attempt usually went this way.

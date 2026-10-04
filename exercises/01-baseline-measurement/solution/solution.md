# Solution: Establish Your Baseline

## What the numbers usually look like

Across a typical cohort, the combined T1 plus T2 baseline lands somewhere
between 15,000 and 120,000 input tokens. That spread is the point of the
exercise, not an error. Same two tasks, same repo, same instructions, and an
eightfold difference in what people spend.

The spread comes from three habits, in descending order of cost:

1. Loading the whole repo, or a large slice of it, for a one-line fix
2. Carrying a session that was already long before T1 started
3. Running a frontier model on a one-character change

Nothing about the tasks themselves explains the difference.

## T1 reference fix

The tier table is inclusive of its thresholds, so the comparison has to be
`>=` rather than `>`. One character, in `rate_for_subtotal`:

```python
for threshold, tier_rate in TIERS:
    if subtotal_cents >= threshold * 100:
        rate = tier_rate
```

A complete fixed file is in [discount.py](discount.py).

**Why the bug is easy to miss.** The regression suite covers 250.00 and
750.00, both comfortably inside a tier, so it stays green while the boundary
is wrong. Only `make task T=t1` exercises the thresholds themselves. This is
worth saying out loud to learners: a green suite is a floor, not a proof.

## T2 reference fix

Two edits. Add the flag to the `report` subparser in `src/orderly/cli.py`:

```python
report.add_argument(
    "--format", choices=("text", "json"), default="text",
    help="Output format",
)
```

Then branch on it where the report is written:

```python
if args.command == "report":
    summary = build_summary(repository.all(), status=args.status, region=args.region)
    if args.format == "json":
        sys.stdout.write(json.dumps(summary, indent=2) + "\n")
    else:
        sys.stdout.write(render_text(summary))
    return 0
```

`json` needs importing at the top of the module. A complete fixed file is in
[cli.py](cli.py).

**The trap.** An agent given the whole repo will often reach for
`orderly.reporting.exporters` and add a third exporter there, which is more
code than the task needs and breaks `test_text_remains_the_default` if it
changes the default. Scoping the agent to `cli.py` and `summary.py` avoids it.

## Reading the baseline

Two things to look for in your own row before the next exercise:

- **Cache write far above cache read.** Your prefix is changing between turns.
  Section 3 explains why that costs you and what to do about it.
- **Input tokens an order of magnitude above output.** Normal and expected.
  Input is where the volume lives; that is the lever Section 3 pulls.

## Common wrong turns

- **Optimizing during the baseline.** It feels productive and it ruins the
  comparison. If you did it, say so and use your first run anyway.
- **Counting only the final successful attempt.** Attempts that failed still
  cost money. Cost per completed task divides total spend, including failures,
  by tasks that pass.
- **Forgetting to run the regression suite.** A task that passes its
  acceptance tests but breaks `make test` is not done.

#!/usr/bin/env python3
"""Print the token and cost figures of each session in a tokscale JSON report.

Run: npx tokscale@latest --json --no-spinner --today --group-by client,session,model \
       | uv run python scripts/session_row.py [SESSION_ID_OR_PREFIX]
"""
import json
import sys


def collapse_sessions(entries):
    """Sum the per-model entries of each session into one row."""
    rows = {}
    for entry in entries:
        row = rows.setdefault(
            entry["sessionId"],
            {"client": entry["client"], "models": [], "input_tokens": 0,
             "output_tokens": 0, "cache_read": 0, "cache_write": 0, "cost_usd": 0.0},
        )
        row["models"].append(entry["model"])
        row["input_tokens"] += entry["input"]
        row["output_tokens"] += entry["output"]
        row["cache_read"] += entry["cacheRead"]
        row["cache_write"] += entry["cacheWrite"]
        row["cost_usd"] += entry["cost"]
    return rows


def print_row(session_id, row):
    """Print one session as labelled figures, cost rounded to cents."""
    print(f"session={session_id} client={row['client']} model={'+'.join(row['models'])}")
    print(
        f"input_tokens={row['input_tokens']} output_tokens={row['output_tokens']} "
        f"cache_read={row['cache_read']} cache_write={row['cache_write']} "
        f"cost_usd={row['cost_usd']:.2f}"
    )


def main():
    """Print the matching session, or every session when no id is given."""
    report = json.load(sys.stdin)
    if "session" not in report.get("groupBy", ""):
        sys.exit("run tokscale with --group-by client,session,model")
    rows = collapse_sessions(report["entries"])
    wanted = sys.argv[1] if len(sys.argv) > 1 else ""
    matches = {sid: row for sid, row in rows.items() if sid.startswith(wanted)}
    if not matches:
        sys.exit(f"no session starting with {wanted!r} in this report")
    for session_id, row in matches.items():
        print_row(session_id, row)
        print()


if __name__ == "__main__":
    main()

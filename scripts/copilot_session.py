#!/usr/bin/env python3
"""Print the requests, token split and tool calls of a Copilot CLI session.

Input tokens are reported uncached, as tokscale does, so the four figures add up to what the model read.

Run: uv run python scripts/copilot_session.py [SESSION_ID_OR_PREFIX]
With no id, the most recently modified session is used.
"""
import json
import os
import sys
from collections import Counter
from pathlib import Path

STATE_DIR = Path(os.environ.get("COPILOT_HOME", Path.home() / ".copilot")) / "session-state"


def find_session(prefix):
    """Return the events.jsonl of the session matching the prefix, or the newest."""
    logs = [p / "events.jsonl" for p in STATE_DIR.iterdir() if (p / "events.jsonl").exists()]
    if prefix:
        logs = [p for p in logs if p.parent.name.startswith(prefix)]
    if not logs:
        sys.exit(f"no Copilot CLI session starting with {prefix!r} under {STATE_DIR}")
    return max(logs, key=lambda p: p.stat().st_mtime)


def main():
    """Summarize usage records and tool calls from the session's event log."""
    log = find_session(sys.argv[1] if len(sys.argv) > 1 else "")
    usage = {}
    tools = Counter()
    files = Counter()
    for line in open(log):
        event = json.loads(line)
        data = event.get("data", {})
        if event["type"] == "session.usage_record":
            u = data["usage"]
            row = usage.setdefault(u["model"], Counter())
            row["requests"] += 1
            for key in ("inputTokens", "outputTokens", "cacheReadTokens", "cacheWriteTokens"):
                row[key] += u.get(key, 0)
        elif event["type"] == "tool.execution_start":
            tools[data["toolName"]] += 1
            args = data.get("arguments")
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except ValueError:
                    args = {}
            path = (args or {}).get("path") if isinstance(args, dict) else None
            if path:
                files[path] += 1
    print(f"session={log.parent.name}")
    for model, row in usage.items():
        uncached = row["inputTokens"] - row["cacheReadTokens"] - row["cacheWriteTokens"]
        print(
            f"model={model} requests={row['requests']} · Input {uncached:,} · "
            f"Output {row['outputTokens']:,} · Cache read {row['cacheReadTokens']:,} · "
            f"Cache write {row['cacheWriteTokens']:,}"
        )
    print("tools: " + ", ".join(f"{name} x{n}" for name, n in tools.most_common()))
    for path, n in files.most_common():
        print(f"  {n}x {path}")


if __name__ == "__main__":
    main()

"""Export reports to flat formats."""
import csv
import io
from typing import Any, Dict


def to_csv(summary: Dict[str, Any]) -> str:
    """Render a summary as a single-row CSV document."""
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=sorted(summary.keys()))
    writer.writeheader()
    writer.writerow(summary)
    return buffer.getvalue()


def to_markdown(summary: Dict[str, Any]) -> str:
    """Render a summary as a two-column markdown table."""
    rows = ["| field | value |", "| --- | --- |"]
    for key in sorted(summary):
        rows.append(f"| {key} | {summary[key]} |")
    return "\n".join(rows) + "\n"

"""Command line entry point. Reference solution for T2."""
import argparse
import json
import sys
from typing import List, Optional

from orderly import __version__
from orderly.reporting.summary import build_summary, render_text
from orderly.repositories.order_repository import OrderRepository
from orderly.seed import load_seed_orders


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser."""
    parser = argparse.ArgumentParser(prog="orderly", description="Order tooling")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    report = sub.add_parser("report", help="Summarize orders")
    report.add_argument("--status", help="Only orders in this status")
    report.add_argument("--region", default="US-CO", help="Tax region")
    report.add_argument(
        "--format", choices=("text", "json"), default="text", help="Output format"
    )

    show = sub.add_parser("show", help="Show one order")
    show.add_argument("order_id")

    sub.add_parser("list", help="List order ids")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Run the CLI, returning a process exit code."""
    args = build_parser().parse_args(argv)
    repository = OrderRepository(load_seed_orders())

    if args.command == "report":
        summary = build_summary(repository.all(), status=args.status, region=args.region)
        if args.format == "json":
            sys.stdout.write(json.dumps(summary, indent=2) + "\n")
        else:
            sys.stdout.write(render_text(summary))
        return 0

    if args.command == "show":
        order = repository.get(args.order_id)
        if order is None:
            sys.stderr.write(f"no order with id {args.order_id}\n")
            return 1
        sys.stdout.write(f"{order['id']} {order['status']} {len(order['lines'])} lines\n")
        return 0

    if args.command == "list":
        for order in repository.all():
            sys.stdout.write(order["id"] + "\n")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())

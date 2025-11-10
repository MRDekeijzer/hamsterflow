"""Command-line interface for HamsterFlow."""

from __future__ import annotations

import argparse
from typing import Sequence

from hamsterflow.config import get_settings
from hamsterflow.ingest import fetch_and_extract


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HamsterFlow maintenance CLI")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch feeds without persisting results.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    settings = get_settings()

    results = fetch_and_extract(settings.rss_feeds)

    if args.dry_run:
        print(f"Fetched {len(results)} feeds (dry run).")
    else:
        print("Ingestion pipeline not yet implemented.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

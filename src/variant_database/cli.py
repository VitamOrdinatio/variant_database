"""Command-line interface for VDB."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vdb",
        description="Variant Database preservation-first evidence system.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print VDB CLI availability check.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.version:
        print("vdb CLI available")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

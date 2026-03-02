"""CLI entrypoint for Bob."""

from __future__ import annotations

import argparse

from bob import __version__


def build_parser() -> argparse.ArgumentParser:
    """Build the Bob CLI parser.

    Testing:
        - Verify --version exits 0 and prints a semantic version string.
        - Verify default invocation exits 0 and prints bootstrap status text.
    """
    parser = argparse.ArgumentParser(
        prog="bob",
        description="Bob voice assistant bootstrap CLI.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print package version and exit.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the Bob CLI.

    Testing:
        - Verify return code is 0 for default invocation.
        - Verify return code is 0 for --version invocation.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return 0

    print("Bob bootstrap entrypoint ready.")
    return 0

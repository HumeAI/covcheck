"""CLI entrypoint."""

import argparse

from covcheck._cli.config import Config
from covcheck._cli.validate import validate_coverage


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    :return: Argparse namespace containing the arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('coverage_file', help="Path to XML coverage file.")
    parser.add_argument('--line', default=None, type=float, help="Line coverage percentage threshold.")
    parser.add_argument('--branch', default=None, type=float, help="Branch coverage percentage threshold.")

    parser.add_argument('--output', default=None, type=str, help="Path to a file where output JSON should be saved.")
    parser.add_argument('--silent', default=False, action='store_true', help="Do not print coverage results.")

    parser.add_argument('--config', default=None, type=str, help="Path to pyproject.toml config file.")

    return parser.parse_args()


def run() -> None:
    """Run the covcheck CLI."""
    args = parse_args()

    config = Config.create(
        args.coverage_file,
        config_file=args.config,
        line=args.line,
        branch=args.branch,
        output=args.output,
        silent=args.silent,
    )

    validate_coverage(config)

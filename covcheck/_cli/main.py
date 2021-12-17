"""CLI entrypoint."""

import argparse
import json

from pathlib import Path
from typing import Optional, Union

from covcheck._parsing.coverage_result import CoverageResult
from covcheck._cli.utilities import fail_with_error


def validate_coverage(
    coverage_filepath: Union[str, Path],
    line_threshold: Optional[float] = None,
    branch_threshold: Optional[float] = None,
    output_filepath: Optional[Union[str, Path]] = None,
    verbose: bool = False,
) -> None:
    """Validate code coverage given an XML coverage file.

    :param coverage_filepath: XML coverage file from Coverage.py.
    :param line_threshold: Threshold for line coverage.
    :param branch_threshold: Threshold for branch coverage.
    :param output_filepath: Path on disk where a JSON output file should be saved.
    :param verbose: Whether the actaual coverage measurements should be printed to stdout.
    """
    _validate_thresholds(line_threshold, branch_threshold)

    result = CoverageResult.from_xml(coverage_filepath)

    if output_filepath is not None:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(result.tree.serialize(), f, indent=4)  # type: ignore

    if all(input_value is None for input_value in [line_threshold, branch_threshold, output_filepath]):
        fail_with_error("Must specify --line, --branch, or --output_filepath.")

    checks_failed = False

    line_rate = result.summary.line_rate * 100
    if line_threshold is not None:
        if line_rate < line_threshold:
            fail_with_error(f"Line coverage ({line_rate:.2f}%) below threshold ({line_threshold}%)", sys_exit=False)
            checks_failed = True
        elif verbose:
            print(f"Line coverage passed: {line_rate:.2f}%")

    branch_rate = result.summary.branch_rate * 100
    if branch_threshold is not None:
        if branch_rate < branch_threshold:
            fail_with_error(f"Branch coverage ({branch_rate:.2f}%) below threshold ({branch_threshold}%)",
                            sys_exit=False)
            checks_failed = True
        elif verbose:
            print(f"Branch coverage passed: {branch_rate:.2f}%")

    if checks_failed:
        fail_with_error("One or more quality checks failed.")


def _validate_thresholds(
    line_threshold: Optional[float],
    branch_threshold: Optional[float],
) -> None:
    """Validate thresholds are within acceptable bounds.

    :param line_threshold: Threshold for line coverage.
    :param branch_threshold: Threshold for branch coverage.
    """
    coverage_map = {
        'line': line_threshold,
        'branch': branch_threshold,
    }
    for coverage_type, threshold in coverage_map.items():
        if threshold is not None and (threshold < 0 or threshold > 100):
            fail_with_error(
                f"Invalid threshold for {coverage_type} coverage ({threshold}). Must be between 0 and 100.")


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

    return parser.parse_args()


def run() -> None:
    """Run the covcheck CLI."""
    args = parse_args()

    validate_coverage(args.coverage_file, args.line, args.branch, args.output, not args.silent)

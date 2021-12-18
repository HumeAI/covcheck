"""Validation entrypoint."""

import json

from typing import Optional

from covcheck._parsing.coverage_result import CoverageResult
from covcheck._cli.utilities import fail_with_error
from covcheck._cli.config import Config


def validate_coverage(config: Config) -> None:
    """Validate code coverage given an XML coverage file.

    param: Config object.
    """
    _validate_thresholds(config.line, config.branch)

    result = CoverageResult.from_xml(config.coverage_filepath)

    if config.output is not None:
        with open(config.output, 'w', encoding='utf-8') as f:
            json.dump(result.tree.serialize(), f, indent=4)  # type: ignore

    required_args = [config.line, config.branch, config.output]
    if all(input_value is None for input_value in required_args):
        fail_with_error("Must specify --line, --branch, or --output_filepath.")

    checks_failed = False

    line_rate = result.summary.line_rate * 100
    if config.line is not None:
        if line_rate < config.line:
            fail_with_error(f"Line coverage ({line_rate:.2f}%) below threshold ({config.line}%)", sys_exit=False)
            checks_failed = True
        elif not config.silent:
            print(f"Line coverage passed: {line_rate:.2f}%")

    branch_rate = result.summary.branch_rate * 100
    if config.branch is not None:
        if branch_rate < config.branch:
            fail_with_error(f"Branch coverage ({branch_rate:.2f}%) below threshold ({config.branch}%)", sys_exit=False)
            checks_failed = True
        elif not config.silent:
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

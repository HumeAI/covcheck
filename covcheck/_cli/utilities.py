"""CLI utilities."""

import sys


class ColorCodes:
    """Color codes for color terminal printing"""
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def fail_with_error(
    message: str,
    sys_exit: bool = True,
    color: bool = True,
) -> None:
    """Print a colorized error message to the terminal.

    :param message: Message to print.
    :param sys_exit: Whether to exit the Python interpreter with sys.exit().
    :param color: Whether to write output in color.
    """
    full_message = message
    if color:
        full_message = f"{ColorCodes.FAIL}{ColorCodes.BOLD}{message}{ColorCodes.END}"

    print(full_message, file=sys.stderr)

    if sys_exit:
        sys.exit(1)

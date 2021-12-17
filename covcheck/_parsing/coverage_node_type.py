"""Types of coverage nodes."""

from enum import Enum


class CoverageNodeType(Enum):
    """Types of coverage nodes."""

    DIR = 'dir'
    FILE = 'file'

"""Coverage result."""

from pathlib import Path
from typing import Union

from covcheck._parsing.coverage_node import CoverageNode
from covcheck._parsing.coverage_summary import CoverageSummary
from covcheck._parsing.coverage_xml_parser import CoverageXMLParser


class CoverageResult:
    """Coverage result."""
    def __init__(self, tree: CoverageNode):
        self.tree = tree

    @property
    def summary(self) -> CoverageSummary:
        """Get the result CoverageSummary."""
        return self.tree.summary

    @classmethod
    def from_xml(cls, filepath: Union[str, Path]) -> 'CoverageResult':
        """Create a CoverageResult by parsing an XML coverage file.

        :param filepath: Path on disk to an XML coverage file.
        """
        tree = CoverageXMLParser.parse(filepath)
        return cls(tree)

"""Coverage node."""

from pathlib import Path
from typing import Any, Dict, Generator, Optional, Union

from covcheck._parsing.coverage_summary import CoverageSummary
from covcheck._parsing.coverage_node_type import CoverageNodeType


class CoverageNode:
    """Coverage node."""
    def __init__(self, name: str, node_type: CoverageNodeType, summary: Optional[CoverageSummary] = None):
        """Construct CoverageNode.

        :param name: Name of the coverage node.
        :param node_type: Type of the coverage node.
        :param summary: Summary of coverage for the node.
        """
        self._name = name
        self._node_type = node_type
        self._summary = summary
        self._children = {}  # type: Dict[str, CoverageNode]

    @property
    def name(self) -> str:
        """Get the CoverageNode name.

        :return: CoverageNode name.
        """
        return self._name

    @property
    def node_type(self) -> CoverageNodeType:
        """Get the CoverageNode type.

        :return: CoverageNode type.
        """
        return self._node_type

    def add_child(self, node: 'CoverageNode', dirpath: Optional[Union[Path, str]] = None) -> None:
        """Add a child node to the current node's children.

        :param node: CoverageNode to add as a child.
        :param path: Relative path to the parent of the child to add.
        """
        self._summary = None

        if dirpath is None:
            if node.name in self._children:
                raise ValueError(f"A node with the name {node.name} was already added as a child")
            self._children[node.name] = node
            return

        path = Path(dirpath)

        if len(path.parts) == 0:
            raise ValueError(f"Invalid child dirpath: '{path}'")

        directory_name = path.parts[0]
        remaining_path = Path(*path.parts[1:]) if len(path.parts) > 1 else None

        if directory_name not in self._children:
            directory_node = CoverageNode(directory_name, node_type=CoverageNodeType.DIR)
            self._children[directory_name] = directory_node

        self._children[directory_name].add_child(node, dirpath=remaining_path)

    @property
    def summary(self) -> CoverageSummary:
        """Get a CoverageSummary for the node.

        :return: CoverageSummary for the node.
        """
        if self._summary is not None:
            return self._summary

        summary = CoverageSummary(0, 0, 0, 0)
        for child in self.children():
            summary.n_lines += child.summary.n_lines
            summary.n_lines_covered += child.summary.n_lines_covered
            summary.n_branches += child.summary.n_branches
            summary.n_branches_covered += child.summary.n_branches_covered
        self._summary = summary
        return self._summary

    def serialize(self) -> Dict[str, Any]:
        """Serialize a tree of CoverageNodes to a tree of Python dictionaries.

        :return: Dictionary representation of the coverage tree.
        """
        summary = {
            'n_lines': self.summary.n_lines,
            'line_rate': self.summary.line_rate,
            'n_lines_covered': self.summary.n_lines_covered,
            'n_branches': self.summary.n_branches,
            'branch_rate': self.summary.branch_rate,
            'n_branches_covered': self.summary.n_branches_covered,
        }
        children = [child.serialize() for child in self.children()]
        node = {
            'name': self.name,
            'summary': summary,
            'node_type': self.node_type.value,
            'children': children,
        }
        return node

    def children(self) -> Generator['CoverageNode', None, None]:
        """Iterate over CoverageNode children."""
        for _, child in self._children.items():
            yield child

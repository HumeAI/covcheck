from pathlib import Path

import pytest

from covcheck import CoverageNode
from covcheck import CoverageNodeType
from covcheck import CoverageSummary


class TestCoverageNode:
    def test_construct(self) -> None:
        node = CoverageNode('myfile', CoverageNodeType.FILE)
        assert node.name == 'myfile'
        assert node.node_type == CoverageNodeType.FILE
        assert len(list(node.children())) == 0
        assert node.summary.n_lines == node.summary.n_branches == 0
        assert node.summary.line_rate == node.summary.branch_rate == 0

    def test_add_child(self) -> None:
        node = CoverageNode('file-1', CoverageNodeType.DIR)
        child_node = CoverageNode('file-2', CoverageNodeType.FILE)
        node.add_child(child_node, dirpath='dir-1')

        children = list(node.children())
        assert len(children) == 1
        assert children[0].name == 'dir-1'

        grandchildren = list(children[0].children())
        assert len(grandchildren) == 1
        assert grandchildren[0].name == 'file-2'

    def test_add_children_same_dir(self) -> None:
        node = CoverageNode('parent', CoverageNodeType.DIR)
        node.add_child(CoverageNode('file-1.txt', CoverageNodeType.FILE), dirpath=Path('dir-1'))
        node.add_child(CoverageNode('file-2.txt', CoverageNodeType.FILE), dirpath=Path('dir-1'))

        assert len(list(list(node.children())[0].children())) == 2

    def test_add_child_invalid_dirpath(self) -> None:
        node = CoverageNode('parent', CoverageNodeType.DIR)
        with pytest.raises(ValueError, match="Invalid child dirpath: '.'"):
            node.add_child(CoverageNode('file-1.txt', CoverageNodeType.FILE), dirpath=Path('dir-1').parent)

    def test_duplicate_children(self) -> None:
        name = 'file-1.txt'
        child_node_1 = CoverageNode(name, CoverageNodeType.FILE)
        child_node_2 = CoverageNode(name, CoverageNodeType.FILE)
        parent_node = CoverageNode('parent', CoverageNodeType.DIR)

        parent_node.add_child(child_node_1)
        with pytest.raises(ValueError, match="A node with the name file-1.txt was already added as a child"):
            parent_node.add_child(child_node_2)

    def test_summary_aggregate(self) -> None:
        child_summary_1 = CoverageSummary(12, 6, 5, 2)
        child_node_1 = CoverageNode('file-1.txt', CoverageNodeType.FILE, summary=child_summary_1)

        child_summary_2 = CoverageSummary(8, 2, 5, 1)
        child_node_2 = CoverageNode('file-2.txt', CoverageNodeType.FILE, summary=child_summary_2)

        parent_node = CoverageNode('parent', CoverageNodeType.DIR)
        parent_node.add_child(child_node_1)
        parent_node.add_child(child_node_2)
        assert parent_node.summary.n_lines == 20
        assert parent_node.summary.line_rate == 0.4
        assert parent_node.summary.n_branches == 10
        assert parent_node.summary.branch_rate == 0.3

    def test_serialize(self) -> None:
        summary = CoverageSummary(12, 6, 5, 2)
        node = CoverageNode('file-1', CoverageNodeType.FILE, summary=summary)
        serialized = node.serialize()
        assert serialized == {
            'children': [],
            'name': 'file-1',
            'node_type': 'file',
            'summary': {
                'n_lines': 12,
                'n_lines_covered': 6,
                'line_rate': 0.5,
                'n_branches': 5,
                'n_branches_covered': 2,
                'branch_rate': 0.4,
            }
        }

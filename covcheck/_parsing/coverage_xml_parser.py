"""XML parser for coverage files."""

import re

from pathlib import Path
from typing import Union
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from covcheck._parsing.coverage_node import CoverageNode
from covcheck._parsing.coverage_node_type import CoverageNodeType
from covcheck._parsing.coverage_summary import CoverageSummary


class CoverageXMLParser:
    """XML parser for coverage files."""
    @classmethod
    def parse(cls, filepath: Union[str, Path]) -> CoverageNode:
        """Parse an XML coverage file into a covcheck tree.

        :param filepath: Path on disk to an XML coverage file.
        """
        xml_tree = ElementTree.parse(filepath)
        xml_root = xml_tree.getroot()

        root_node = CoverageNode('root', node_type=CoverageNodeType.DIR)

        xml_packages = cls._try_get_child(xml_root, 'packages')
        for xml_package in xml_packages:
            xml_classes = cls._try_get_child(xml_package, 'classes')
            for xml_class in xml_classes:
                code_filename = xml_class.attrib['name']
                full_filepath = xml_class.attrib['filename']
                code_dirpath = Path(full_filepath).parent if '/' in full_filepath else None

                summary = CoverageSummary(0, 0, 0, 0)
                xml_lines = cls._try_get_child(xml_class, 'lines')
                for xml_line in xml_lines:
                    summary.n_lines += 1
                    if xml_line.attrib['hits'] == '1':
                        summary.n_lines_covered += 1

                    if 'branch' in xml_line.attrib and xml_line.attrib['branch']:
                        branch_condition = xml_line.attrib['condition-coverage']
                        pattern = r"^\d+% \((\d+)\/(\d+)\)$"
                        match = re.match(pattern, branch_condition)

                        if match is None:
                            raise ValueError(f"Failed to parse condition-coverage XML: {branch_condition}")

                        summary.n_branches_covered += int(match.group(1))
                        summary.n_branches += int(match.group(2))

                node = CoverageNode(code_filename, node_type=CoverageNodeType.FILE, summary=summary)
                root_node.add_child(node, dirpath=code_dirpath)

        return root_node

    @classmethod
    def _try_get_child(cls, xml_element: Element, tag: str) -> Element:
        for xml_child in xml_element:
            if xml_child.tag == tag:
                return xml_child
        raise ValueError(f"Could not parse coverage XML, no attribute '{tag}'")

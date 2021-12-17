import re
from pathlib import Path
from xml.etree.ElementTree import Element, ParseError

import pytest

from covcheck._parsing.coverage_xml_parser import CoverageXMLParser


class TestCoverageXmlParser:
    def test_parser_invalid_xml(self, tmp_path: Path) -> None:
        filepath = tmp_path / 'coverage.txt'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("[invalid xml]")

        parser = CoverageXMLParser()
        with pytest.raises(ParseError, match="syntax error: line 1, column 0"):
            parser.parse(filepath)

    def test_parser_invalid_condition(self, invalid_coverage_filepath: Path) -> None:
        parser = CoverageXMLParser()
        with pytest.raises(ValueError, match=re.escape("Failed to parse condition-coverage XML: 0% (0//2)")):
            parser.parse(invalid_coverage_filepath)

    def test_fail_try_get_child(self) -> None:
        element = Element('tag')
        with pytest.raises(ValueError, match="Could not parse coverage XML, no attribute 'attr'"):
            CoverageXMLParser._try_get_child(element, 'attr')

    def test_parser(self, coverage_filepath: Path) -> None:
        parser = CoverageXMLParser()
        node = parser.parse(coverage_filepath)
        assert node.name == 'root'

        children = list(node.children())
        assert len(children) == 2

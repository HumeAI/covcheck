import math

from pathlib import Path

from covcheck import CoverageResult


class TestCoverageResult:
    def test_result(self, coverage_filepath: Path) -> None:
        result = CoverageResult.from_xml(coverage_filepath)
        assert math.isclose(result.summary.line_rate, 0.7561837455830389)
        assert math.isclose(result.summary.branch_rate, 0.5057471264367817)

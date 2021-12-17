from covcheck import CoverageSummary


class TestCoverageSummary:
    def test_construct(self) -> None:
        summary = CoverageSummary(10, 2, 8, 4)
        assert summary.n_lines == 10
        assert summary.n_lines_covered == 2
        assert summary.line_rate == 0.2
        assert summary.n_branches == 8
        assert summary.n_branches_covered == 4
        assert summary.branch_rate == 0.5

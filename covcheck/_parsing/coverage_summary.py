"""Coverage summary."""


class CoverageSummary:
    """Coverage summary."""
    def __init__(
        self,
        n_lines: int,
        n_lines_covered: int,
        n_branches: int,
        n_branches_covered: int,
    ):
        self.n_lines = n_lines
        self.n_lines_covered = n_lines_covered
        self.n_branches = n_branches
        self.n_branches_covered = n_branches_covered

    @property
    def line_rate(self) -> float:
        """Get the summary line rate."""
        if self.n_lines == 0:
            return 0
        return 1.0 * self.n_lines_covered / self.n_lines

    @property
    def branch_rate(self) -> float:
        """Get the summary branch rate."""
        if self.n_branches == 0:
            return 0
        return 1.0 * self.n_branches_covered / self.n_branches

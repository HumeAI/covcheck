import json
from pathlib import Path

import pytest

from utilities.process_utilities import run_command

from covcheck._cli.main import validate_coverage
from covcheck._cli.config import Config


class TestMain:
    def test_run(self) -> None:
        command = ["covcheck", "--help"]
        output = run_command(command)

        assert len(output.stderr) == 0
        assert "usage: covcheck" in output.stdout

    def test_validate_coverage_silent(self, capsys: pytest.CaptureFixture, coverage_filepath: Path) -> None:
        validate_coverage(Config(coverage_filepath, line=0, branch=0, silent=True))

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_validate_coverage_verbose(self, capsys: pytest.CaptureFixture, coverage_filepath: Path) -> None:
        validate_coverage(Config(coverage_filepath, line=0, branch=0))

        captured = capsys.readouterr()
        assert "Line coverage passed: 75.62" in captured.out
        assert "Branch coverage passed: 50.57%" in captured.out

    def test_validate_coverage_verbose_line(self, capsys: pytest.CaptureFixture, coverage_filepath: Path) -> None:
        validate_coverage(Config(coverage_filepath, line=0))

        captured = capsys.readouterr()
        assert "Line coverage passed: 75.62" in captured.out

    def test_validate_coverage_verbose_branch(self, capsys: pytest.CaptureFixture, coverage_filepath: Path) -> None:
        validate_coverage(Config(coverage_filepath, branch=0))

        captured = capsys.readouterr()
        assert "Branch coverage passed: 50.57%" in captured.out

    def test_validate_coverage_verbose_neither_fail(self, capsys: pytest.CaptureFixture,
                                                    coverage_filepath: Path) -> None:
        with pytest.raises(SystemExit):
            validate_coverage(Config(coverage_filepath))

        captured = capsys.readouterr()
        expected = "Must specify --line, --branch, or --output_filepath."
        assert expected in captured.err

    def test_validate_coverage_fail(self, capsys: pytest.CaptureFixture, coverage_filepath: Path) -> None:
        with pytest.raises(SystemExit):
            validate_coverage(Config(coverage_filepath, line=100, branch=100))

        captured = capsys.readouterr()
        expected = "Line coverage (75.62%) below threshold (100%)"
        assert expected in captured.err

    def test_validate_coverage_invalid_threshold(self, capsys: pytest.CaptureFixture, coverage_filepath: Path) -> None:
        with pytest.raises(SystemExit):
            validate_coverage(Config(coverage_filepath, line=101, branch=100))

        captured = capsys.readouterr()
        expected = "Invalid threshold for line coverage (101). Must be between 0 and 100."
        assert expected in captured.err

    def test_json_output(self, tmp_path: Path, coverage_filepath: Path) -> None:
        output_filepath = tmp_path / 'coverage.json'
        validate_coverage(Config(coverage_filepath, output=output_filepath))

        with open(output_filepath, 'r', encoding='utf-8') as f:
            json.load(f)

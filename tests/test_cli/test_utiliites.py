import pytest

from covcheck._cli.utilities import fail_with_error


class TestUtilities:
    def test_fail_with_error(self, capsys: pytest.CaptureFixture) -> None:
        fail_with_error("Error message", sys_exit=False)

        captured = capsys.readouterr()
        assert "Error message" in captured.err

    def test_fail_with_error_no_color(self, capsys: pytest.CaptureFixture) -> None:
        fail_with_error("Error message", sys_exit=False, color=False)

        captured = capsys.readouterr()
        assert "Error message" in captured.err

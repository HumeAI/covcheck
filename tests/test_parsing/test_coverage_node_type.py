from covcheck import CoverageNodeType


class TestCoverageNodeType:
    def test_types(self) -> None:
        assert CoverageNodeType.DIR.value == 'dir'
        assert CoverageNodeType.FILE.value == 'file'

        assert len(list(CoverageNodeType)) == 2

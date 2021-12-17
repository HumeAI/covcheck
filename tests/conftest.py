from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def coverage_filepath() -> Path:
    return Path(__file__).parent / 'coverage_xml' / 'coverage.xml'


@pytest.fixture(scope='session')
def invalid_coverage_filepath() -> Path:
    return Path(__file__).parent / 'coverage_xml' / 'invalid-coverage.xml'

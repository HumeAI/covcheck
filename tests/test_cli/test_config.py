from pathlib import Path
from typing import Any, Dict

import pytest
from pytest import TempPathFactory

from covcheck._cli import config as config_module


@pytest.fixture(name='example_config_filepath', scope='module')
def fixture_example_config_filepath(tmp_path_factory: TempPathFactory) -> Path:
    temp_dirpath = tmp_path_factory.mktemp('configs')
    config_filepath = temp_dirpath / 'pyproject.toml'
    lines = [
        '[tool.covcheck]\n',
        'line = 2.0\n',
        'branch = 3.0\n',
        'silent = true\n',
    ]
    with open(config_filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    return config_filepath


@pytest.fixture(name='example_config_kwargs', scope='module')
def fixture_example_config_kwargs() -> Dict[str, Any]:
    return {
        'line': 4.0,
        'branch': 5.0,
        'silent': True,
    }


class TestConfig:
    def test_create_cli(
        self,
        coverage_filepath: Path,
        example_config_kwargs: Dict[str, Any],
    ) -> None:
        config = config_module.Config.create(
            coverage_filepath,
            config_file=None,
            **example_config_kwargs,
        )
        assert config.line == 4.0
        assert config.branch == 5.0
        assert config.silent

    def test_create_file(
        self,
        example_config_filepath: Path,
        coverage_filepath: Path,
    ) -> None:
        config = config_module.Config.create(
            coverage_filepath,
            config_file=example_config_filepath,
        )
        assert config.line == 2.0
        assert config.branch == 3.0
        assert config.silent

    def test_create_both(
        self,
        example_config_filepath: Path,
        coverage_filepath: Path,
        example_config_kwargs: Dict[str, Any],
    ) -> None:
        config = config_module.Config.create(
            coverage_filepath,
            config_file=example_config_filepath,
            **example_config_kwargs,
        )
        assert config.line == 4.0
        assert config.branch == 5.0
        assert config.silent

    def test_create_no_toml(
        self,
        example_config_filepath: Path,
        coverage_filepath: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(config_module, 'TOML_INSTALLED', False, raising=True)

        message = ("--config was passed, but the toml package was not installed. "
                   "Please 'pip install toml' before running with --config.")
        with pytest.raises(ImportError, match=message):
            config_module.Config.create(
                coverage_filepath,
                config_file=example_config_filepath,
            )

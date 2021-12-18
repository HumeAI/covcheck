"""Configuration for covcheck validation."""

from pathlib import Path
from typing import Any, Optional, Union

try:
    import toml
    TOML_INSTALLED = True
except ImportError:
    TOML_INSTALLED = False


class Config:
    """Configuration for covcheck validation."""
    def __init__(
        self,
        coverage_filepath: Union[str, Path],
        line: Optional[float] = None,
        branch: Optional[float] = None,
        output: Optional[Union[str, Path]] = None,
        silent: bool = False,
    ):
        """Create a covcheck config.

        :param coverage_filepath: XML coverage file from Coverage.py.
        :param line: Threshold for line coverage.
        :param branch: Threshold for branch coverage.
        :param output: Path on disk where a JSON output file should be saved.
        :param silent: Whether the actaual coverage measurements should be printed to stdout.
        """
        self.coverage_filepath = coverage_filepath
        self.line = line
        self.branch = branch
        self.output = output
        self.silent = silent

    @classmethod
    def create(
        cls,
        coverage_file: Union[str, Path],
        config_file: Optional[Union[str, Path]] = None,
        **kwargs: Optional[Any],
    ) -> 'Config':
        """Get a config based on both CLI arguments and config file settings.

        If the same argument is specified in both CLI arguments and config file,
        then the CLI argument will take precedence.

        :param coverage_file: XML coverage file from Coverage.py.
        :param config_file: Path to pyproject.toml config file.
        :param kwargs: Kwargs containing additional config settings.
        """
        config = cls(coverage_file)

        if config_file is not None:
            if not TOML_INSTALLED:
                raise ImportError("--config was passed, but the toml package was not installed. "
                                  "Please 'pip install toml' before running with --config.")

            with open(config_file, 'r', encoding='utf-8') as f:
                toml_config = toml.load(f)

                toml_tools = toml_config['tool']
                if 'covcheck' in toml_tools:
                    toml_covcheck = toml_tools['covcheck']
                    for key, value in toml_covcheck.items():
                        setattr(config, key, value)

        for key, value in kwargs.items():
            if value is not None:
                setattr(config, key, value)

        return config

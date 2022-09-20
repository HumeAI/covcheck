"""Configuration for covcheck validation."""

from pathlib import Path
from typing import Any, Optional, Union

from covcheck._cli.utilities import fail_with_error

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
        coverage_filepath: Union[str, Path],
        config_filepath: Optional[Union[str, Path]] = None,
        group: Optional[str] = None,
        **kwargs: Optional[Any],
    ) -> 'Config':
        """Get a config based on both CLI arguments and config file settings.

        If the same argument is specified in both CLI arguments and config file,
        then the CLI argument will take precedence.

        :param coverage_filepath: Path to XML coverage file from Coverage.py.
        :param config_filepath: Path to pyproject.toml config file.
        :param group: Name of coverage group to check.
        :param kwargs: Kwargs containing additional config settings.
        """
        config = cls(coverage_filepath)

        if config_filepath is not None:
            if not TOML_INSTALLED:
                raise ImportError("--config was passed, but the toml package was not installed. "
                                  "Please 'pip install toml' before running with --config.")

            with open(config_filepath, 'r', encoding='utf-8') as f:
                toml_config = toml.load(f)

                if 'tool' in toml_config:
                    toml_tools = toml_config['tool']
                    if 'covcheck' in toml_tools:
                        toml_covcheck = toml_tools['covcheck']

                        # Check for missing group configuration
                        if group is not None:
                            # Group name selected but no matching group in config file
                            if 'group' in toml_covcheck and group not in toml_covcheck['group']:
                                fail_with_error(f"Group {group} not found in config")
                            # Group name selected but no groups at all in config file
                            if 'group' not in toml_covcheck:
                                fail_with_error(f"Group {group} not found in config")

                        if 'group' in toml_covcheck and group is not None:
                            group_dict = toml_covcheck['group'][group]
                            if 'coverage' in group_dict:
                                for key, value in group_dict['coverage'].items():
                                    setattr(config, key, value)
                        else:
                            for key, value in toml_covcheck.items():
                                setattr(config, key, value)

        for key, value in kwargs.items():
            if value is not None:
                setattr(config, key, value)

        return config

"""General classes used for configuration."""

from typing import NamedTuple


class ConfigError(RuntimeError):
    """ConfigError is used for config related errors."""


class Input(NamedTuple):
    """Input holds all information wrt. data which is consumed."""

    bom_file: str
    bom_type: str
    template_file: str


class Output(NamedTuple):
    """Output holds all information wrt. data which is being produced."""

    markdown_file: str


class Config(NamedTuple):
    """Config represents the entire configuration."""

    source: Input
    target: Output

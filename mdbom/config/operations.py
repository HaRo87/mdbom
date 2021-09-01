"""Operations which handle configuration(s)."""

import errno
import os
from configparser import ConfigParser
from typing import NoReturn

from mdbom.config import types

DEFAULT_CONFIG_FILE_NAME = "mdbom.ini"
CONFIG_INPUT_PORTION_KEY = "INPUT"
CONFIG_OUTPUT_PORTION_KEY = "OUTPUT"
CONFIG_BOM_FILE_KEY = "bom_file"
CONFIG_BOM_TYPE_KEY = "bom_type"
CONFIG_TEMPLATE_FILE_KEY = "template_file"
CONFIG_MARKDOWN_FILE_KEY = "markdown_file"

config_parser = ConfigParser()


def get_config(config_file="") -> types.Config:
    """Get the config based on the provided config_file path.

    Args:
        config_file: The path to the config file.

    Returns:
        The complete and validated config.

    Raises:
        ConfigError: If the config file cannot be read.

    """
    if config_file:
        if os.path.exists(config_file):
            config_parser.read(config_file)
        else:
            raise types.ConfigError("Unable to read provided config")
    else:
        if os.path.exists(DEFAULT_CONFIG_FILE_NAME):
            config_parser.read(DEFAULT_CONFIG_FILE_NAME)
        else:
            raise types.ConfigError("Unable to read default config")

    input_conf = config_parser[CONFIG_INPUT_PORTION_KEY]
    output_conf = config_parser[CONFIG_OUTPUT_PORTION_KEY]

    mdb_config = types.Config(
        types.Input(
            input_conf[CONFIG_BOM_FILE_KEY],
            input_conf[CONFIG_BOM_TYPE_KEY],
            input_conf[CONFIG_TEMPLATE_FILE_KEY],
        ),
        types.Output(
            output_conf[CONFIG_MARKDOWN_FILE_KEY],
        ),
    )

    _validate_config(config=mdb_config)

    return mdb_config


def create_config(
    config: types.Config,
    config_file="",
    force=False,
) -> NoReturn:
    """Create the provided config under the provided config_file path.

    Args:
        config: The actual configuration.
        config_file: The path to the config file.
        force: Whether an existing file shall be overwritten or not.

    Raises:
        ConfigError: If the config file cannot be created.

    """
    _validate_config(config=config)
    if not config_file:
        config_file = DEFAULT_CONFIG_FILE_NAME
    if os.path.exists(config_file):
        if force:
            _write_config(config=config, file_name=config_file)
        else:
            raise types.ConfigError(
                "Config file exists and no force arg provided",
            )
    else:
        _write_config(config=config, file_name=config_file)


def _validate_config(config: types.Config) -> NoReturn:  # type: ignore
    if not config.source.bom_file:
        raise types.ConfigError("Invalid BOM file")
    if not config.source.template_file:
        raise types.ConfigError("Invalid template file")
    if not config.target.markdown_file:
        raise types.ConfigError("Invalid markdown file")


def _write_config(config: types.Config, file_name: str) -> NoReturn:  # type: ignore
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise

    config_parser[CONFIG_INPUT_PORTION_KEY] = {
        CONFIG_BOM_FILE_KEY: config.source.bom_file,
        CONFIG_BOM_TYPE_KEY: config.source.bom_type,
        CONFIG_TEMPLATE_FILE_KEY: config.source.template_file,
    }
    config_parser[CONFIG_OUTPUT_PORTION_KEY] = {
        CONFIG_MARKDOWN_FILE_KEY: config.target.markdown_file,
    }
    with open(file_name, "w") as conf:
        config_parser.write(conf)

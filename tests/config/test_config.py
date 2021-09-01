import unittest
import pathlib
from unittest.mock import patch
import os
from mdbom.config import operations, types
import tempfile
from configparser import ConfigParser


class TestConfig(unittest.TestCase):
    config_dir = pathlib.Path.cwd() / "tests" / "inputs"

    @patch("os.path.exists")
    def test_get_config_fails_due_to_no_default_config(self, path_patch):
        path_patch.return_value = False

        with self.assertRaises(types.ConfigError) as ce:
            operations.get_config()
        self.assertEqual("Unable to read default config", str(ce.exception))

        path_patch.assert_called_once_with(operations.DEFAULT_CONFIG_FILE_NAME)

    @patch("os.path.exists")
    def test_get_config_fails_due_to_no_valid_config(self, path_patch):
        path_patch.return_value = False

        with self.assertRaises(types.ConfigError) as ce:
            operations.get_config(config_file="config.ini")
        self.assertEqual("Unable to read provided config", str(ce.exception))

        path_patch.assert_called_once_with("config.ini")

    def test_get_config_from_provided_file_success(self):
        config_path = self.config_dir / "valid_config.ini"
        conf = operations.get_config(config_file=config_path)
        self.assertEqual("bom-pypi.json", conf.source.bom_file)
        self.assertEqual("pypi", conf.source.bom_type)
        self.assertEqual("template.md.jinja", conf.source.template_file)
        self.assertEqual("3rd-party.md", conf.target.markdown_file)

    def test_validate_config_fails_due_to_no_bom_file(self):
        conf = types.Config(
            types.Input(
                "",
                "pypi",
                "template.md.jinja",
            ),
            types.Output(
                "3rd-party.md",
            ),
        )
        with self.assertRaises(types.ConfigError) as ce:
            operations._validate_config(conf)
        self.assertEqual("Invalid BOM file", str(ce.exception))

    def test_validate_config_fails_due_to_invalid_template_file(self):
        conf = types.Config(
            types.Input(
                "bom-pypi.json",
                "pypi",
                "",
            ),
            types.Output(
                "3rd-party.md",
            ),
        )
        with self.assertRaises(types.ConfigError) as ce:
            operations._validate_config(conf)
        self.assertEqual("Invalid template file", str(ce.exception))

    def test_validate_config_fails_due_to_invalid_markdown_file(self):
        conf = types.Config(
            types.Input(
                "bom-pypi.json",
                "pypi",
                "template.md.jinja",
            ),
            types.Output(
                "",
            ),
        )
        with self.assertRaises(types.ConfigError) as ce:
            operations._validate_config(conf)
        self.assertEqual("Invalid markdown file", str(ce.exception))

    def test_validate_config_success(self):
        conf = types.Config(
            types.Input(
                "bom-pypi.json",
                "pypi",
                "template.md.jinja",
            ),
            types.Output(
                "3rd-party.md",
            ),
        )
        operations._validate_config(conf)

    def test_write_config_into_existing_dir(self):
        config_parser = ConfigParser()
        conf = types.Config(
            types.Input(
                "bom-pypi.json",
                "pypi",
                "template.md.jinja",
            ),
            types.Output(
                "3rd-party.md",
            ),
        )

        with tempfile.TemporaryDirectory() as dir:
            config_path = os.path.join(dir, "config.ini")
            operations._write_config(conf, config_path)
            self.assertTrue(os.path.exists(config_path))
            config_parser.read(config_path)
            input_info = config_parser[operations.CONFIG_INPUT_PORTION_KEY]
            output_info = config_parser[operations.CONFIG_OUTPUT_PORTION_KEY]
            self.assertEqual(
                "bom-pypi.json", input_info[operations.CONFIG_BOM_FILE_KEY]
            )
            self.assertEqual("pypi", input_info[operations.CONFIG_BOM_TYPE_KEY])
            self.assertEqual(
                "template.md.jinja",
                input_info[operations.CONFIG_TEMPLATE_FILE_KEY],
            )
            self.assertEqual(
                "3rd-party.md", output_info[operations.CONFIG_MARKDOWN_FILE_KEY]
            )

    def test_write_config_into_non_existing_dir(self):
        config_parser = ConfigParser()
        conf = types.Config(
            types.Input(
                "bom-pypi.json",
                "pypi",
                "template.md.jinja",
            ),
            types.Output(
                "3rd-party.md",
            ),
        )

        with tempfile.TemporaryDirectory() as dir:
            config_path = os.path.join(dir, ".config", "config.ini")
            operations._write_config(conf, config_path)
            self.assertTrue(os.path.exists(config_path))
            config_parser.read(config_path)
            input_info = config_parser[operations.CONFIG_INPUT_PORTION_KEY]
            output_info = config_parser[operations.CONFIG_OUTPUT_PORTION_KEY]
            self.assertEqual(
                "bom-pypi.json", input_info[operations.CONFIG_BOM_FILE_KEY]
            )
            self.assertEqual("pypi", input_info[operations.CONFIG_BOM_TYPE_KEY])
            self.assertEqual(
                "template.md.jinja",
                input_info[operations.CONFIG_TEMPLATE_FILE_KEY],
            )
            self.assertEqual(
                "3rd-party.md", output_info[operations.CONFIG_MARKDOWN_FILE_KEY]
            )

    @patch("os.path.exists")
    def test_create_config_fails_due_to_file_exists_and_no_force(
        self, path_patch
    ):
        path_patch.return_value = True
        file_path = "test/config.ini"
        conf = types.Config(
            types.Input(
                "bom-pypi.json",
                "pypi",
                "template.md.jinja",
            ),
            types.Output(
                "3rd-party.md",
            ),
        )

        with self.assertRaises(types.ConfigError) as ce:
            operations.create_config(config=conf, config_file=file_path)
        self.assertEqual(
            "Config file exists and no force arg provided", str(ce.exception)
        )

    @patch("os.path.exists")
    @patch("mdbom.config.operations._write_config")
    def test_create_config_at_file_path_success(self, write_patch, path_patch):
        path_patch.return_value = False
        file_path = "test/config.ini"
        conf = types.Config(
            types.Input(
                "bom-pypi.json",
                "pypi",
                "template.md.jinja",
            ),
            types.Output(
                "3rd-party.md",
            ),
        )

        operations.create_config(config=conf, config_file=file_path)

        write_patch.assert_called_once_with(config=conf, file_name=file_path)

    @patch("os.path.exists")
    @patch("mdbom.config.operations._write_config")
    def test_create_config_at_default_file_path_success(
        self, write_patch, path_patch
    ):
        path_patch.return_value = False

        conf = types.Config(
            types.Input(
                "bom-pypi.json",
                "pypi",
                "template.md.jinja",
            ),
            types.Output(
                "3rd-party.md",
            ),
        )

        operations.create_config(config=conf)

        write_patch.assert_called_once_with(
            config=conf, file_name=operations.DEFAULT_CONFIG_FILE_NAME
        )

    @patch("os.path.exists")
    @patch("mdbom.config.operations._write_config")
    def test_create_config_at_file_path_with_force_success(
        self, write_patch, path_patch
    ):
        path_patch.return_value = True
        file_path = "test/config.ini"
        conf = types.Config(
            types.Input(
                "bom-pypi.json",
                "pypi",
                "template.md.jinja",
            ),
            types.Output(
                "3rd-party.md",
            ),
        )

        operations.create_config(config=conf, config_file=file_path, force=True)

        write_patch.assert_called_once_with(config=conf, file_name=file_path)
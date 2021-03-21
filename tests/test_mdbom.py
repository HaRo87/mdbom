import pathlib
from click.testing import CliRunner
from unittest import TestCase
from mdbom.mdbom import cli, generate


class TestCLICommands(TestCase):

    input_dir = pathlib.Path.cwd() / "tests" / "inputs"

    def test_info(self):
        runner = CliRunner()
        result = runner.invoke(cli, "info")
        self.assertEqual(0, result.exit_code)

    def test_generate(self):
        file_name = self.input_dir / "bom.json"
        runner = CliRunner()
        result = runner.invoke(generate, ["--in", f"{file_name}"])
        self.assertIsNotNone(result.output)

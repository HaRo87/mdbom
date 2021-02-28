from click.testing import CliRunner
from unittest import TestCase
from mdbom.mdbom import cli

class TestCLICommands(TestCase):
    def test_info(self):
        runner = CliRunner()
        result = runner.invoke(cli, "info")
        self.assertEqual(0, result.exit_code)
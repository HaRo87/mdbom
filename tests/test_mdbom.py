import os
import pathlib
import tempfile
from click.testing import CliRunner
from unittest import TestCase
from mdbom.mdbom import cli, generate


class TestCLICommands(TestCase):

    input_dir = pathlib.Path.cwd() / "tests" / "inputs"
    examples_dir = pathlib.Path.cwd() / "examples"

    def test_info(self):
        runner = CliRunner()
        result = runner.invoke(cli, "info")
        self.assertEqual(0, result.exit_code)

    # def test_generate(self):
    #     file_name = self.input_dir / "bom.json"
    #     runner = CliRunner()
    #     with tempfile.TemporaryDirectory() as dir:
    #         out_name = os.path.join(dir, "3rdParty.md")
    #         template_name = self.examples_dir / "template.md.jinja"
    #         result = runner.invoke(
    #             generate,
    #             [
    #                 "--in",
    #                 f"{file_name}",
    #                 "--out",
    #                 f"{out_name}",
    #                 "--template",
    #                 f"{template_name}",
    #             ],
    #         )
    #         self.assertTrue(os.path.isfile(file_name))
    #         with open(out_name, "r") as result:
    #             content = result.read()
    #         self.assertIn(
    #             "| Name | Version | License(s) | Type | URL |", content
    #         )
    #         self.assertIn(
    #             "| argcomplete | 1.12.2 | Apache Software License | library | https://pypi.org/project/argcomplete/1.12.2/ |",
    #             content,
    #         )
    #     self.assertIsNotNone(result.output)

import os
import pathlib
import tempfile
from click.testing import CliRunner
from unittest import TestCase
from unittest.mock import patch
from mdbom.bom.processor import ProcessingError
from mdbom.mdbom import cli, generate


class TestCLICommands(TestCase):

    input_dir = pathlib.Path.cwd() / "tests" / "inputs"
    examples_dir = pathlib.Path.cwd() / "examples"

    def test_info(self):
        runner = CliRunner()
        result = runner.invoke(cli, "info")
        self.assertEqual(0, result.exit_code)

    def test_generate_success_default(self):
        file_name = self.input_dir / "bom-pypi.json"
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as dir:
            out_name = os.path.join(dir, "3rdParty.md")
            template_name = self.examples_dir / "template.md.jinja"
            result = runner.invoke(
                generate,
                [
                    f"--input={file_name}",
                    f"--output={out_name}",
                    f"--template={template_name}",
                ],
            )
            self.assertEqual(0, result.exit_code)
            self.assertTrue(os.path.isfile(out_name))
            with open(out_name, "r") as result:
                content = result.read()
            self.assertIn(
                "| Name | Version | License(s) | Type | URL |", content
            )
            self.assertIn(
                "| argcomplete | 1.12.2 | Apache Software License | library | https://pypi.org/project/argcomplete/1.12.2/ |",
                content,
            )

    def test_generate_success_npm(self):
        file_name = self.input_dir / "bom-npm.json"
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as dir:
            out_name = os.path.join(dir, "3rdParty.md")
            template_name = self.examples_dir / "template.md.jinja"
            result = runner.invoke(
                generate,
                [
                    f"--input={file_name}",
                    f"--output={out_name}",
                    f"--template={template_name}",
                    "--type=npm",
                ],
            )
            self.assertEqual(0, result.exit_code)
            self.assertTrue(os.path.isfile(out_name))
            with open(out_name, "r") as result:
                content = result.read()
            self.assertIn(
                "| Name | Version | License(s) | Type | URL |", content
            )
            self.assertIn(
                "| eslint | 7.27.0 | MIT | library | https://www.npmjs.com/package/eslint/v/7.27.0 |",
                content,
            )

    def test_generate_fails_due_to_input_file_not_existing(self):
        file_name = "bom.json"
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as dir:
            out_name = ""
            template_name = ""
            result = runner.invoke(
                generate,
                [
                    f"--input={file_name}",
                    f"--output={out_name}",
                    f"--template={template_name}",
                ],
            )
            self.assertEqual(1, result.exit_code)
            self.assertEqual(
                result.output, "Error: Provided file does not exist\n"
            )

    def test_generate_fails_due_to_empty_output_file(self):
        file_name = self.input_dir / "bom-pypi.json"
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as dir:
            out_name = ""
            template_name = self.examples_dir / "template.md.jinja"
            result = runner.invoke(
                generate,
                [
                    f"--input={file_name}",
                    f"--output={out_name}",
                    f"--template={template_name}",
                ],
            )
            self.assertEqual(1, result.exit_code)
            self.assertEqual(
                result.output, "Error: No valid output file name provided.\n"
            )

    def test_generate_fails_due_to_empty_template_file(self):
        file_name = self.input_dir / "bom-pypi.json"
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as dir:
            out_name = os.path.join(dir, "3rdParty.md")
            template_name = ""
            result = runner.invoke(
                generate,
                [
                    f"--input={file_name}",
                    f"--output={out_name}",
                    f"--template={template_name}",
                ],
            )
            self.assertEqual(1, result.exit_code)
            self.assertEqual(
                result.output, "Error: No valid template provided.\n"
            )

    def test_generate_fails_due_to_processor_type_not_available(self):
        file_name = self.input_dir / "bom-pypi.json"
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as dir:
            out_name = os.path.join(dir, "3rdParty.md")
            template_name = self.examples_dir / "template.md.jinja"
            result = runner.invoke(
                generate,
                [
                    f"--input={file_name}",
                    f"--output={out_name}",
                    f"--template={template_name}",
                    "--type=golang",
                ],
            )
            self.assertEqual(1, result.exit_code)
            self.assertEqual(
                result.output,
                "Error: Invalid processor provided, check --help for available ones\n",
            )

    def test_generate_fails_due_to_pypi_processing__not_working(
        self,
    ):
        file_name = self.input_dir / "bom-pypi.json"

        def construct_urls(self, packages):
            raise ProcessingError("Something went wrong")

        with patch.object(PyPiProcessor, "construct_urls", construct_urls):
            with tempfile.TemporaryDirectory() as dir:
                out_name = os.path.join(dir, "3rdParty.md")
                template_name = self.examples_dir / "template.md.jinja"
                runner = CliRunner()
                result = runner.invoke(
                    generate,
                    [
                        f"--input={file_name}",
                        f"--output={out_name}",
                        f"--template={template_name}",
                        "--type=pypi",
                    ],
                )
                self.assertEqual(1, result.exit_code)
                self.assertEqual(
                    result.output,
                    "Error: Something went wrong\n",
                )
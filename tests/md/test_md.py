import os
import pathlib
import tempfile
from unittest import TestCase
from mdbom.bom.bom import Package
from mdbom.md.md import GeneratingError, generate_markdown


class TestGenerator(TestCase):

    input_dir = pathlib.Path.cwd() / "examples"

    def test_generate_fails_due_to_empty_template(self):
        with self.assertRaises(GeneratingError) as ge:
            generate_markdown(template="", file_name="test.md", packages=[])
        self.assertEqual("No valid template provided.", str(ge.exception))

    def test_generate_fails_due_to_empty_file_name(self):
        with self.assertRaises(GeneratingError) as ge:
            generate_markdown(
                template="test.md.jinja", file_name="", packages=[]
            )
        self.assertEqual(
            "No valid output file name provided.", str(ge.exception)
        )

    def test_generate_success(self):
        template = self.input_dir / "template.md.jinja"
        packages = [
            Package(
                "test",
                "0.1.0",
                "lib",
                "MIT",
                "https://some.url",
            ),
        ]

        with tempfile.TemporaryDirectory() as dir:
            file_name = os.path.join(dir, "3rdParty.md")
            generate_markdown(
                template=template, file_name=file_name, packages=packages
            )
            self.assertTrue(os.path.isfile(file_name))
            with open(file_name, "r") as result:
                content = result.read()
            self.assertIn(
                "| Name | Version | License(s) | Type | URL |", content
            )
            self.assertIn(
                "| test | 0.1.0 | MIT | lib | https://some.url |", content
            )

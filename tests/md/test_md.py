import pathlib
from unittest import TestCase
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

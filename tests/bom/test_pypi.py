import pathlib
from unittest import TestCase
from mdbom.bom.pypi import PyPiProcessor


class TestProcessor(TestCase):

    input_dir = pathlib.Path.cwd() / "tests" / "inputs"

    def test_construct_pypi_urls_success(self):
        proc = PyPiProcessor()
        packages = proc.get_packages_from_bom(
            filename=self.input_dir / "bom-pypi.json"
        )
        packages = proc.construct_urls(packages=packages)
        self.assertEqual("argcomplete", packages[0].name)
        self.assertEqual("Apache Software License", packages[0].licenses)
        self.assertEqual("library", packages[0].kind)
        self.assertEqual("1.12.2", packages[0].version)
        self.assertEqual(
            "https://pypi.org/project/argcomplete/1.12.2/", packages[0].url
        )

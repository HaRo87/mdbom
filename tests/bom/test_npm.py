import pathlib
from unittest import TestCase
from mdbom.bom.npm import NpmProcessor


class TestProcessor(TestCase):

    input_dir = pathlib.Path.cwd() / "tests" / "inputs"

    def test_construct_npm_urls_success(self):
        proc = NpmProcessor()
        packages = proc.get_packages_from_bom(
            filename=self.input_dir / "bom-npm.json"
        )
        packages = proc.construct_urls(packages=packages)
        self.assertEqual("eslint", packages[0].name)
        self.assertEqual("MIT", packages[0].licenses)
        self.assertEqual("library", packages[0].kind)
        self.assertEqual("7.27.0", packages[0].version)
        self.assertEqual(
            "https://www.npmjs.com/package/eslint/v/7.27.0", packages[0].url
        )

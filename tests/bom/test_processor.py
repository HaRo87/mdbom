import pathlib
from unittest import TestCase
from unittest.mock import patch
from mdbom.bom.bom import Package, ProcessingError
from mdbom.bom.processor import (
    _load_bom,
    get_packages_from_bom,
    filter_packages_by_type,
)


class TestProcessor(TestCase):

    input_dir = pathlib.Path.cwd() / "tests" / "inputs"

    def test_get_packages_from_bom_fails_due_to_empty_file_name(self):
        with self.assertRaises(ProcessingError) as pe:
            get_packages_from_bom()
        self.assertEqual("No file provided", str(pe.exception))

    @patch("os.path.exists")
    def test_load_bom_fails_due_to_file_does_not_exist(self, path_patch):
        path_patch.return_value = False
        with self.assertRaises(ProcessingError) as pe:
            _load_bom(filename="bom.json")
        self.assertEqual("Provided file does not exist", str(pe.exception))

    def test_load_bom_success(self):
        packages = _load_bom(filename=self.input_dir / "bom-pypi.json")
        self.assertEqual("argcomplete", packages["components"][0]["name"])

    @patch("mdbom.bom.processor._load_bom")
    def test_get_packages_bom_with_unknown_license(self, load_patch):
        load_patch.return_value = {
            "components": [
                {
                    "name": "Test",
                    "version": "0.1.1",
                    "type": "test",
                    "licenses": [{"license": {"description": "test"}}],
                }
            ]
        }
        packages = get_packages_from_bom(
            filepath=self.input_dir / "bom-pypi.json"
        )
        self.assertEqual("Test", packages[0].name)
        self.assertEqual("unknown", packages[0].licenses)
        self.assertEqual("test", packages[0].kind)
        self.assertEqual("0.1.1", packages[0].version)
        self.assertEqual("", packages[0].url)

    @patch("mdbom.bom.processor._load_bom")
    def test_get_packages_bom_with_unknown_licenses(self, load_patch):
        load_patch.return_value = {
            "components": [
                {
                    "name": "Test",
                    "version": "0.1.1",
                    "type": "test",
                }
            ]
        }
        packages = get_packages_from_bom(
            filepath=self.input_dir / "bom-pypi.json"
        )
        self.assertEqual("Test", packages[0].name)
        self.assertEqual("unknown", packages[0].licenses)
        self.assertEqual("test", packages[0].kind)
        self.assertEqual("0.1.1", packages[0].version)
        self.assertEqual("", packages[0].url)

    def test_get_packages_pypi_bom_success(self):
        packages = get_packages_from_bom(
            filepath=self.input_dir / "bom-pypi.json"
        )
        self.assertEqual("argcomplete", packages[0].name)
        self.assertEqual("Apache Software License", packages[0].licenses)
        self.assertEqual("library", packages[0].kind)
        self.assertEqual("1.12.2", packages[0].version)
        self.assertEqual("pkg:pypi/argcomplete@1.12.2", packages[0].purl)
        self.assertEqual(
            "https://pypi.org/project/argcomplete/1.12.2", packages[0].url
        )
        self.assertEqual("certifi", packages[1].name)
        self.assertEqual("click", packages[2].name)

    def test_get_packages_npm_bom_success(self):
        packages = get_packages_from_bom(
            filepath=self.input_dir / "bom-npm.json"
        )
        self.assertEqual("eslint", packages[0].name)
        self.assertEqual("MIT", packages[0].licenses)
        self.assertEqual("library", packages[0].kind)
        self.assertEqual("7.27.0", packages[0].version)
        self.assertEqual("pkg:npm/eslint@7.27.0", packages[0].purl)
        self.assertEqual(
            "https://www.npmjs.com/package/eslint/v/7.27.0", packages[0].url
        )

    def test_get_packages_golang_bom_success(self):
        packages = get_packages_from_bom(
            filepath=self.input_dir / "bom-golang.json"
        )
        self.assertEqual("cloud.google.com/go", packages[0].name)
        self.assertEqual("library", packages[0].kind)
        self.assertEqual("v0.93.3", packages[0].version)
        self.assertEqual(
            "pkg:golang/cloud.google.com/go@v0.93.3?type=module",
            packages[0].purl,
        )
        self.assertEqual(
            "https://pkg.go.dev/cloud.google.com/go@v0.93.3", packages[0].url
        )
        self.assertEqual("cloud.google.com/go/container", packages[1].name)

    def test_get_packages_multiple_boms_success(self):
        packages = get_packages_from_bom(filepath=self.input_dir)
        self.assertEqual(6, len(packages))
        self.assertEqual("cloud.google.com/go", packages[0].name)
        self.assertEqual("cloud.google.com/go/container", packages[1].name)
        self.assertEqual("eslint", packages[2].name)
        self.assertEqual("MIT", packages[2].licenses)
        self.assertEqual("library", packages[2].kind)
        self.assertEqual("7.27.0", packages[2].version)
        self.assertEqual("pkg:npm/eslint@7.27.0", packages[2].purl)
        self.assertEqual(
            "https://www.npmjs.com/package/eslint/v/7.27.0", packages[2].url
        )
        self.assertEqual("argcomplete", packages[3].name)
        self.assertEqual("Apache Software License", packages[3].licenses)
        self.assertEqual("library", packages[3].kind)
        self.assertEqual("1.12.2", packages[3].version)
        self.assertEqual("pkg:pypi/argcomplete@1.12.2", packages[3].purl)
        self.assertEqual(
            "https://pypi.org/project/argcomplete/1.12.2", packages[3].url
        )
        self.assertEqual("certifi", packages[4].name)
        self.assertEqual("click", packages[5].name)

    def test_filter_packages_by_type_no_type_returns_all(self):
        packages = packages = [
            Package(
                "test",
                "0.1.0",
                "lib",
                "MIT",
                "pkg:pypi/some-package_1.2.3",
                "https://some.url",
            ),
            Package(
                "test2",
                "0.1.1",
                "lib",
                "MIT",
                "pkg:npm/some-package_1.2.3",
                "https://some2.url",
            ),
        ]
        filtered_packages = filter_packages_by_type(
            packages=packages, package_type=""
        )
        self.assertEqual(packages, filtered_packages)

    def test_filter_packages_by_type_type_returns_filtered_list(self):
        packages = packages = [
            Package(
                "test",
                "0.1.0",
                "lib",
                "MIT",
                "pkg:pypi/some-package_1.2.3",
                "https://some.url",
            ),
            Package(
                "test2",
                "0.1.1",
                "lib",
                "MIT",
                "pkg:npm/some-package_1.2.3",
                "https://some2.url",
            ),
        ]
        filtered_packages = filter_packages_by_type(
            packages=packages, package_type="npm"
        )
        self.assertNotEqual(packages, filtered_packages)
        self.assertTrue(len(filtered_packages) == 1)
        self.assertEqual(
            "pkg:npm/some-package_1.2.3", filtered_packages[0].purl
        )

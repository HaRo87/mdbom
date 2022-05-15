from testfixtures import LogCapture
from unittest import TestCase
from mdbom.bom.urls import _get_package_and_version, get_url


class TestURLs(TestCase):

    invalid_purl = ""
    invalid_purl_rest = "pkg:pypi/some-package_1.2.3"
    valid_pypi_purl = "pkg:pypi/django@1.11.1"
    valid_npm_purl = "pkg:npm/foobar@12.3.1"

    def test_get_package_and_version_empty_return_due_to_invalid_purl(self):
        package, version = _get_package_and_version(self.invalid_purl_rest)
        self.assertEqual("", package)
        self.assertEqual("", version)

    def test_get_package_and_version_only_package_due_to_invalid_purl(self):
        package, version = _get_package_and_version("pkg:pypi/some-package@")
        self.assertEqual("some-package", package)
        self.assertEqual("", version)

    def test_get_package_and_version_only_package_due_to_invalid_purl(self):
        package, version = _get_package_and_version("pkg:pypi/@1.2.3")
        self.assertEqual("", package)
        self.assertEqual("1.2.3", version)

    def test_get_url_fails_due_to_invalid_purl(self):
        with LogCapture() as log:
            res = get_url(self.invalid_purl)
            self.assertEqual("", res)
            log.check(
                (
                    "MdBOM",
                    "WARNING",
                    "No valid purl provided, returning empty URL",
                )
            )

    def test_get_url_for_pypi_success(self):
        res = get_url(self.valid_pypi_purl)
        self.assertEqual("https://pypi.org/project/django/1.11.1", res)

    def test_get_url_for_npm_success(self):
        res = get_url(self.valid_npm_purl)
        self.assertEqual("https://www.npmjs.com/package/foobar/v/12.3.1", res)

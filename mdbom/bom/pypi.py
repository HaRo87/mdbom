"""A processor who takes care of handling PyPi packages."""

from typing import List

from mdbom.bom.bom import Package
from mdbom.bom.processor import Processor


class PyPiProcessor(Processor):
    """PyPiProcessor takes care of processing PyPi related packages."""

    def __init__(self):
        """Construct a new PyPiProcessor."""
        super().__init__(processor_name="PyPiProcessor")

    def construct_urls(self, packages: List[Package]) -> List[Package]:
        """Adds the correct URLs to the package list.

        Args:
            packages: The packages where the URLs need to be added.

        Returns:
            A list of packages with URLs.
        """
        new_packages = []
        for package in packages:
            new_packages.append(
                Package(
                    package.name,
                    package.version,
                    package.kind,
                    package.licenses,
                    "https://pypi.org/project/"
                    + package.name
                    + "/"
                    + package.version
                    + "/",
                ),
            )
        return new_packages

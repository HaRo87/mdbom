"""A processor who takes care of handling npm packages."""

from typing import List

from mdbom.bom.bom import Package
from mdbom.bom.processor import Processor


class NpmProcessor(Processor):
    """NpmProcessor takes care of processing npm related packages."""

    def __init__(self):
        """Construct a new NpmProcessor."""
        super().__init__(processor_name="NpmProcessor")

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
                    "https://www.npmjs.com/package/"
                    + package.name
                    + "/v/"
                    + package.version,
                ),
            )
        return new_packages

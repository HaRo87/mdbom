"""Abstract class for handling BOM processing."""

import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from mdbom.bom.bom import Package, ProcessingError


class Processor(ABC):
    """A processor for handling bill of materials."""

    logger = logging.getLogger("MdBOM")

    def __init__(self, processor_name=""):
        """Construct a new processor.

        Args:
            processor_name: The name of the processor.

        Raises:
            ProcessingError: If no name is provided.
        """
        super()

        if processor_name:
            self.processor_name = processor_name
        else:
            raise ProcessingError("No processor name defined")

    def get_packages_from_bom(self, filename: str = "") -> List[Package]:
        """Get a list of packages from the BOM.

        Args:
            filename: The path to the BOM file.

        Returns:
            A list of packages.
        """
        content = self._load_bom(filename=filename)
        packages = []
        for component in content["components"]:
            licenses = []
            for component_license in component["licenses"]:
                licenses.append(component_license["license"]["name"])
            packages.append(
                Package(
                    component["name"],
                    component["version"],
                    component["type"],
                    ",".join(licenses),
                    " ",
                ),
            )
        return packages

    @abstractmethod
    def construct_urls(self, packages: List[Package]) -> List[Package]:
        """Construct the correct package urls.

        Args:
            packages: The list of packages to use.
        """
        pass

    def _load_bom(self, filename: str = "") -> Dict[Any, Any]:
        if filename:
            if os.path.exists(filename):
                with open(filename, "r") as read_file:
                    return json.load(read_file)
            else:
                raise ProcessingError("Provided file does not exist")
        else:
            raise ProcessingError("No file provided")

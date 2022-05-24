"""Handling BOM processing."""

import json
import os
from typing import Any, Dict, List

from mdbom.bom.bom import Package, ProcessingError
from mdbom.bom.urls import get_purl_type, get_url

COMPONENTS_ID = "components"
LICENSE_ID = "license"
LICENSES_ID = "licenses"
NAME_ID = "name"
ID_ID = "id"
TYPE_ID = "type"
VERSION_ID = "version"
PURL_ID = "purl"


def get_packages_from_bom(filename: str = "") -> List[Package]:
    """Get a list of packages from the BOM.

    Args:
        filename: The path to the BOM file.

    Returns:
        A list of packages.
    """
    content = _load_bom(filename=filename)
    packages = []
    for component in content[COMPONENTS_ID]:
        packages.append(
            Package(
                component[NAME_ID],
                component[VERSION_ID],
                component[TYPE_ID],
                ",".join(_extract_licenses(component)),
                _extract_purl(component),
                get_url(_extract_purl(component)),
            ),
        )
    return packages


def filter_packages_by_type(
    packages: List[Package],
    package_type: str,
) -> List[Package]:
    """Filter a list of packages based on type.

    Args:
        packages:       The list of packages to filter.
        package_type:   The packages type to apply as filter.

    Returns:
        A filtered list of packages.
    """
    if not package_type:
        return packages
    return list(
        filter(
            lambda package: get_purl_type(package.purl) == package_type,
            packages,
        ),
    )


def _load_bom(filename: str = "") -> Dict[Any, Any]:
    if filename:
        if os.path.exists(filename):
            with open(filename, "r") as read_file:
                return json.load(read_file)
        else:
            raise ProcessingError("Provided file does not exist")
    else:
        raise ProcessingError("No file provided")


def _extract_licenses(component: Dict[Any, Any]) -> List[str]:
    licenses = []
    if component.get(LICENSES_ID) is not None:
        for component_license in component[LICENSES_ID]:
            if component_license[LICENSE_ID].get(ID_ID) is not None:
                licenses.append(component_license[LICENSE_ID][ID_ID])
            elif component_license[LICENSE_ID].get(NAME_ID) is not None:
                licenses.append(component_license[LICENSE_ID][NAME_ID])
            else:
                licenses.append("unknown")
    else:
        licenses.append("unknown")
    return licenses


def _extract_purl(component: Dict[Any, Any]) -> str:
    purl = ""
    if component.get(PURL_ID) is not None:
        purl = component[PURL_ID]
    return purl

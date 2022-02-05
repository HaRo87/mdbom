"""Handling URL construction."""

import logging
import re
from typing import Callable, Tuple

TYPE_GROUP_ID = "type"
REST_GROUP_ID = "rest"
GOLANG_TYPE = "golang"
GITHUB_TYPE = "github"
NPM_TYPE = "npm"
NUGET_TYPE = "nuget"

logger = logging.getLogger("MdBOM")

purl_reg = re.compile(r"pkg:(?P<type>[a-z]+)\/(?P<rest>\S*)")

def get_url_builder(purl: str) -> Callable[[str], str]:
    types = {
        "pypi": _pypi_url_builder,
        "npm": _npm_url_builder,
    }
    match = purl_reg.match(purl)
    if match:
        if match.group(TYPE_GROUP_ID) not in types:
            logger.warning("Package type not supported, returning empty URL")
            return _empty_url_builder
        else:
            return types[match.group(TYPE_GROUP_ID)]
    else:
        logger.warning("No valid purl provided, returning empty URL")
        return _empty_url_builder
    

def _empty_url_builder(purl: str) -> str:
    return ""

def _pypi_url_builder(purl: str) -> str:
    url = ""
    package, version = _get_package_and_version(purl)
    if package and version:
        url = "https://pypi.org/project/" + package + "/" + version
    else:
        logger.warning("No valid pypi purl provided, returning empty URL")
    return url

def _npm_url_builder(purl: str) -> str:
    url = ""
    package, version = _get_package_and_version(purl)
    if package and version:
        url = "https://www.npmjs.com/package/" + package + "/" + version
    else:
        logger.warning("No valid npm purl provided, returning empty URL")
    return url

def _get_package_and_version(purl: str) -> Tuple[str, str]:
    package, version = "", ""
    match = purl_reg.match(purl)
    if match:
        result = match.group(REST_GROUP_ID).split("@")
        if len(result) == 2:
            package = result[0]
            version = result[1]
    return package, version

    

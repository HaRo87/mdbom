"""Handling URL construction."""

import logging
import re
from typing import Tuple

TYPE_GROUP_ID = "type"
REST_GROUP_ID = "rest"
NPM_TYPE = "npm"

logger = logging.getLogger("MdBOM")

purl_reg = re.compile(r"pkg:(?P<type>[a-z]+)\/(?P<rest>\S*)")

url_types = {
    "pypi": "https://pypi.org/project/",
    "npm": "https://www.npmjs.com/package/",
}


def get_url(purl: str) -> str:
    """Contruct the package URL from provided purl.

    Args:
        purl: The purl of the package.

    Returns:
        A URL to the package.
    """
    match = purl_reg.match(purl)
    if match:
        if match.group(TYPE_GROUP_ID) not in url_types:
            logger.warning("Package type not supported, returning empty URL")
            return ""
        return _convert_purl_to_url(
            purl=purl,
            purl_type=match.group(TYPE_GROUP_ID),
        )
    logger.warning("No valid purl provided, returning empty URL")
    return ""


def _get_package_and_version(purl: str) -> Tuple[str, str]:
    package, version = "", ""
    match = purl_reg.match(purl)
    if match:
        result = match.group(REST_GROUP_ID).split("@")
        if len(result) == 2:
            package = result[0]
            version = result[1]
    return package, version


def _convert_purl_to_url(purl, purl_type: str) -> str:
    url = url_types[purl_type]
    package, version = _get_package_and_version(purl)
    if package and version:
        if purl_type == NPM_TYPE:
            url += "{0}/v/{1}".format(package, version)
        else:
            url += "{0}/{1}".format(package, version)
    else:
        logger.warning(
            f"No valid {purl_type} purl provided, returning empty URL",
        )
        url = ""
    return url

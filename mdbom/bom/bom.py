"""General stuff for handling BOM files."""

from typing import NamedTuple


class ProcessingError(RuntimeError):
    """Processing error for raising processing specific errors."""


class Package(NamedTuple):
    """A representation of a package."""

    name: str
    version: str
    kind: str
    licenses: str
    url: str

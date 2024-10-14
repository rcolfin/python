from __future__ import annotations

import importlib.metadata

from github import commands
from github.client import GitHub

# set the version number within the package using importlib
try:
    __version__: str | None = importlib.metadata.version("pygithub")
except importlib.metadata.PackageNotFoundError:
    # package is not installed
    __version__ = None

__all__ = ["GitHub", "__version__", "commands", "providers"]

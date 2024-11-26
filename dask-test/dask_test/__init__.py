from __future__ import annotations

import importlib.metadata

# set the version number within the package using importlib
try:
    __version__: str | None = importlib.metadata.version("dask-test")
except importlib.metadata.PackageNotFoundError:
    # package is not installed
    __version__ = None


__all__ = ["__version__"]

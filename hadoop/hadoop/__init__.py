from __future__ import annotations

import importlib.metadata

from . import social_media_connect, word_count

# set the version number within the package using importlib
try:
    __version__: str | None = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    # package is not installed
    __version__ = None


__all__ = ["__version__", "social_media_connect", "word_count"]

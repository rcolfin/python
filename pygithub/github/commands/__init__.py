from github.commands import git
from github.commands.common import cli

__all__ = ["cli"]

del git  # only need git to be initialized.

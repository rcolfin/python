import os
import socket

from docker_health_check import constants


def set_env_defaults() -> None:
    """Sets defaults for environment variables that should otherwise be set."""
    if "HOSTNAME" not in os.environ:
        os.environ["HOSTNAME"] = socket.gethostname().split(".")[0]


def replace_newlines(text: str) -> str:
    return text.replace("\n", "\\n")


def truncate(text: str) -> str:
    """Truncates the text and inserts a ... if the text is over MAX_COL_LENGTH"""
    if len(text) > constants.MAX_COL_LENGTH:
        text = text[: constants.MAX_COL_LENGTH] + "..."

    return text

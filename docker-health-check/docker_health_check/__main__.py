from __future__ import annotations

import logging
from typing import Final

from docker_health_check import utils
from docker_health_check.commands import cli

logger = logging.getLogger(__name__)
MAX_COL_LENGTH: Final[int] = 19


def main() -> None:
    utils.set_env_defaults()

    cli(_anyio_backend="asyncio")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-4s\t%(message)s",
    )

    main()

from __future__ import annotations

import logging

from docker_health_check import utils
from docker_health_check.commands import cli

logger = logging.getLogger(__name__)


def main() -> None:
    utils.set_env_defaults()

    cli(_anyio_backend="asyncio")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-4s\t%(message)s",
    )

    main()

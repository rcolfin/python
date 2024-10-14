from __future__ import annotations

import logging
import traceback
from collections.abc import Iterable, Sequence
from datetime import timedelta
from typing import Any

import anyio
import backoff
import requests
from tabulate import tabulate

from docker.client import DockerClient
from docker_health_check import constants, utils
from docker_health_check.models import ContainerRow
from docker_health_check.notifications import NotificationHub

logger = logging.getLogger(__name__)


async def _restart(state: tuple[ContainerRow, NotificationHub]) -> None:
    row, notification_hub = state
    try:
        logger.info("Restarting %s", row.name)
        row.restart()
        logger.info("Restarted %s", row.name)
        notification_hub.enqueue(f"{row.name} container was restarted.")
    except Exception as e:
        message = f"{row.name} container failed to be restarted.  {e}"
        logger.exception(message)
        notification_hub.enqueue(message)


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=constants.MAX_RETRY)
def _get_containers(client: DockerClient, filters: dict[str, Any] | None) -> Iterable[ContainerRow]:
    containers = client.containers.list(filters=filters)
    return map(ContainerRow.from_container, containers)


async def health_check(interval: float, labels: Sequence[str], restart: bool) -> None:
    filters: dict[str, Any] | None = None
    if labels:
        labels = sorted(labels)
        filters = {"label": labels}

    logger.info("Health Check is running")
    if filters:
        logger.info("Filtering by %s", filters)

    if restart:
        logger.info("Containers that are unhealthy will be restarted.")

    client = DockerClient.from_env()
    with NotificationHub() as notification_hub:
        with notification_hub.notify_onexit():
            notification_hub.enqueue("Process is running")

        while True:
            with notification_hub.notify_onexit():
                try:
                    async with anyio.create_task_group() as tg:
                        table: list[tuple[str, str, str, str, timedelta, str]] = []
                        rows = _get_containers(client, filters)
                        for row in rows:
                            table.append(
                                (row.container_id, row.name, row.image, utils.truncate(utils.replace_newlines(row.command)), row.uptime, row.status)
                            )

                            if not row.is_restart_eligible:
                                continue

                            # Container is unhealthy:
                            if restart:
                                logger.info("Scheduling restart of %s", row.name)
                                tg.start_soon(_restart, (row, notification_hub))
                            else:
                                notification_hub.enqueue(f"{row.name} container is not healthy.")

                        logger.info(
                            "Status\n%s",
                            tabulate(
                                table,
                                headers=["CONTAINER ID", "NAME", "IMAGE", "COMMAND", "UPTIME", "STATUS"],
                            ),
                        )
                except Exception:
                    logger.exception("An error occurred while processing containers.")
                    notification_hub.enqueue(f"An error occurred while processing containers.\n${traceback.format_exc()}")

            logger.info("sleeping for %.0fs.", interval)
            await anyio.sleep(interval)

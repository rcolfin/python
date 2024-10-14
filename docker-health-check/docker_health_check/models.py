from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Final, NamedTuple

from docker_health_check.enums import ContainerStatus, HealthCheck

if TYPE_CHECKING:
    from collections.abc import Iterable

    from docker.models.containers import Container

logger = logging.getLogger(__name__)

_CONFIG_CMD_KEYS: Final[tuple[str, str]] = ("Entrypoint", "Cmd")


class ContainerRow(NamedTuple):
    container: Container
    container_id: str
    name: str
    image: str
    command: str
    created: datetime
    status: str
    health: str

    @property
    def is_restart_eligible(self) -> bool:
        return self.status == ContainerStatus.RUNNING and self.health == HealthCheck.HEALTHY

    @property
    def uptime(self) -> timedelta:
        delta = datetime.now(tz=UTC) - self.created
        delta -= timedelta(microseconds=delta.microseconds)
        return delta

    def restart(self) -> None:
        logger.info("Restarting %s", self.name)
        try:
            self.container.restart()
        except Exception:
            logger.exception("Failed to restart %s", self.name)
            raise

    @staticmethod
    def from_container(container: Container) -> ContainerRow:
        attrs = container.attrs
        config = attrs.get("Config", {})
        image = config.get("Image", container.image.short_id)
        command = " ".join(ContainerRow._get_cmd(config))
        created = datetime.fromisoformat(attrs["Created"])

        health = container.health
        status = container.status
        if container.health and container.health != HealthCheck.UNKNOWN:
            status += f" ({container.health})"

        return ContainerRow(container, container.short_id, container.name, image, command, created, status, health)

    @staticmethod
    def _get_cmd(config: dict[str, list[str] | None]) -> Iterable[str]:
        for key in _CONFIG_CMD_KEYS:
            c = config.get(key)
            if c:
                yield from c

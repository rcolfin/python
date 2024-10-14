from __future__ import annotations

import logging

import asyncclick as click

from docker_health_check import api
from docker_health_check.commands.common import cli

logger = logging.getLogger(__name__)


@cli.command("health-check")
@click.option("-i", "--interval", type=float, default=30, help="The interval to inspect running containers")
@click.option("-l", "--label", "labels", type=str, multiple=True, help="container label or labels to filter")
@click.option("-r/-nr", "--restart/--no-restart", is_flag=True, type=bool, default=True, help="toggle to enable auto-restart (default is True)")
async def health_check(interval: float, labels: tuple[str, ...], restart: bool) -> None:
    await api.healthcheck.health_check(interval, labels, restart)

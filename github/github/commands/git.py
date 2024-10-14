from __future__ import annotations

import logging
from pathlib import Path

import asyncclick as click

import github
from github.commands.common import cli

logger = logging.getLogger(__name__)


@cli.command("create-jwt")
@click.argument("client-id", type=str)
@click.argument("signing-key", type=click.Path(exists=True, dir_okay=False))
async def create_jwt(client_id: str, signing_key: str) -> None:
    async with github.providers.Application(
        client_id=client_id, signing_key=Path(signing_key).read_bytes()
    ) as provider:
        print(provider.generate_jwt())  # noqa: T201


@cli.command("get-app")
@click.argument("client-id", type=str)
@click.argument("signing-key", type=click.Path(exists=True, dir_okay=False))
async def get_app(client_id: str, signing_key: str) -> None:
    async with github.providers.Application(
        client_id=client_id, signing_key=Path(signing_key).read_bytes()
    ) as provider:
        print(await provider.get_app())  # noqa: T201


@cli.command("get-app-installations")
@click.argument("client-id", type=str)
@click.argument("signing-key", type=click.Path(exists=True, dir_okay=False))
async def get_app_install_id(
    client_id: str,
    signing_key: str,
) -> None:
    async with github.providers.Application(
        client_id=client_id, signing_key=Path(signing_key).read_bytes()
    ) as provider:
        async for app_inst in provider.get_app_installations():
            print(app_inst)  # noqa: T201


@cli.command("get-access-token")
@click.argument("client-id", type=str)
@click.argument("signing-key", type=click.Path(exists=True, dir_okay=False))
@click.argument("installation-id", type=str)
async def get_access_token(client_id: str, signing_key: str, installation_id: str) -> None:
    async with github.providers.Application(client_id, Path(signing_key).read_bytes(), installation_id) as provider:
        print(await provider.access_token())  # noqa: T201


@cli.command("delete-workflow-runs")
@click.argument("owner", type=str)
@click.argument("repo", type=str)
@click.argument("access-token", type=str)
async def delete_workflow_runs(owner: str, repo: str, access_token: str) -> None:
    provider = github.providers.Token(access_token)
    async with github.GitHub(provider) as client:
        await client.delete_workflow_runs(owner, repo)


@cli.command("list-workflow-runs")
@click.argument("owner", type=str)
@click.argument("repo", type=str)
@click.argument("access-token", type=str)
async def list_workflow_runs(owner: str, repo: str, access_token: str) -> None:
    provider = github.providers.Token(access_token)
    async with github.GitHub(provider) as client:
        await client.list_workflow_runs(owner, repo)

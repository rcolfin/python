import logging
from pathlib import Path

import click

import github
import github.providers

logger = logging.getLogger(__name__)


@click.group()
def cli() -> None:
    pass


@cli.command("create-jwt")
@click.argument("client-id", type=str)
@click.argument("signing-key", type=click.Path(exists=True, dir_okay=False))
def create_jwt(client_id: str, signing_key: str) -> None:
    provider = github.providers.Application(client_id=client_id, signing_key=Path(signing_key).read_bytes())
    print(provider.generate_jwt())  # noqa: T201


@cli.command("get-app")
@click.argument("client-id", type=str)
@click.argument("signing-key", type=click.Path(exists=True, dir_okay=False))
def get_app(client_id: str, signing_key: str) -> None:
    provider = github.providers.Application(client_id=client_id, signing_key=Path(signing_key).read_bytes())
    print(provider.get_app())  # noqa: T201


@cli.command("get-app-installations")
@click.argument("client-id", type=str)
@click.argument("signing-key", type=click.Path(exists=True, dir_okay=False))
def get_app_install_id(
    client_id: str,
    signing_key: str,
) -> None:
    provider = github.providers.Application(client_id=client_id, signing_key=Path(signing_key).read_bytes())
    print(provider.get_app_installations())  # noqa: T201


@cli.command("get-access-token")
@click.argument("client-id", type=str)
@click.argument("signing-key", type=click.Path(exists=True, dir_okay=False))
@click.argument("installation-id", type=str)
def get_access_token(client_id: str, signing_key: str, installation_id: str) -> None:
    provider = github.providers.Application(client_id, Path(signing_key).read_bytes(), installation_id)
    print(provider.access_token())  # noqa: T201


@cli.command("delete-workflow-runs")
@click.argument("owner", type=str)
@click.argument("repo", type=str)
@click.argument("access-token", type=str)
def delete_workflow_runs(owner: str, repo: str, access_token: str) -> None:
    provider = github.providers.Token(access_token)
    client = github.GitHub(provider)
    client.delete_workflow_runs(owner, repo)


@cli.command("list-workflow-runs")
@click.argument("owner", type=str)
@click.argument("repo", type=str)
@click.argument("access-token", type=str)
def list_workflow_runs(owner: str, repo: str, access_token: str) -> None:
    provider = github.providers.Token(access_token)
    client = github.GitHub(provider)
    client.list_workflow_runs(owner, repo)


def main() -> None:
    cli()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)-12s: %(levelname)-8s\t%(message)s",
    )
    cli()

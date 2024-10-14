import logging

import click

from dask_test import factory, models, tasks


@click.command
@click.option(
    "-c",
    "--client-type",
    type=click.Choice([x.name for x in models.ClientType], case_sensitive=False),
)
def test(client_type: str) -> None:
    client = factory.create_client(models.ClientType[client_type])
    logging.info("client type is %s", client)
    messages = [f"This is message {x}" for x in range(10)]
    futures = client.map(tasks.echo, messages)
    results = client.gather(futures)
    logging.info(results)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)-12s: %(levelname)-8s\t%(message)s",
    )
    test()

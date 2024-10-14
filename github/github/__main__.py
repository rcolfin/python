import logging

from github.commands import cli

logger = logging.getLogger(__name__)


def main() -> None:
    cli()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)-12s: %(levelname)-8s\t%(message)s",
    )
    cli()

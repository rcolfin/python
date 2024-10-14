#!/usr/bin/env python
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable


def main(lines: Iterable[str]) -> None:
    for line in lines:
        print(line)  # noqa: T201


if __name__ == "__main__":
    main(sys.stdin)

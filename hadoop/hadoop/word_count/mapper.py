#!/usr/bin/env python
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable


def mapper(lines: Iterable[str]) -> Iterable[tuple[str, int]]:
    for line in lines:
        sline = line.strip()
        if not sline:
            continue
        # split the line into words
        words = sline.split()
        yield from ((word, 1) for word in words)


def main(lines: Iterable[str]) -> None:
    for word, count in mapper(lines):
        print(f"{word}\t{count}")  # noqa: T201


if __name__ == "__main__":
    main(sys.stdin)

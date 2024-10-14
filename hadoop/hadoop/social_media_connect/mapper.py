#!/usr/bin/env python
import itertools
import sys
from collections import defaultdict
from collections.abc import Iterable
from typing import cast


def mapper(lines: Iterable[str]) -> Iterable[tuple[str, str]]:
    """Produces a list of tuples for possible connections."""
    mapping: dict[str, list[str]] = defaultdict(list)
    for line in lines:
        sline = line.strip()
        if not sline:
            continue
        user, friends = sline.split("\t", maxsplit=2)
        mapping[user].extend(friends.split(","))

    distinct = set()
    for frdlst in mapping.values():
        for users in itertools.combinations(frdlst, 2):
            t = sorted(users)
            v1 = cast(tuple[str, str], (t[0], t[1]))
            if v1 in distinct:
                continue

            distinct.add(v1)
            v2 = cast(tuple[str, str], (t[1], t[0]))
            yield v1
            yield v2


def main(lines: Iterable[str]) -> None:
    for user1, user2 in mapper(lines):
        print(f"{user1}\t{user2}")  # noqa: T201


if __name__ == "__main__":
    main(sys.stdin)

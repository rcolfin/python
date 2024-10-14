#!/usr/bin/env python
import itertools
import sys
from collections import defaultdict
from collections.abc import Iterable
from typing import Final, cast

EXPECTED_VALUES_PER_LINE: Final[int] = 2


def _sort_tuple(t: tuple[str, str]) -> tuple[str, str]:
    """
    Sorts the tuple ensuring that the first element is smaller than the first.

    This is to avoid the intermediate list being created when doing a tuple(sorted(t))
    """
    if t[0] < t[1]:
        return t
    return t[::-1]


def mapper(lines: Iterable[str]) -> Iterable[tuple[str, str]]:
    """Produces a list of tuples for possible connections."""
    mapping: dict[str, list[str]] = defaultdict(list)
    distinct: set[tuple[str, str]] = set()
    for line in lines:
        sline = line.strip()
        if not sline:
            continue

        user_friends = sline.split("\t", maxsplit=2)
        if len(user_friends) < EXPECTED_VALUES_PER_LINE:
            continue  # if a user has no friends.

        user, friends = user_friends[0], user_friends[1].split(",")

        # Ignore users who are already connected
        distinct.update(_sort_tuple((user, friend)) for friend in friends)
        mapping[user].extend(friends)

    for frdlst in mapping.values():
        for users in itertools.combinations(frdlst, 2):
            t = _sort_tuple(users)
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

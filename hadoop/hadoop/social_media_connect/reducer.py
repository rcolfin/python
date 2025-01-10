#!/usr/bin/env python
import sys
from collections import defaultdict
from collections.abc import Iterable


def reducer(lines: Iterable[str]) -> Iterable[tuple[str, tuple[str, ...]]]:
    """Produces for each user a tuple containing possible connections."""
    suggestions: dict[str, set[str]] = defaultdict(set)

    for line in lines:
        sline = line.strip()
        if not sline:
            continue

        # Potential friend pair:
        user, suggestion = sline.split("\t", 2)
        suggestions[user].add(suggestion)

    # Sort results by number of suggested friends:
    suggestions_by_user_lst = [(user, tuple(sorted(friends))) for user, friends in suggestions.items()]
    suggestions_by_user_lst.sort(key=lambda item: (-len(item[1]), item[0]))
    yield from suggestions_by_user_lst


def main(lines: Iterable[str]) -> None:
    for user, suggestions in reducer(lines):
        print(f"{user}\t{','.join(suggestions)}")  # noqa: T201


if __name__ == "__main__":
    main(sys.stdin)

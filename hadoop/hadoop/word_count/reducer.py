#!/usr/bin/env python
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable


def reducer(lines: Iterable[str]) -> Iterable[tuple[str, int]]:
    current_word = None
    current_count = 0
    word = None

    for line in lines:
        sline = line.strip()
        if not sline:
            continue
        # remove leading and trailing whitespace
        # parse the input we got from mapper.py
        word, count = sline.split("\t", 1)

        # convert count (currently a string) to int
        try:
            icount = int(count)
        except ValueError:
            # count was not a number, so silently
            # ignore/discard this line
            continue

        # this IF-switch only works because Hadoop sorts map output
        # by key (here: word) before it is passed to the reducerr
        if current_word == word:
            current_count += icount
        else:
            if current_word:
                # write result to STDOUT
                yield current_word, current_count
            current_count = icount
            current_word = word

    # do not forget to output the last word if needed!
    if current_word and current_word == word:
        yield current_word, current_count


def main(lines: Iterable[str]) -> None:
    for word, count in reducer(lines):
        print(f"{word}\t{count}")  # noqa: T201


if __name__ == "__main__":
    main(sys.stdin)

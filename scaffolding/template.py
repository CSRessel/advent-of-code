import functools
import itertools
import json
import math
import re
import sys
from functools import lru_cache, reduce

from collections import namedtuple, deque, defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Iterable, List, Optional, Literal


def find_idx_ele[T](iterable: Iterable[T], predicate: Callable[[T], bool]) -> Optional[tuple[int, T]]:
    def predicate_tuple(tup: tuple[int, T]) -> bool:
        _, element = tup
        return predicate(element)

    idxele: Optional[tuple[int, T]] = next(filter(predicate_tuple, enumerate(iterable)), None)
    return idxele


def find_idx[T](iterable: Iterable[T], predicate: Callable[[T], bool]) -> Optional[int]:
    result = find_idx_ele(iterable, predicate)
    return result[0] if result is not None else result  # rip option monad not in python ; w ;


def find_ele[T](iterable: Iterable[T], predicate: Callable[[T], bool]) -> Optional[T]:
    result = find_idx_ele(iterable, predicate)
    return result[1] if result is not None else result  # rip option monad not in python ; w ;


# This results in the parent directory of the script
SCRIPT_DIR = Path(__file__).absolute().parent
DEBUG = False
TEST = """
"""


def part1(input: str):
    for line in input.splitlines():
        pass

    return 0


def part2(input: str):
    for line in input.splitlines():
        pass

    return 0


def main():
    print("Part 1")
    print("Test: ", test1 := part1(TEST))
    assert test1 == 0
    print("Answer: ", answer1 := part1(open(SCRIPT_DIR / "input").read()))
    assert answer1 == 0
    print("Part 2")
    print("Test: ", test2 := part2(TEST))
    assert test2 == 0
    print("Answer: ", answer2 := part2(open(SCRIPT_DIR / "input").read()))
    assert answer2 == 0


if __name__ == "__main__":
    main()

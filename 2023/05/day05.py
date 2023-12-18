import functools
import itertools
import json
import math
import re
import sys
from functools import cache

from collections import namedtuple, deque, defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, List, Optional, Literal, Tuple

def find_idx_ele[T](iterable: Iterable[T], predicate: Callable[[T], bool]) -> Optional[tuple[int, T]]:
    def predicate_tuple(tup: tuple[int, T]) -> bool:
        _, element = tup
        return predicate(element)
    idxele: Optional[tuple[int, T]] = next(filter(predicate_tuple, enumerate(iterable)), None)
    return idxele
def find_idx[T](iterable: Iterable[T], predicate: Callable[[T], bool]) -> Optional[int]:
    result = find_idx_ele(iterable, predicate)
    return result[0] if result is not None else result # rip option monad not in python ; w ;
def find_ele[T](iterable: Iterable[T], predicate: Callable[[T], bool]) -> Optional[T]:
    result = find_idx_ele(iterable, predicate)
    return result[1] if result is not None else result # rip option monad not in python ; w ;


# This results in the parent directory of the script
SCRIPT_DIR = Path(__file__).absolute().parent
DEBUG = False
TEST = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

def get_minimum_mapped_target(mapped_targets: List[int], mappings: str) -> int:
    for mapping in mappings.strip().split("\n\n"):
        header, lines = mapping.split("\n", 1)

        print(header) if DEBUG else None
        mapped = set()
        for line in lines.split('\n'):
            dest_start, source_start, length = map(int, line.split())
            for i, mapped_target in enumerate(mapped_targets):
                if source_start <= mapped_target < source_start + length and i not in mapped: # todo possible off-by-one
                    mapped.add(i)
                    #print(f"[{i = }] mapping {mapped_target} to {dest_start + (mapped_target - source_start)}") if DEBUG else None
                    mapped_targets[i] = dest_start + (mapped_target - source_start) # todo possible off-by-one

    return min(mapped_targets)


def part1(input: str):
    targetline, rest = input.split("\n", 1)
    targets: List[int] = list(map(int, targetline.strip().split(": ")[1].split()))
    return get_minimum_mapped_target(targets, rest)

def part2(input: str):
    return 0

def main():
    print("Part 1")
    print("Test: ", test1 := part1(TEST))
    assert test1 == 35
    print("Answer: ", answer1 := part1(open(SCRIPT_DIR / "input").read()))
    assert answer1 == 322500873
    # print("Part 2")
    # print("Test: ", test2 := part2(TEST))
    # assert test2 == 46
    # print("Answer: ", answer2 := part2(open(SCRIPT_DIR / "input").read()))
    # assert answer2 == 0

if __name__ == "__main__":
  main()

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


def find_idx_ele[
    T
](iterable: Iterable[T], predicate: Callable[[T], bool]) -> Optional[tuple[int, T]]:
    def predicate_tuple(tup: tuple[int, T]) -> bool:
        _, element = tup
        return predicate(element)

    idxele: Optional[tuple[int, T]] = next(
        filter(predicate_tuple, enumerate(iterable)), None
    )
    return idxele


def find_idx[T](iterable: Iterable[T], predicate: Callable[[T], bool]) -> Optional[int]:
    result = find_idx_ele(iterable, predicate)
    return (
        result[0] if result is not None else result
    )  # rip option monad not in python ; w ;


def find_ele[T](iterable: Iterable[T], predicate: Callable[[T], bool]) -> Optional[T]:
    result = find_idx_ele(iterable, predicate)
    return (
        result[1] if result is not None else result
    )  # rip option monad not in python ; w ;


# This results in the parent directory of the script
SCRIPT_DIR = Path(__file__).absolute().parent
DEBUG = False
TEST = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""


def part1(input: str):
    starts, branches = input.strip().split("\n\n")
    starts = dict(map(lambda x: x.split(": "), starts.splitlines()))
    branches = list(map(lambda x: x.split(" -> "), branches.splitlines()))

    frontier: deque[tuple[str, str]] = deque()
    lookup: dict[str, bool] = {}

    for start, value in starts.items():
        if start not in lookup:
            lookup[start] = bool(int(value))

    for branch, target in branches:
        frontier.append((branch, target))

    while frontier:
        branch, target = frontier.popleft()

        left, op, right = branch.split(" ")
        if left not in lookup or right not in lookup:
            frontier.append((branch, target))
            continue

        left = lookup[left]
        right = lookup[right]

        if op == "AND":
            lookup[target] = left & right

        elif op == "OR":
            lookup[target] = left | right

        elif op == "XOR":
            lookup[target] = left ^ right

    result = ""
    for key in sorted(
        filter(
            lambda x: x.startswith("z"),
            lookup.keys(),
        )
    ):
        result += "1" if lookup[key] else "0"

    return int(result[::-1], 2)


def part2(input: str):
    for line in input.splitlines():
        pass

    return 0


def main():
    print("Part 1")
    print("Test: ", test1 := part1(TEST))
    assert test1 == 2024
    print("Answer: ", answer1 := part1(open(SCRIPT_DIR / "input").read()))
    assert answer1 == 0
    print("Part 2")
    print("Test: ", test2 := part2(TEST))
    assert test2 == 0
    print("Answer: ", answer2 := part2(open(SCRIPT_DIR / "input").read()))
    assert answer2 == 0


if __name__ == "__main__":
    main()

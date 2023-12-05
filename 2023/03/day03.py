from collections.abc import Callable
from itertools import chain, groupby
from pathlib import Path
from typing import Iterable, List, Optional

DEBUG = False

TEST = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

type VerticalNeighbor = tuple[str, str, str]

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

def split_row_to_indexed_numbers(line: str) -> list[tuple[int, int, str]]:
    indexed_chars = list(enumerate(list(line)))
    # like so:
    # [(0, '.'), (1, '4'), (2, '6'), (3, '7'), (4, '.'), (5, '.'), (6, '1'), (7, '1'), (8, '4'), (9, '.'), (10, '.'), (11, '.')]

    contiugous_numbers = [list(g) for k, g in groupby(indexed_chars, lambda x: x[1].isdigit()) if k]
    # like so:
    # [[(1, '4'), (2, '6'), (3, '7')], [(6, '1'), (7, '1'), (8, '4')]]
    # representing indices for: [ 467, 114 ]

    # return tuples like: ( start_idx, end_idx, number_str)
    return [(number_chars_group[0][0], number_chars_group[-1][0] + 1, "".join(c for _, c in number_chars_group))
            for number_chars_group in contiugous_numbers
            if not DEBUG or len(number_chars_group) > 0 and all(len(e) == 2 for e in number_chars_group) # unnecessary invariant just for debugging
            ]

def get_number_surrounding_idx(data: List[str], row: int, col: int) -> Optional[int]:
    indexed_nums = split_row_to_indexed_numbers(data[row])
    number = find_ele(indexed_nums, lambda x: x[0] <= col < x[1])

    if number is None:
        print(f"DEBUG: no number found at {row}, {col}") if DEBUG else None
        return None
    return int(number[2]) if number is not None else None

def has_neighboring_symbol(vertical_neighbors: List[VerticalNeighbor], i: int) -> bool:
    return any(not neighbor.isdigit() and neighbor != "."
               for neighbor in chain(vertical_neighbors[i],
                                     vertical_neighbors[i + 1],
                                     vertical_neighbors[i - 1]
                                     )
               )

def get_two_neighboring_numbers(vertical_neighbors: List[VerticalNeighbor], i) -> tuple[Optional[tuple[int, int]], Optional[tuple[int, int]]]:
    # returns 0 indexed instead of -1 indexed, which is kind of weird
    # given that it's searching from i - 1 to i + 1 and j - 1 to j + 1

    col_left_neighbor = vertical_neighbors[i - 1]
    col_self_neighbor = vertical_neighbors[i]
    col_right_neighbor = vertical_neighbors[i + 1]

    cols = [col_left_neighbor, col_self_neighbor, col_right_neighbor]
    print(f"DEBUG: col orientation {cols}") if DEBUG else None
    rows = list(zip(*cols)) # transposed
    print(f"DEBUG: row orientation {rows}") if DEBUG else None
    row_top, row_mid, row_bot = rows
    row_top_neighbor = find_idx(row_top, lambda x: x.isdigit())
    row_mid_neighbor = find_idx(row_mid, lambda x: x.isdigit())
    row_bot_neighbor = find_idx(row_bot, lambda x: x.isdigit())

    # differing line cases
    if all(x is not None for x in [row_top_neighbor, row_mid_neighbor, row_bot_neighbor]):
        assert False, "undefined behavior for which two numbers to pick"
    elif row_top_neighbor is not None and row_mid_neighbor is not None:
        return (0, row_top_neighbor), (1, row_mid_neighbor)
    elif row_mid_neighbor is not None and row_bot_neighbor is not None:
        return (1, row_mid_neighbor), (2, row_bot_neighbor)
    elif row_top_neighbor is not None and row_bot_neighbor is not None:
        return (0, row_top_neighbor), (2, row_bot_neighbor)

    row_idx = find_idx(rows, lambda x: any(c.isdigit() for c in x))

    # no neighboring number case
    if row_idx is None:
        assert row_top_neighbor == None and row_mid_neighbor == None and row_bot_neighbor == None
        return None, None

    # all in one line case
    row = rows[row_idx]
    if row[0].isdigit() and not row[1].isdigit() and row[2].isdigit():
        # if there are two numbers on the same line, they must be on opposite sides of the gear
        return (row_idx, 0), (row_idx, 2)
    else:
        # only one neighbor case
        col_idx = find_idx(row, lambda x: x.isdigit())
        if col_idx is None:
            assert False, "could not find digit in row already verified as having digit"
        return (row_idx, col_idx), None

def row_pad(data):
    # pad top and bottom with empty rows
    empty_row = "." * len(data[0])
    data.insert(0, empty_row)
    data.append(empty_row)
    return data
def col_pad(data):
    # pad left and right with empty columns
    data = ["." + line + "." for line in data]
    return data

def part1(input):
    sum = 0
    data = input.splitlines()
    data = col_pad(row_pad(data))

    for i, line in enumerate(data):
        if i == 0 or i == len(data) - 1:
            continue
        vertical_neighbors: List[VerticalNeighbor] = list(zip(list(data[i - 1]), list(line), list(data[i + 1])))

        # so for a line like this:
        # ".467..114..."
        # we have vertical_neighbors like this:
        # [('.', '.', '.'), ('.', '4', '.'), ('.', '6', '.'), ('.', '7', '.'), ('.', '.', '*'), ('.', '.', '.'), ('.', '1', '.'), ('.', '1', '.'), ('.', '4', '.'), ('.', '.', '.'), ('.', '.', '.'), ('.', '.', '.')]

        # for each number in the line, check if it neighbors a symbol
        indexed_numbers = split_row_to_indexed_numbers(line)
        for start_idx, end_idx, num in indexed_numbers:
            if any(has_neighboring_symbol(vertical_neighbors, i) for i in range(start_idx, end_idx)):
                sum += int(num)

    return sum

def part2(input):
    sum = 0
    data = input.splitlines()
    data = col_pad(row_pad(data))

    for i, line in enumerate(data):
        if i == 0 or i == len(data) - 1:
            continue
        vertical_neighbors: List[VerticalNeighbor] = list(zip(list(data[i - 1]), list(line), list(data[i + 1])))

        # for each gear in the line, check if it neighbors a number
        for gear_idx, c in enumerate(list(line)):
            if c != "*":
                continue
            neighbor_one, neighbor_two = get_two_neighboring_numbers(vertical_neighbors, gear_idx)
            if neighbor_one is None or neighbor_two is None:
                continue

            x1, y1 = neighbor_one
            x2, y2 = neighbor_two
            num1 = get_number_surrounding_idx(data, i + x1 - 1, gear_idx + y1 - 1)
            num2 = get_number_surrounding_idx(data, i + x2 - 1, gear_idx + y2 - 1)
            if num1 is not None and num2 is not None:
                sum += num1 * num2

    return sum

SCRIPT_DIR = Path(__file__).absolute().parent

def main():
    print("Day 3")
    print("Part 1")
    print("Test: ", test1 := part1(TEST))
    assert test1 == 4361
    print("Answer: ", answer1 := part1(open(SCRIPT_DIR / "input").read()))
    assert answer1 == 519444
    print("Part 2")
    print("Test: ", test2 := part2(TEST))
    assert test2 == 467835
    print("Answer: ", answer2 := part2(open(SCRIPT_DIR / "input").read()))
    assert answer2 == 74528807

if __name__ == "__main__":
  main()

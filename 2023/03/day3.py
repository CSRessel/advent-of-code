from itertools import chain, groupby

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

def find_idx(iterable, predicate) -> int | None:
    def predicate_tuple(tup):
        _, element = tup
        return predicate(element)
    idx, _ = next(filter(predicate_tuple, enumerate(iterable)), (None, None))
    return idx

def get_number_surrounding_idx(data, row, col):
    line = data[row]
    indexed_chars = list(enumerate(list(line)))
    # like so:
    # [(0, '.'), (1, '4'), (2, '6'), (3, '7'), (4, '.'), (5, '.'), (6, '1'), (7, '1'), (8, '4'), (9, '.'), (10, '.'), (11, '.')]

    contiugous_numbers = [list(g) for k, g in groupby(indexed_chars, lambda x: x[1].isdigit()) if k]
    # like so:
    # [[(1, '4'), (2, '6'), (3, '7')], [(6, '1'), (7, '1'), (8, '4')]]
    # representing indices for: [ 467, 114 ]

    for each_contiugous_num in contiugous_numbers:
        if any(i == col for i, _ in each_contiugous_num):
            num = "".join([c for _, c in each_contiugous_num])
            return int(num)

    print(f"DEBUG: no number found at {row}, {col}") if DEBUG else None
    return None

def has_neighboring_symbol(vertical_neighbors, i):
    for neighbor in chain(vertical_neighbors[i], vertical_neighbors[i + 1], vertical_neighbors[i - 1]):
        if not neighbor.isdigit() and neighbor != ".":
            return True
    return False

def get_two_neighboring_numbers(vertical_neighbors, i):
    # returns 0 indexed instead of -1 indexed, which is kind of weird
    # given that it's searching from i - 1 to i + 1

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
    # all in one line case
    if row_idx is not None:
        row = rows[row_idx]
        #line = vertical_neighbors[i + row_idx - 1]
        if row[0].isdigit() and not row[1].isdigit() and row[2].isdigit():
            # if there are two numbers on the same line, they must be on opposite sides of the gear
            return (row_idx, 0), (row_idx, 2)
        else:
            # only one neighbor case
            col_idx = find_idx(row, lambda x: x.isdigit())
            return (row_idx, col_idx), None

    # no neighboring number case
    assert row_top_neighbor == None and row_mid_neighbor == None and row_bot_neighbor == None
    return None, None

def row_pad(data):
    # pad top and bottom with empty rows
    empty_row = "." * len(data[0])
    data.insert(0, empty_row)
    data.append(empty_row)
    return data

def part1(input):
    sum = 0
    data = input.splitlines()
    data = row_pad(data)

    for i, line in enumerate(data):
        if i == 0 or i == len(data) - 1:
            continue
        vertical_neighbors = list(zip(list(data[i - 1]), list(line), list(data[i + 1])))

        # pad left and right with empty columns
        vertical_neighbors.insert(0, (".", ".", "."))
        vertical_neighbors.append((".", ".", "."))
        line = "." + line + "."

        # so for a line like this:
        # ".467..114..."
        # we have vertical_neighbors like this:
        # [('.', '.', '.'), ('.', '4', '.'), ('.', '6', '.'), ('.', '7', '.'), ('.', '.', '*'), ('.', '.', '.'), ('.', '1', '.'), ('.', '1', '.'), ('.', '4', '.'), ('.', '.', '.'), ('.', '.', '.'), ('.', '.', '.')]

        # for each number in the line, check if it neighbors a symbol
        part_number_evidence = [c.isdigit() and has_neighboring_symbol(vertical_neighbors, i) for i, c in enumerate(list(line))]
        # like so:
        # [False, False, False, True, False, False, False, False, False, False, False, False]

        indexed_chars = list(enumerate(list(line)))
        # like so:
        # [(0, '.'), (1, '4'), (2, '6'), (3, '7'), (4, '.'), (5, '.'), (6, '1'), (7, '1'), (8, '4'), (9, '.'), (10, '.'), (11, '.')]

        contiugous_numbers = [list(g) for k, g in groupby(indexed_chars, lambda x: x[1].isdigit()) if k]
        # like so:
        # [[(1, '4'), (2, '6'), (3, '7')], [(6, '1'), (7, '1'), (8, '4')]]
        # representing indices for: [ 467, 114 ]

        for each_contiugous_num in contiugous_numbers:
            if any(part_number_evidence[i] for i, _ in each_contiugous_num):
                num = "".join([c for _, c in each_contiugous_num])
                sum += int(num)
    return sum

def part2(input):
    sum = 0
    data = input.splitlines()
    data = row_pad(data)

    for i, line in enumerate(data):
        if i == 0 or i == len(data) - 1:
            continue
        vertical_neighbors = list(zip(list(data[i - 1]), list(line), list(data[i + 1])))

        # pad left and right with empty columns
        vertical_neighbors.insert(0, (".", ".", "."))
        vertical_neighbors.append((".", ".", "."))
        line = "." + line + "."

        # for each gear in the line, check if it neighbors a number
        for gear_idx, c in enumerate(list(line)):
            if c != "*":
                continue
            print(f"DEBUG: found gear at {i}, {gear_idx}, with neighbors:") if DEBUG else None
            neighbor_one, neighbor_two = get_two_neighboring_numbers(vertical_neighbors, gear_idx)
            if neighbor_one is not None and neighbor_two is not None:
                x1, y1 = neighbor_one
                x2, y2 = neighbor_two
                # -2 because we added an empty column to our vertical_neighbors,
                # not present in the full data variable
                num1 = get_number_surrounding_idx(data, i + x1 - 1, gear_idx + y1 - 2)
                num2 = get_number_surrounding_idx(data, i + x2 - 1, gear_idx + y2 - 2)
                if num1 is not None and num2 is not None:
                    sum += num1 * num2

    return sum

def main():
    print("Day 3")
    print("Part 1")
    print("Test: ", part1(TEST))
    print("Answer: ", part1(open("input").read()))
    print("Part 2")
    print("Test: ", part2(TEST))
    print("Answer: ", part2(open("input").read()))

if __name__ == "__main__":
  main()

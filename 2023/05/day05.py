from functools import reduce
from collections.abc import Generator
from pathlib import Path
from typing import List, Tuple

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

def get_minimum_mapped_target(mapped_targets: List[int], mappings: List[str]) -> int:
    for mapping in mappings:
        header, *lines = mapping.strip().split("\n")

        print(header) if DEBUG else None
        mapped = set()
        for line in lines[1:]:
            dest_start, source_start, length = map(int, line.split())
            for i, mapped_target in enumerate(mapped_targets):
                if source_start <= mapped_target < source_start + length and i not in mapped:
                    mapped.add(i)
                    #print(f"[{i = }] mapping {mapped_target} to {dest_start + (mapped_target - source_start)}") if DEBUG else None
                    mapped_targets[i] = dest_start + (mapped_target - source_start)

    return min(mapped_targets)


def part1(input: str):
    targetline, *mappings = input.split("\n\n")
    targets: List[int] = list(map(int, targetline.strip().split()[1:]))
    return get_minimum_mapped_target(targets, mappings)

def part2(input: str):
    reduce(lambda x, y: x * y, [1, 2, 3])
    targetline, *mappings = input.split("\n\n")
    target_nums: List[int] = list(map(int, targetline.strip().split()[1:]))
    target_intervals = list(zip(target_nums[0::2], target_nums[1::2]))

    # generator of (start, length) tuples
    def lookup(inputs: Generator[Tuple[int, int], None, None], mapping: str) -> Generator[Tuple[int, int], None, None]:
        for target_start, target_length in inputs:
            while target_length > 0:
                print(mapping) if DEBUG else None
                for m in mapping.strip().split("\n")[1:]:
                    # for each interval mapping, apply it to the currently manipulated target interval
                    dest_start, source_start, mapping_length = map(int, m.split())

                    if source_start <= target_start < source_start + mapping_length:
                        # if the mapping intersects our current target interval
                        # then we emit the newly mapped range
                        mapping_length = min(mapping_length - (target_start - source_start), target_length)
                        yield (dest_start + target_start - source_start, mapping_length)
                        # then update the target interval to be just the remainder of the interval
                        # and break the for loop so we can start again looking for another mapping intersecting the remainder interval
                        # (unless the remainder length is non-positive, in which case we're finished with this target interval)
                        target_start += mapping_length
                        target_length -= mapping_length
                        break
                else:
                    # no mapping intersected the target interval, so we just emit the target interval as-is
                    yield (target_start, target_length)
                    break

    # note: the iterable args need to be re-packed as generators for the typing of the reduce function to work
    return min(reduce(lookup, (m for m in mappings), (tr for tr in target_intervals)))[0]

def main():
    print("Part 1")
    print("Test: ", test1 := part1(TEST))
    assert test1 == 35
    print("Answer: ", answer1 := part1(open(SCRIPT_DIR / "input").read()))
    assert answer1 == 322500873
    print("Part 2")
    print("Test: ", test2 := part2(TEST))
    assert test2 == 46
    print("Answer: ", answer2 := part2(open(SCRIPT_DIR / "input").read()))
    assert answer2 == 108956227

if __name__ == "__main__":
  main()

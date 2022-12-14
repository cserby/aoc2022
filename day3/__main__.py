from functools import reduce
from typing import List, Set, Tuple

from utils import chunks, file_lines


def split_in_half(line: str) -> Tuple[str, str]:
    length = len(line)
    return line[: int(length / 2)], line[int(length / 2) :]


def to_ord_set(comp: str) -> Set[int]:
    return {ord(ch) for ch in comp}


def find_common(compartments: List[str]) -> Set[int]:
    assert len(compartments) >= 2
    return reduce(
        lambda prev, curr: prev & to_ord_set(curr),
        compartments[1:],
        to_ord_set(compartments[0]),
    )


def ord_to_prio(ord: int) -> int:
    if 97 <= ord <= 122:
        return ord - 96
    else:
        return ord - 38


def part1(fn: str) -> int:
    return sum(
        [
            ord_to_prio(find_common(list(split_in_half(line))).pop())
            for line in file_lines(fn)
        ]
    )


def part2(fn: str) -> int:
    return sum(
        [
            ord_to_prio(find_common(list(group)).pop())
            for group in chunks(file_lines(fn), 3, "")
        ]
    )


print(f"Part1 Sample: {part1('day3/sample')}")
print(f"Part1: {part1('day3/input')}")
print(f"Part2 Sample: {part2('day3/sample')}")
print(f"Part2: {part2('day3/input')}")

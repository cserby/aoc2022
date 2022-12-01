from functools import reduce
from typing import Generator, Iterator, List

from utils import file_lines


def split_inventories(lines: Iterator[str]) -> Generator[List[int], None, None]:
    inventory: List[int] = []
    for line in lines:
        if line == "":
            yield inventory
            inventory = []
        else:
            inventory += [int(line)]
    yield inventory


def sum_inventories(inventories: Iterator[List[int]]) -> Generator[int, None, None]:
    for inventory in inventories:
        yield reduce(lambda prev, curr: prev + curr, inventory, 0)


def part1(input_fn: str):
    return max(sum_inventories(split_inventories(file_lines(input_fn))))


def part2(input_fn: str):
    return sum(
        sorted(sum_inventories(split_inventories(file_lines(input_fn))), reverse=True)[
            0:3
        ]
    )


print(f"Part1 Sample: {part1('day1/sample')}")
print(f"Part1: {part1('day1/input')}")
print(f"Part2 Sample: {part2('day1/sample')}")
print(f"Part2: {part2('day1/input')}")

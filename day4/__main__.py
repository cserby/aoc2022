from typing import Tuple

from utils import file_lines


def parse_assignment(line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    (range1, range2) = line.split(",")

    def range_str_to_start_end(range: str):
        (start, end) = range.split("-")
        return (int(start), int(end))

    return (range_str_to_start_end(range1), range_str_to_start_end(range2))


def subset(range1: Tuple[int, int], range2: Tuple[int, int]) -> bool:
    (start1, end1) = range1
    (start2, end2) = range2

    return start1 <= start2 and end2 <= end1


def subset_any_way(range1: Tuple[int, int], range2: Tuple[int, int]) -> bool:
    return subset(range1, range2) or subset(range2, range1)


def part1(file_name: str):
    count = 0
    for line in file_lines(file_name):
        if subset_any_way(*parse_assignment(line)):
            count += 1
    return count


def is_overlapping(range1: Tuple[int, int], range2: Tuple[int, int]) -> bool:
    (start1, end1) = range1
    (start2, end2) = range2

    return len(set(range(start1, end1 + 1)) & set(range(start2, end2 + 1))) > 0


def part2(file_name: str):
    count = 0
    for line in file_lines(file_name):
        if is_overlapping(*parse_assignment(line)):
            count += 1
    return count


print(f"Part1 Sample: {part1('day4/sample')}")
print(f"Part1: {part1('day4/input')}")
print(f"Part2 Sample: {part2('day4/sample')}")
print(f"Part2: {part2('day4/input')}")

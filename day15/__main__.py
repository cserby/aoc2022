import re
from typing import Generator, List, Optional, Set, Tuple

from utils import file_lines
from utils.geometry import Point


def parse(line: str) -> Tuple[Point, Point]:
    m = re.match(
        r"^Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)$",
        line,
    )
    assert m is not None, f"Failed to parse line: {line}"
    assert len(m.groups()) == 4, f"Failed to parse line: {line}"
    return (
        Point(int(m.group(1)), int(m.group(2))),
        Point(int(m.group(3)), int(m.group(4))),
    )


def find_excluded_spots(
    sensor: Point, closest: Point, line_y: int
) -> Optional[Tuple[int, int]]:
    distance = sensor.distance(closest)
    distance_from_line = abs(sensor.y - line_y)
    if distance < distance_from_line:
        return None
    width_of_cut_to_one_side = distance - distance_from_line
    return (sensor.x - width_of_cut_to_one_side, sensor.x + width_of_cut_to_one_side)


def beacons_on_line(beacons: Set[Point], line_y: int) -> int:
    return len({b for b in beacons if b.y == line_y})


class NotMergeableException(Exception):
    pass


def merge_ordered_sections(
    first: Tuple[int, int], second: Tuple[int, int]
) -> Tuple[int, int]:
    (first_low, first_high) = first
    (second_low, second_high) = second
    if second_low <= second_high:
        return (first_low, max(first_high, second_high))
    else:
        raise NotMergeableException(first, second)


def merge_excludeds(
    excludeds: List[Tuple[int, int]]
) -> Generator[Tuple[int, int], None, None]:
    it = iter(sorted(excludeds))
    curr = next(it)
    for nxt in excludeds:
        try:
            curr = merge_ordered_sections(curr, nxt)
        except NotMergeableException:
            yield curr
            curr = nxt
    yield curr


def part1(fn: str) -> int:
    Y = 10 if fn.endswith("sample") else 2000000
    beacons: Set[Point] = set()
    excludeds: List[Tuple[int, int]] = []
    for l in file_lines(fn):
        sensor, closest = parse(l)
        beacons.add(closest)
        excluded = find_excluded_spots(sensor, closest, Y)
        if excluded is not None:
            excludeds += [excluded]
    return sum(excl_high - excl_low + 1 for excl_low, excl_high in merge_excludeds(excludeds)) - beacons_on_line(
        beacons, Y
    )


def part2(fn: str) -> int:
    raise NotImplementedError()


print(f"Part1 Sample: {part1('day15/sample')}")
print(f"Part1: {part1('day15/input')}")
# print(f"Part2 Sample: {part2('day15/sample')}")
# print(f"Part2: {part2('day15/input')}")

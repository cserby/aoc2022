import cProfile
from functools import reduce
from typing import Generator, Iterator, List, Optional, Set

from utils import file_lines
from utils.geometry import HorizontalOrVerticalLine, Point, draw_coordinates


def lines(lines: Iterator[str]) -> Generator[HorizontalOrVerticalLine, None, None]:
    for line in lines:
        endpoints = line.split(" -> ")
        for i in range(len(endpoints) - 1):
            yield HorizontalOrVerticalLine(
                Point.from_string(endpoints[i]), Point.from_string(endpoints[i + 1])
            )


class InletBlockedException(Exception):
    pass


class FellIntoAbyssException(Exception):
    pass


def collision(
    new_sand: Point,
    line_points: Set[Point],
    sands: Set[Point],
    bottom: Optional[int] = None,
) -> bool:
    if new_sand.y == bottom:
        return True
    if new_sand in sands:
        return True
    if new_sand in line_points:
        return True
    return False


def drop_sand(
    line_points: Set[Point],
    sands: Set[Point],
    lowest: int,
    bottom: Optional[int] = None,
) -> Point:
    sand = Point(500, 0)
    while sand.y < lowest:
        # print(draw_pit(lines, sands))

        new_sand = sand.move(dy=1)

        if collision(new_sand, line_points, sands, bottom):
            new_sand = sand.move(dx=-1, dy=1)

            if collision(new_sand, line_points, sands, bottom):
                new_sand = sand.move(dx=1, dy=1)

                if collision(new_sand, line_points, sands, bottom):
                    if sand == Point(500, 0):
                        raise InletBlockedException(sand)
                    else:
                        return sand

        sand = new_sand

    raise FellIntoAbyssException(sand)


def lowest_point(lines: List[HorizontalOrVerticalLine]) -> int:
    return max(l.high.y for l in lines)


def draw_pit(line_points: Set[Point], sands: Set[Point]) -> str:
    return draw_coordinates(
        points={
            **{
                Point(500, 0): "+",
            },
            **{sand: "s" for sand in sands},
            **{lp: "#" for lp in line_points},
        },
    )


def part1(fn: str) -> int:
    ls = list(lines(file_lines(fn)))
    lowest = lowest_point(ls)
    line_points: Set[Point] = reduce(lambda prev, curr: prev | curr.points(), ls, set())
    sands: Set[Point] = set()

    try:
        while True:
            sands.add(drop_sand(line_points, sands, lowest))
    except FellIntoAbyssException:
        print(draw_pit(line_points, sands))
        return len(sands)


def part2(fn: str) -> int:
    ls = list(lines(file_lines(fn)))
    lowest = lowest_point(ls)
    line_points: Set[Point] = reduce(lambda prev, curr: prev | curr.points(), ls, set())
    sands: Set[Point] = set()

    try:
        while True:
            sands.add(drop_sand(line_points, sands, lowest + 3, bottom=lowest + 2))
    except InletBlockedException:
        print(draw_pit(line_points, sands))
        return len(sands) + 1


# cProfile.run("part1('day14/input')")
print(f"Part1 Sample: {part1('day14/sample')}")
print(f"Part1: {part1('day14/input')}")
print(f"Part2 Sample: {part2('day14/sample')}")
print(f"Part2: {part2('day14/input')}")

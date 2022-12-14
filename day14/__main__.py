from typing import Generator, Iterator, List

from utils import file_lines
from utils.geometry import HorizontalOrVerticalLine, Point, draw_coordinates

import cProfile


def lines(lines: Iterator[str]) -> Generator[HorizontalOrVerticalLine, None, None]:
    for line in lines:
        endpoints = line.split(" -> ")
        for i in range(len(endpoints) - 1):
            yield HorizontalOrVerticalLine(
                Point.from_string(endpoints[i]), Point.from_string(endpoints[i + 1])
            )


class CantMoveFurtherException(Exception):
    pass


class FellIntoAbyssException(Exception):
    pass


def collision(
    new_sand: Point, lines: List[HorizontalOrVerticalLine], sands: List[Point]
) -> bool:
    return any(new_sand == p for p in sands) or any(l.online(new_sand) for l in lines)


def drop_sand(
    lines: List[HorizontalOrVerticalLine], sands: List[Point], lowest: int
) -> Point:
    sand = Point(500, 0)
    while sand.y < lowest:
        # print(draw_pit(lines, sands))

        new_sand = sand.move(dy=1)

        if collision(new_sand, lines, sands):
            new_sand = sand.move(dx=-1, dy=1)

            if collision(new_sand, lines, sands):
                new_sand = sand.move(dx=1, dy=1)

                if collision(new_sand, lines, sands):
                    return sand

        sand = new_sand

    raise FellIntoAbyssException(sand)


def lowest_point(lines: List[HorizontalOrVerticalLine]) -> int:
    return max(max(l.end1.y, l.end2.y) for l in lines)


def draw_pit(lines: List[HorizontalOrVerticalLine], sands: List[Point]) -> str:
    return draw_coordinates(
        points={
            **{
                Point(500, 0): "+",
            },
            **{sand: "s" for sand in sands},
        },
        lines=lines,
    )


def part1(fn: str) -> int:
    ls = list(lines(file_lines(fn)))
    lowest = lowest_point(ls)
    sands: List[Point] = []

    try:
        while True:
            sands.insert(0, drop_sand(ls, sands, lowest))
    except FellIntoAbyssException:
        print(draw_pit(ls, sands))
        return len(sands)


def part2(fn: str) -> int:
    raise NotImplementedError()


cProfile.run("part1('day14/input')")
# print(f"Part1 Sample: {part1('day14/sample')}")
# print(f"Part1: {part1('day14/input')}")
# print(f"Part2 Sample: {part2('day14/sample')}")
# print(f"Part2: {part2('day14/input')}")

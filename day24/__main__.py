import math
from collections import defaultdict
from enum import Enum
from typing import Dict, Generator, List, Set, Tuple

from utils import file_lines
from utils.matrix import down_of, indices, left_of, matrix_to_str, right_of, up_of, horizontal_and_vertical_neighbor_indices

# from utils.geometry import Point, draw_coordinates


def parse_field(lines: List[str]) -> List[List[str]]:
    return [[c for c in l[1:-1]] for l in lines[1:-1]]


def calc_periodicity(field: List[List[str]]) -> int:
    return math.lcm(len(field[0]), len(field))


def open_timeslots(field: List[List[str]]) -> List[List[Set[int]]]:
    periodicity = calc_periodicity(field)

    cell_open_at_timeslots = [
        [{n for n in range(periodicity)} for _ in r] for r in field
    ]

    for (x, y) in indices(field):
        match field[x][y]:
            case ">":
                for cell in range(y, y + periodicity):
                    try:
                        if x == 0 and cell % len(cell_open_at_timeslots[x]) == 0:
                            print(f"{field[x][y]} {(x, y)} at {cell - y}")
                        cell_open_at_timeslots[x][
                            cell % len(cell_open_at_timeslots[x])
                        ].remove(cell - y)
                    except KeyError:
                        pass
            case "v":
                for row in range(x, x + periodicity):
                    try:
                        if y == 0 and row % len(cell_open_at_timeslots) == 0:
                            print(f"{field[x][y]} {(x, y)} at {row - x}")
                        cell_open_at_timeslots[row % len(cell_open_at_timeslots)][
                            y
                        ].remove(row - x)
                    except KeyError:
                        pass
            case "^":
                for row in range(x, x - periodicity, -1):
                    try:
                        if y == 0 and abs(row % len(cell_open_at_timeslots)) == 0:
                            print(f"{field[x][y]} {(x, y)} at {abs(row - x)}")
                        cell_open_at_timeslots[abs(row % len(cell_open_at_timeslots))][
                            y
                        ].remove(abs(row - x))
                    except KeyError:
                        pass
            case "<":
                for cell in range(y, y - periodicity, -1):
                    try:
                        if x == 0 and abs(cell % len(cell_open_at_timeslots[x])) == 0:
                            print(f"{field[x][y]} {(x, y)} at {abs(cell - y)}")
                        cell_open_at_timeslots[x][
                            abs(cell % len(cell_open_at_timeslots[x]))
                        ].remove(abs(cell - y))
                    except KeyError:
                        pass
            case ".":
                continue
            case _:
                assert False

    return cell_open_at_timeslots

def part1(fn: str) -> int:
    lines = list(file_lines(fn))
    field = parse_field(lines)

    print(matrix_to_str(open_timeslots(field), cell_size=10))

    raise NotImplementedError()


def part2(fn: str) -> int:
    raise NotImplementedError()


print(f"Part1 Sample: {part1('day24/sample')}")
# print(f"Part1: {part1('day24/input')}")
# print(f"Part2 Sample: {part2('day24/sample')}")
# print(f"Part2: {part2('day24/input')}")

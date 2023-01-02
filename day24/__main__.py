from collections import defaultdict
from enum import Enum
from typing import Dict, Generator, List, Set, Tuple

from utils import file_lines
from utils.matrix import down_of, indices, left_of, matrix_to_str, right_of, up_of
import math

# from utils.geometry import Point, draw_coordinates


def part1(fn: str) -> int:
    lines = list(file_lines(fn))
    # input: 150 (3x5x5x2) x 20 (2x5x2) -> periodicity 3x5x5x2x2 = 300
    # sample: 6 x 4 -> periodicity 12
    field_width = len(lines[1]) - 2
    field_height = len(lines) - 2
    periodicity = math.lcm(field_width, field_height)
    field = [[c for c in l[1:-1]] for l in lines[1:-1]]
    cell_open = [
        [{n for n in range(periodicity)} for _ in l[1:-1]] for l in lines[1:-1]
    ]

    for (x, y) in indices(field):
        match field[x][y]:
            case ">":
                for cell in range(y, y + periodicity):
                    try:
                        if x == 0 and cell % len(cell_open[x]) == 0:
                            print(f"{field[x][y]} {(x, y)} at {cell - y}")
                        cell_open[x][cell % len(cell_open[x])].remove(cell - y)
                    except KeyError:
                        pass
            case "v":
                for row in range(x, x + periodicity):
                    try:
                        if y == 0 and row % len(cell_open) == 0:
                            print(f"{field[x][y]} {(x, y)} at {row - x}")
                        cell_open[row % len(cell_open)][y].remove(row - x)
                    except KeyError:
                        pass
            case "^":
                for row in range(x, x - periodicity, -1):
                    try:
                        if y == 0 and abs(row % len(cell_open)) == 0:
                            print(f"{field[x][y]} {(x, y)} at {abs(row - x)}")
                        cell_open[abs(row % len(cell_open))][y].remove(abs(row - x))
                    except KeyError:
                        pass
            case "<":
                for cell in range(y, y - periodicity, -1):
                    try:
                        if x == 0 and abs(cell % len(cell_open[x])) == 0:
                            print(f"{field[x][y]} {(x, y)} at {abs(cell - y)}")
                        cell_open[x][abs(cell % len(cell_open[x]))].remove(abs(cell - y))
                    except KeyError:
                        pass
            case ".":
                continue
            case _:
                assert False

    print(matrix_to_str(cell_open, cell_size=10))

    raise NotImplementedError()


def part2(fn: str) -> int:
    raise NotImplementedError()


print(f"Part1 Sample: {part1('day24/sample')}")
# print(f"Part1: {part1('day24/input')}")
# print(f"Part2 Sample: {part2('day24/sample')}")
# print(f"Part2: {part2('day24/input')}")

from typing import Generator, List, Tuple

from utils import file_lines

Grid = List[List[List[bool]]]

GRID_SIZE = 21


def neighbors(x: int, y: int, z: int) -> Generator[Tuple[int, int, int], None, None]:
    for x_1 in [x - 1, x + 1]:
        if x_1 < 0 or x_1 > GRID_SIZE - 1:
            continue
        yield (x_1, y, z)
    for y_1 in [y - 1, y + 1]:
        if y_1 < 0 or y_1 > GRID_SIZE - 1:
            continue
        yield (x, y_1, z)
    for z_1 in [z - 1, z + 1]:
        if z_1 < 0 or z_1 > GRID_SIZE - 1:
            continue
        yield (x, y, z_1)


def part1(fn: str) -> int:
    surface: int = 0

    grid = [
        [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for _ in range(GRID_SIZE)
    ]

    for line in file_lines(fn):
        (x, y, z) = [int(c) for c in line.split(",")]

        assert grid[x][y][z] == False
        surface += 6

        for (x_1, y_1, z_1) in neighbors(x, y, z):
            if grid[x_1][y_1][z_1]:
                surface -= 2

        grid[x][y][z] = True

    return surface


IntGrid = List[List[List[int]]]


def parse(fn: str) -> IntGrid:
    grid = [
        [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for _ in range(GRID_SIZE)
    ]

    for line in file_lines(fn):
        (x, y, z) = [int(c) for c in line.split(",")]

        assert grid[x][y][z] == 0

        grid[x][y][z] = 1

    return grid


def fill_steam(grid: IntGrid) -> None:
    assert grid[0][0][0] == 0

    grid[0][0][0] = 2

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            for z in range(GRID_SIZE):
                if grid[x][y][z] != 0:
                    continue
                if any(grid[x1][y1][z1] == 2 for (x1, y1, z1) in neighbors(x, y, z)):
                    grid[x][y][z] = 2


def part2(fn: str) -> int:
    grid = parse(fn)

    assert grid[0][0][0] == False

    fill_steam(grid)

    surface = 0

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            for z in range(GRID_SIZE):
                if grid[x][y][z] == 1:
                    for (x_1, y_1, z_1) in neighbors(x, y, z):
                        if grid[x_1][y_1][z_1] == 2:
                            surface += 1

    return surface


# print(f"Part1 Sample: {part1('day18/sample')}")
# print(f"Part1: {part1('day18/input')}")
print(f"Part2 Sample: {part2('day18/sample')}")
# cProfile.run("print(part1('day18/input'))")
print(f"Part2: {part2('day18/input')}")

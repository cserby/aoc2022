from typing import List, Optional, Set, Tuple

from utils import file_lines
from utils.matrix import (
    cell_value,
    horizontal_and_vertical_neighbor_indices,
    indices,
    matrix_of_size,
    matrix_to_str,
    read_matrix,
)


def move_allowed(
    height_map: List[List[str]],
    from_coords: Tuple[int, int],
    to_coords: Tuple[int, int],
) -> bool:
    def height_value(height: str) -> int:
        if height == "S":
            return ord("a")
        elif height == "E":
            return ord("z")
        else:
            return ord(height)

    from_height = cell_value(height_map, from_coords[0], from_coords[1])
    assert from_height is not None
    to_height = cell_value(height_map, to_coords[0], to_coords[1])
    assert to_height is not None

    return height_value(to_height) <= height_value(from_height) + 1


def shortest_path(
    height_map: List[List[str]], end_coords: Tuple[int, int]
) -> List[List[int]]:

    distances = matrix_of_size(len(height_map), len(height_map[0]), -1)
    distances[end_coords[0]][end_coords[1]] = 0
    not_visited = set(indices(height_map))
    frontier = {end_coords}

    while len(frontier) > 0:
        curr_coords = frontier.pop()
        curr_distance = cell_value(distances, curr_coords[0], curr_coords[1])
        assert curr_distance is not None
        assert curr_distance != -1

        try:
            not_visited.remove(curr_coords)
        except KeyError:
            pass

        for neighbor in horizontal_and_vertical_neighbor_indices(
            height_map, curr_coords[0], curr_coords[1]
        ):
            if move_allowed(height_map, from_coords=neighbor, to_coords=curr_coords):
                neighbor_distance = cell_value(distances, neighbor[0], neighbor[1])
                assert neighbor_distance is not None
                if neighbor_distance > curr_distance + 1 or neighbor_distance == -1:
                    distances[neighbor[0]][neighbor[1]] = curr_distance + 1
                    frontier.add(neighbor)

    return distances


def part1(fn: str) -> int:
    height_map = read_matrix(file_lines(fn), lambda s: s)

    start_coords: Optional[Tuple[int, int]] = None
    end_coords: Optional[Tuple[int, int]] = None

    for (x, y) in indices(height_map):
        cell = cell_value(height_map, x, y)
        if cell == "S":
            start_coords = (x, y)
        elif cell == "E":
            end_coords = (x, y)

    assert start_coords is not None
    assert end_coords is not None

    distances = shortest_path(height_map, end_coords)
    c_v = cell_value(distances, start_coords[0], start_coords[1])
    assert c_v is not None
    return c_v


def part2(fn: str) -> int:
    height_map = read_matrix(file_lines(fn), lambda s: s)

    start_coords: Set[Tuple[int, int]] = set()
    end_coords: Optional[Tuple[int, int]] = None

    for (x, y) in indices(height_map):
        cell = cell_value(height_map, x, y)
        if cell == "S" or cell == "a":
            start_coords.add((x, y))
        elif cell == "E":
            end_coords = (x, y)

    assert start_coords is not None
    assert end_coords is not None

    distances = shortest_path(height_map, end_coords)
    return min(
        [
            dist
            for dist in [
                cell_value(distances, start_coord[0], start_coord[1])
                for start_coord in start_coords
            ]
            if dist is not None and dist != -1
        ]
    )


print(f"Part1 Sample: {part1('day12/sample')}")
print(f"Part1: {part1('day12/input')}")
print(f"Part2 Sample: {part2('day12/sample')}")
print(f"Part2: {part2('day12/input')}")

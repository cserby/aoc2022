from typing import Any, Generator, List, Optional, Tuple, TypeVar

T = TypeVar("T")


def indices(matrix: List[List[Any]]) -> Generator[Tuple[int, int], None, None]:
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            yield x, y


def horizontal_and_vertical_neighbor_indices(
    matrix: List[List[Any]], x: int, y: int
) -> Generator[Tuple[int, int], None, None]:
    if x > 0:
        yield (x - 1, y)
    if x < len(matrix) - 1:
        yield (x + 1, y)
    if y > 0:
        yield (x, y - 1)
    if y < len(matrix[0]) - 1:
        yield (x, y + 1)


def horizontal_vertical_and_diagonal_neighbor_indices(
    matrix: List[List[Any]], x: int, y: int
) -> Generator[Tuple[int, int], None, None]:
    if x > 0:
        yield (x - 1, y)
        if y > 0:
            yield (x - 1, y - 1)
    if x < len(matrix) - 1:
        yield (x + 1, y)
        if y < len(matrix[0]) - 1:
            yield (x + 1, y + 1)
    if y > 0:
        yield (x, y - 1)
        if x < len(matrix) - 1:
            yield (x + 1, y - 1)
    if y < len(matrix[0]) - 1:
        yield (x, y + 1)
        if x > 0:
            yield (x - 1, y + 1)


def matrix_to_str(matrix: List[List[Any]]) -> str:
    matrix_str = ""
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            matrix_str += f"{str(matrix[x][y])}"
        matrix_str += "\n"

    return matrix_str


def safe_list_get(list: List[T], index: int, default: Optional[T]) -> Optional[T]:
    if index < 0:
        return default
    try:
        return list[index]
    except IndexError:
        return default


U = TypeVar("U")


def cell_value(matrix: List[List[U]], x: int, y: int) -> Optional[U]:
    return safe_list_get(safe_list_get(matrix, x, []), y, None)  # type: ignore


def horizontal_and_vertical_neighbor_values(
    matrix: List[List[T]], x: int, y: int
) -> Generator[T, None, None]:
    for (n_x, n_y) in horizontal_and_vertical_neighbor_indices(matrix, x, y):
        c_v = cell_value(matrix, n_x, n_y)
        if c_v is not None:
            yield c_v


def is_cell_local_minimum(matrix: List[List[int]], x: int, y: int) -> bool:
    c_v = cell_value(matrix, x, y)
    if c_v is None:
        raise IndexError(x, y)
    return all(c_v < n for n in horizontal_and_vertical_neighbor_values(matrix, x, y))


def local_minimum_indices(
    matrix: List[List[int]],
) -> Generator[Tuple[int, int], None, None]:
    for (x, y) in indices(matrix):
        if is_cell_local_minimum(matrix, x, y):
            yield (x, y)

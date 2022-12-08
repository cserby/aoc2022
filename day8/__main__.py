from functools import reduce
from typing import List

from utils import file_lines
from utils.matrix import cols, matrix_of_size, matrix_to_str, read_matrix, rows


def visible_in_line(line: List[int]) -> List[bool]:
    prev_max = None
    visible = []
    for elem in line:
        if prev_max is None or elem > prev_max:
            visible.append(True)
            prev_max = elem
        else:
            visible.append(False)
    return visible


def or_merge_bool_matrices(
    one: List[List[bool]], other: List[List[bool]]
) -> List[List[bool]]:
    return [
        [one_cell or other_cell for one_cell, other_cell in zip(one_row, other_row)]
        for (one_row, other_row) in zip(one, other)
    ]


def sum_bool_matrix(matrix: List[List[bool]]) -> int:
    return sum(sum(int(cell) for cell in row) for row in matrix)


def visible_in_forest(forest: List[List[int]]) -> List[List[bool]]:

    visible_from_left = [visible_in_line(row) for row in rows(forest)]
    visible_from_right = [
        list(reversed(visible_in_line(list(reversed(row))))) for row in rows(forest)
    ]
    visible_from_top = list(cols([visible_in_line(col) for col in cols(forest)]))
    visible_from_bottom = list(
        cols(
            [
                list(reversed(visible_in_line(list(reversed(col)))))
                for col in cols(forest)
            ]
        )
    )

    return reduce(
        lambda prev, curr: or_merge_bool_matrices(prev, curr),
        [
            visible_from_left,
            visible_from_right,
            visible_from_top,
            visible_from_bottom,
        ],
        matrix_of_size(len(forest), len(forest[0]), False),
    )


def part1(fn: str):
    forest = read_matrix(file_lines(fn), int)
    visible = visible_in_forest(forest)
    return sum_bool_matrix(visible)


def part2(fn: str):
    pass


print(f"Part1 Sample: {part1('day8/sample')}")
print(f"Part1: {part1('day8/input')}")
# print(f"Part2 Sample: {part2('day8/sample')}")
# print(f"Part2: {part2('day8/input')}")

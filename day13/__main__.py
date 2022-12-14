from itertools import zip_longest
from typing import Generator, List, Tuple

from utils import file_lines, match_into_chunks
from functools import cmp_to_key

StrangeNumber = int | List["StrangeNumber"] | None


def pairs(fn: str) -> Generator[Tuple[StrangeNumber, StrangeNumber], None, None]:
    for [left_str, right_str] in match_into_chunks(
        file_lines(fn), lambda s: s == "", return_match=False
    ):
        left: StrangeNumber = eval(left_str)
        right: StrangeNumber = eval(right_str)
        yield (left, right)


def compare(left: StrangeNumber, right: StrangeNumber) -> int:
    # -1: left is greater
    # 0: equal
    # 1: right is greater
    match left:
        case list():
            match right:
                case list():
                    for (new_left, new_right) in zip_longest(
                        left, right, fillvalue=None
                    ):
                        compare_result = compare(new_left, new_right)
                        if compare_result != 0:
                            return compare_result
                    return 0
                case int():
                    return compare(left, [right])
                case None:
                    return 1
        case int():
            match right:
                case list():
                    return compare([left], right)
                case int():
                    if left < right:
                        return -1
                    elif left == right:
                        return 0
                    else:
                        return 1
                case None:
                    return 1
        case None:
            match right:
                case list():
                    return -1
                case int():
                    return -1
                case None:
                    assert False, f"Should never get here, both left and right are None"


def sum_indices_of_pairs_in_correct_order(fn: str) -> int:
    return sum(
        index + 1
        for (index, (left, right)) in enumerate(pairs(fn))
        if compare(left, right) == -1
    )


def part1(fn: str) -> int:
    return sum_indices_of_pairs_in_correct_order(fn)


def part2(fn: str) -> int:
    divider_2: StrangeNumber = [[2]]
    divider_6: StrangeNumber = [[6]]
    sorted_strange_nums: List[StrangeNumber] = sorted(
        [eval(l) for l in file_lines(fn) if l != ""]
        + [
            divider_2,
            divider_6,
        ],
        key=cmp_to_key(compare),
    )
    return (sorted_strange_nums.index(divider_2) + 1) * (
        sorted_strange_nums.index(divider_6) + 1
    )


print(f"Part1 Sample: {part1('day13/sample')}")
print(f"Part1: {part1('day13/input')}")
print(f"Part2 Sample: {part2('day13/sample')}")
print(f"Part2: {part2('day13/input')}")

import math

from utils import file_lines

snafu_digit_to_dec = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}

dec_to_snafu = {v: k for k, v in snafu_digit_to_dec.items()}


def from_snafu(snafu: str) -> int:
    dec = 0
    exp = 1
    for digit in reversed(snafu):
        dec += exp * snafu_digit_to_dec[digit]
        exp *= 5
    return dec


tests = [
    ("1=", 3),
    ("12", 7),
    ("21", 11),
    ("111", 31),
    ("112", 32),
    ("122", 37),
    ("1-12", 107),
    ("2=0=", 198),
    ("2=01", 201),
    ("1=-1=", 353),
    ("12111", 906),
    ("20012", 1257),
    ("1=-0-2", 1747),
]

for (snafu, dec) in tests:
    assert from_snafu(snafu) == dec


def to_snafu(dec: int) -> str:
    def find_lenght(dec: int) -> int:
        exp = 0
        while abs(dec) > 2.5 * math.pow(5, exp):
            exp += 1
        return exp + 1

    def __to_snafu(remaining: int, snafu_so_far: str, remaining_length: int) -> str:
        if remaining_length == 0:
            assert remaining == 0
            return snafu_so_far

        pow = int(math.pow(5, remaining_length - 1))

        if 1.5 * pow < remaining <= 2.5 * pow:
            return __to_snafu(
                remaining - 2 * pow, f"{snafu_so_far}2", remaining_length - 1
            )
        elif 0.5 * pow < remaining <= 1.5 * pow:
            return __to_snafu(remaining - pow, f"{snafu_so_far}1", remaining_length - 1)
        elif -0.5 * pow < remaining <= 0.5 * pow:
            return __to_snafu(remaining, f"{snafu_so_far}0", remaining_length - 1)
        elif -1.5 * pow < remaining <= -0.5 * pow:
            return __to_snafu(remaining + pow, f"{snafu_so_far}-", remaining_length - 1)
        elif -2.5 * pow < remaining <= -1.5 * pow:
            return __to_snafu(
                remaining + 2 * pow, f"{snafu_so_far}=", remaining_length - 1
            )
        else:
            assert False

    return __to_snafu(dec, "", find_lenght(dec))


for (snafu, dec) in tests:
    assert to_snafu(dec) == snafu


def part1(fn: str) -> str:
    return to_snafu(sum(from_snafu(snafu) for snafu in file_lines(fn)))


def part2(fn: str) -> int:
    raise NotImplementedError()


print(f"Part1 Sample: {part1('day25/sample')}")
print(f"Part1: {part1('day25/input')}")
# print(f"Part2 Sample: {part2('day25/sample')}")
# print(f"Part2: {part2('day25/input')}")

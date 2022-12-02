from utils import file_lines


def parsed_lines(fn: str):
    for line in file_lines(fn):
        yield line.split(" ")


def value_of_my_shape(me):
    if me == "X":
        return 1
    elif me == "Y":
        return 2
    elif me == "Z":
        return 3
    else:
        raise Exception(f"Me: {me}")


def outcome_of_round(opponent, me):
    results = {
        "A": {  # Rock
            "X": 3,  # Rock -> Draw
            "Y": 6,  # Paper -> Win
            "Z": 0,  # Scissors -> Lose
        },
        "B": {  # Paper
            "X": 0,
            "Y": 3,
            "Z": 6,
        },
        "C": {  # Scissors
            "X": 6,
            "Y": 0,
            "Z": 3,
        },
    }
    return results[opponent][me]


def score_round(opponent: str, me: str):
    return value_of_my_shape(me) + outcome_of_round(opponent, me)


def part1(fn: str):
    return sum(score_round(opponent, me) for opponent, me in parsed_lines(fn))


print(f"Part2 Sample: {part1('day2/sample')}")
print(f"Part2: {part1('day2/input')}")


def select_shape(opponent: str, outcome: str):
    shape = {
        "A": {  # Rock
            "X": "Z",  # Scissors -> Lose
            "Y": "X",  # Rock -> Draw
            "Z": "Y",  # Paper -> Win
        },
        "B": {  # Paper
            "X": "X",
            "Y": "Y",
            "Z": "Z",
        },
        "C": {  # Scissors
            "X": "Y",
            "Y": "Z",
            "Z": "X",
        },
    }
    return shape[opponent][outcome]


def part2(fn: str):
    return sum(
        score_round(opponent, select_shape(opponent, outcome))
        for opponent, outcome in parsed_lines(fn)
    )


print(f"Part2 Sample: {part2('day2/sample')}")
print(f"Part2: {part2('day2/input')}")

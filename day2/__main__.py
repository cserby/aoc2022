from utils import file_lines

def parsed_lines(fn: str):
    for line in file_lines(fn):
        yield line.split(' ')

def value_of_my_shape(me):
    if me == 'X':
        return 1
    elif me == 'Y':
        return 2
    elif me == 'Z':
        return 3
    else:
        raise Exception(f"Me: {me}")

def outcome_of_round(opponent, me):
    results = {
        'A': {
            'X': 3,
            'Y': 6,
            'Z': 0
        },
        'B': { #Paper
            'X': 0,
            'Y': 3,
            'Z': 6,
        },
        'C': {
            'X': 6,
            'Y': 0,
            'Z': 3,
        }
    }
    return results[opponent][me]

def score_round(opponent: str, me: str):
    return value_of_my_shape(me) + outcome_of_round(opponent, me)

def part1(fn: str):
    return sum(score_round(opponent, me) for opponent, me in parsed_lines(fn))

print(f"Part2 Sample: {part1('day2/sample')}")
print(f"Part2: {part1('day2/input')}")
#print(f"Part2 Sample: {part2('day1/sample')}")
#print(f"Part2: {part2('day1/input')}")
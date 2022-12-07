from utils import file_lines


def start_of_packet_marker_end_index(input: str, packet_length: int = 4):
    for i in range(packet_length - 1, len(input)):
        if len(set(input[i - (packet_length - 1) : i + 1])) == packet_length:
            return i + 1


def part1(file_name: str):
    return [start_of_packet_marker_end_index(input) for input in file_lines(file_name)]


def part2(file_name: str):
    return [
        start_of_packet_marker_end_index(input, packet_length=14)
        for input in file_lines(file_name)
    ]


print(f"Part1 Sample: {part1('day6/sample')}")
print(f"Part1: {part1('day6/input')}")
print(f"Part2 Sample: {part2('day6/sample')}")
print(f"Part2: {part2('day6/input')}")

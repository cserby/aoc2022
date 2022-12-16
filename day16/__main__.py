import math
import re
from dataclasses import dataclass, field
from typing import Dict, Generator, Iterator, List, Optional, Set, Tuple

from utils import file_lines
from utils.matrix import matrix_of_size, matrix_to_str


@dataclass
class Valve:
    id: str
    flow_rate: int
    tunnels_to: List[str]
    on: bool = False


def parse_cave(fn: str) -> Dict[str, Valve]:
    caves: Dict[str, Valve] = {}
    for line in file_lines(fn):
        m = re.search(
            r"^Valve (..) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)$",
            line,
        )
        assert m is not None, f"Failed to parse: {line}"
        valve_id = m.group(1)
        flow_rate = int(m.group(2))
        tunnels_to = [t.strip() for t in m.group(3).split(",")]
        assert valve_id not in caves.keys()
        caves[valve_id] = Valve(valve_id, flow_rate, tunnels_to)
    return caves


def distances(cave: Dict[str, Valve]) -> Dict[str, Dict[str, int]]:
    # https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm

    vertices = list(sorted(cave.keys()))
    dsts = matrix_of_size(len(vertices), len(vertices), math.inf)

    # for each vertex v do
    #    dist[v][v] ← 0
    for i in range(len(vertices)):
        dsts[i][i] = 0

    # for each edge (u, v) do
    #    dist[u][v] ← w(u, v)  // The weight of the edge (u, v)
    for indx, vert in enumerate(vertices):
        for other in cave[vert].tunnels_to:
            dsts[indx][vertices.index(other)] = 1

    # for k from 1 to |V|
    #    for i from 1 to |V|
    #        for j from 1 to |V|
    #            if dist[i][j] > dist[i][k] + dist[k][j]
    #                dist[i][j] ← dist[i][k] + dist[k][j]
    #            end if

    for k in range(len(vertices)):
        for i in range(len(vertices)):
            for j in range(len(vertices)):
                if dsts[i][j] > dsts[i][k] + dsts[k][j]:
                    dsts[i][j] = dsts[i][k] + dsts[k][j]

    return {
        vert: {
            other: int(dsts[vert_idx][other_idx])
            for other_idx, other in enumerate(vertices)
        }
        for (vert_idx, vert) in enumerate(vertices)
    }


def release_from_valve(valve: Valve, time_left: int):
    return valve.flow_rate * time_left if not valve.on else 0


def cost_benefit_of_going_to_X_and_opening_valve(
    curr_pos: str,
    dest_pos: str,
    distances: Dict[str, Dict[str, int]],
    valves: Dict[str, Valve],
    time_left: int,
) -> Tuple[int, int]:  # time it takes and release
    time_it_takes = distances[curr_pos][dest_pos] + 1  # opening the valve
    release = release_from_valve(valves[dest_pos], time_left - time_it_takes)
    return (time_it_takes, release)


def cost_benefit_of_going_to_X_and_opening_valves(
    curr_pos: str,
    distances: Dict[str, Dict[str, int]],
    valves: Dict[str, Valve],
    time_left: int = 30,
):

    return {
        dest_pos: cost_benefit_of_going_to_X_and_opening_valve(
            curr_pos, dest_pos, distances, valves, time_left
        )
        for dest_pos in sorted(valves.keys())
    }


def part1(fn: str) -> int:
    valves = parse_cave(fn)
    dsts = distances(valves)
    print(dsts)

    time_left = 30
    curr_pos = "AA"
    assert curr_pos in valves.keys()

    released = 0

    if valves["AA"].flow_rate > 0:
        # Open valve in AA
        time_left -= 1
        released = release_from_valve(valves["AA"], time_left)
        valves["AA"].on = True

    while time_left > 0:
        print(f"In {curr_pos}, time left: {time_left}")

        benefit_cost = cost_benefit_of_going_to_X_and_opening_valves(
            curr_pos, dsts, valves, time_left
        )
        print(f"Benefit - cost: {benefit_cost}")

        # TODO backtrack!
        next_pos = max(benefit_cost, key=lambda k: benefit_cost.get(k)[1])
        print(f"Max benefit next: {next_pos}")

        # move to next pos
        time_left -= benefit_cost[next_pos][0]
        curr_pos = next_pos

        # open valve in next pos
        valves[next_pos].on = True
        released += benefit_cost[next_pos][1]

    return released


def part2(fn: str) -> int:
    raise NotImplementedError()


print(f"Part1 Sample: {part1('day16/sample')}")
# print(f"Part1: {part1('day16/input')}")
# print(f"Part2 Sample: {part2('day16/sample')}")
# print(f"Part2: {part2('day16/input')}")

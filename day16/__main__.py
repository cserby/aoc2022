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

    return { vert: { other: int(dsts[vert_idx][other_idx]) for other_idx, other in enumerate(vertices) } for (vert_idx, vert) in enumerate(vertices) }


def benefits(cave: Dict[str, Valve], time_left: int = 30):

    return {
        vert: ((time_left - 1) * cave[vert].flow_rate)
        if time_left > 1 and not cave[vert].on
        else 0
        for vert in sorted(cave.keys())
    }


def part1(fn: str) -> int:
    caves = parse_cave(fn)
    dsts = distances(caves)
    print(dsts)

    time_left = 30
    curr_pos = "AA"
    assert curr_pos in caves.keys()

    released = 0

    if caves["AA"].flow_rate > 0:
        # Open valve in AA
        time_left -= 1
        released = benefits(caves)["AA"]
        caves["AA"].on = True

    while time_left > 0:
        print(f"In {curr_pos}, time left: {time_left}")
        bnfts = benefits(caves, time_left)
        print(f"Benefits: {bnfts}")
        costs = dsts[curr_pos]

        benefit_cost = { vert: bc if bc >0 else 0 for vert, bc in { vert: (bnfts[vert] - costs[vert]) for vert in caves.keys() }.items()}
        print(f"Benefit - cost: {benefit_cost}")

        next_pos = max(benefit_cost, key=benefit_cost.get)
        print(f"Max benefit next: {next_pos}")

        # move to next pos
        time_left -= costs[next_pos]
        curr_pos = next_pos

        # open valve in next pos
        caves[next_pos].on = True
        time_left -= 1
        released += bnfts[next_pos]

    return released


def part2(fn: str) -> int:
    raise NotImplementedError()


print(f"Part1 Sample: {part1('day16/sample')}")
print(f"Part1: {part1('day16/input')}")
# print(f"Part2 Sample: {part2('day16/sample')}")
# print(f"Part2: {part2('day16/input')}")

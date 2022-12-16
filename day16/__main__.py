import copy
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


def visit(
    valve: Valve,
    valves: Dict[str, Valve],
    distances: Dict[str, Dict[str, int]],
    released_so_far: int = 0,
    time_left: int = 30,
    indent: int = 0,
) -> int:
#    print(" " * indent + f"{valve.id} IN (time_left = {time_left})")
    new_time_left = time_left
    new_released_so_far = released_so_far

    if valve.flow_rate > 0:
#        print(" " * indent + f"{valve.id} VISIT")
        # open valve
        new_time_left -= 1
        curr_release = release_from_valve(valve, new_time_left)
#        print(
#            " " * indent
#            + f"{valve.id} will release {curr_release} until time runs out in {new_time_left}"
#        )
        new_released_so_far += curr_release
        valve.on = True

    max_release = None
    for new_valve in [
        possible_new_valve
        for possible_new_valve in distances[valve.id].keys()
        if (
            valves[possible_new_valve].flow_rate > 0
            and (not valves[possible_new_valve].on)
            and distances[valve.id][possible_new_valve] + 1 <= new_time_left
        )
    ]:
#        print(
#            " " * indent
#            + f"{valve.id} TRAVERSE TO {new_valve} in {distances[valve.id][new_valve]}"
#        )

        new_valves = copy.deepcopy(valves)
        max_release_if_we_go_this_way = visit(
            new_valves[new_valve],
            new_valves,
            distances,
            0,
            new_time_left - distances[valve.id][new_valve],
            indent + 2,
        )
        if max_release is None or max_release_if_we_go_this_way > max_release:
            max_release = max_release_if_we_go_this_way
    if max_release is not None:
        new_released_so_far += max_release

#    print(" " * indent + f"{valve.id} EXIT ({new_released_so_far})")
    return new_released_so_far


def part1(fn: str) -> int:
    valves = parse_cave(fn)
    dsts = distances(valves)

    #print(dsts)

    return visit(valves["AA"], valves, dsts)


def part2(fn: str) -> int:
    raise NotImplementedError()


print(f"Part1 Sample: {part1('day16/sample')}")
print(f"Part1: {part1('day16/input')}")
# print(f"Part2 Sample: {part2('day16/sample')}")
# print(f"Part2: {part2('day16/input')}")

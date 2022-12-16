import copy
import math
import re
from typing import Dict, List, Tuple

from utils import file_lines
from utils.matrix import matrix_of_size


def parse_cave(fn: str) -> Tuple[Dict[str, int], Dict[str, bool], Dict[str, List[str]]]:
    flow_rate: Dict[str, int] = {}
    valve_on: Dict[str, bool] = {}
    connections: Dict[str, List[str]] = {}

    for line in file_lines(fn):
        m = re.search(
            r"^Valve (..) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)$",
            line,
        )
        assert m is not None, f"Failed to parse: {line}"
        valve_id = m.group(1)
        assert valve_id not in flow_rate.keys()
        assert valve_id not in valve_on.keys()
        assert valve_id not in connections.keys()

        flow_rate[valve_id] = int(m.group(2))
        connections[valve_id] = [t.strip() for t in m.group(3).split(",")]
        valve_on[valve_id] = False

    return (flow_rate, valve_on, connections)


def distances(connections: Dict[str, List[str]]) -> Dict[str, Dict[str, int]]:
    # https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm

    vertices = list(sorted(connections.keys()))
    dsts = matrix_of_size(len(vertices), len(vertices), math.inf)

    # for each vertex v do
    #    dist[v][v] ← 0
    for i in range(len(vertices)):
        dsts[i][i] = 0

    # for each edge (u, v) do
    #    dist[u][v] ← w(u, v)  // The weight of the edge (u, v)
    for indx, vert in enumerate(vertices):
        for other in connections[vert]:
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


def visit(
    position: str,
    flow_rate: Dict[str, int],
    valve_on: Dict[str, bool],
    distances: Dict[str, Dict[str, int]],
    time_left: int = 30,
    indent: int = 0,
) -> int:
    new_time_left = time_left
    released_if_we_take_this_route = 0

    if flow_rate[position] > 0:
        # open valve
        new_time_left -= 1
        assert not valve_on[position]
        curr_release = flow_rate[position] * new_time_left
        released_if_we_take_this_route += curr_release
        valve_on[position] = True

    max_release = None
    for new_position in [
        possible_new_valve
        for possible_new_valve in distances[position].keys()
        if (
            flow_rate[possible_new_valve] > 0
            and (not valve_on[possible_new_valve])
            and distances[position][possible_new_valve] + 1 <= new_time_left
        )
    ]:
        max_release_if_we_go_this_way = visit(
            new_position,
            flow_rate,
            copy.deepcopy(valve_on),
            distances,
            new_time_left - distances[position][new_position],
            indent + 2,
        )
        if max_release is None or max_release_if_we_go_this_way > max_release:
            max_release = max_release_if_we_go_this_way
    if max_release is not None:
        released_if_we_take_this_route += max_release

    return released_if_we_take_this_route


def part1(fn: str) -> int:
    (flow_rate, valve_on, connections) = parse_cave(fn)
    dsts = distances(connections)
    return visit("AA", flow_rate, valve_on, dsts)


def visit2(
    state_1: Tuple[str, int],
    state_2: Tuple[str, int],
    flow_rate: Dict[str, int],
    valve_on: Dict[str, bool],
    distances: Dict[str, Dict[str, int]],
    time_left: int = 26,
    indent: int = 0,
) -> int:
    print(" " * indent + f"-- Minute {26 - time_left + 1} --")
    print(" " * indent + f"Valves {[ k for k,v in valve_on.items() if v]} are open")
    released_if_we_take_this_route = 0

    (pos1, at1) = state_1
    new_at1 = at1
    (pos2, at2) = state_2
    new_at2 = at2

    def step_of_1():
        return time_left == at1

    def step_of_2():
        return time_left == at2

    if step_of_1() and flow_rate[pos1] > 0:
        # 1 open valve
        new_at1 -= 1
        assert not valve_on[pos1]
        curr_release = flow_rate[pos1] * new_at1
        print(" " * indent + f"You open valve {pos1}, will release {curr_release}")
        released_if_we_take_this_route += curr_release
        valve_on[pos1] = True

    if step_of_2() and flow_rate[pos2] > 0:
        # 2 open valve
        new_at2 -= 1
        assert not valve_on[pos2]
        curr_release = flow_rate[pos2] * new_at2
        print(" " * indent + f"Elephant opens valve {pos2}, will release {curr_release}")
        released_if_we_take_this_route += curr_release
        valve_on[pos2] = True

    max_release = None
    for new_pos1 in (
        [
            possible_new_valve
            for possible_new_valve in distances[pos1].keys()
            if (
                flow_rate[possible_new_valve] > 0
                and (not valve_on[possible_new_valve])
                and distances[pos1][possible_new_valve] + 1 <= new_at1
                and possible_new_valve != pos2
            )
        ]
        if step_of_1()
        else [pos1]
    ):
        for new_pos2 in (
            [
                possible_new_valve
                for possible_new_valve in distances[pos2].keys()
                if (
                    flow_rate[possible_new_valve] > 0
                    and (not valve_on[possible_new_valve])
                    and distances[pos2][possible_new_valve] + 1 <= new_at2
                    and possible_new_valve != pos1
                    and possible_new_valve != new_pos1
                )
            ]
            if step_of_2()
            else [pos2]
        ):
            max_release_if_we_go_this_way = visit2(
                (new_pos1, new_at1 - distances[pos1][new_pos1]),
                (new_pos2, new_at2 - distances[pos2][new_pos2]),
                flow_rate,
                copy.deepcopy(valve_on),
                distances,
                max(
                    new_at1 - distances[pos1][new_pos1],
                    new_at2 - distances[pos2][new_pos2],
                ),
                indent + 2,
            )
            if max_release is None or max_release_if_we_go_this_way > max_release:
                max_release = max_release_if_we_go_this_way

    if max_release is not None:
        released_if_we_take_this_route += max_release

    print(" " * indent + f"This option results in a total release of {released_if_we_take_this_route}")
    return released_if_we_take_this_route


def part2(fn: str) -> int:
    (flow_rate, valve_on, connections) = parse_cave(fn)
    dsts = distances(connections)
    return visit2(("AA", 26), ("AA", 26), flow_rate, valve_on, dsts)


#print(f"Part1 Sample: {part1('day16/sample')}")
#print(f"Part1: {part1('day16/input')}")
print(f"Part2 Sample: {part2('day16/sample')}")
#print(f"Part2: {part2('day16/input')}")

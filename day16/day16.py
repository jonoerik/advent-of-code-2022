#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
import re
import itertools
import string

# List of dicts {valve name: (flow rate, dict of tunnels {destination valve: travel cost in minutes}}
InputData = dict[int, tuple[int, dict[int, int]]]


def valve_name_to_id(s: str) -> int:
    assert len(s) == 2
    return len(string.ascii_uppercase) * string.ascii_uppercase.index(s[0]) + string.ascii_uppercase.index(s[1])


def load(input_path: Path) -> InputData:
    valves = {}
    line_regex = re.compile("^Valve (?P<valve>[A-Z]{2}) has flow rate=(?P<flow>[0-9]+); tunnels? leads? to valves? (?P<tunnels>[A-Z]{2}(?:, [A-Z]{2})*)$")
    with open(input_path) as f:
        while line := f.readline():
            re_match = line_regex.fullmatch(line.strip())
            assert re_match is not None
            valves[valve_name_to_id(re_match.group("valve"))] = (int(re_match.group("flow")), {valve_name_to_id(tunnel): 1 for tunnel in re_match.group("tunnels").split(", ")})
    return valves


def released_pressure(input_data: InputData, position: int, opened_valves: list[int], remaining_time: int, memo: dict[tuple[int, frozenset[int], int], int] | None = None) -> int:
    """
    Find the maximum pressure that can be released from `position`, having already opened `opened_valves`,
    with `remaining_time` minutes left.
    Pressure released by opening a valve is calculated when the valve is opened, projected into the future for
    the remaining time.
    """
    if memo is None:
        memo = {}

    if (position, frozenset(opened_valves), remaining_time) in memo:
        return memo[(position, frozenset(opened_valves), remaining_time)]

    if remaining_time <= 0:
        return 0
    # Pressures released by taking different actions this turn.
    options = []
    if position not in opened_valves:
        # Open valve in current room.
        options.append(input_data[position][0] * (remaining_time - 1) + released_pressure(input_data, position, opened_valves + [position], remaining_time - 1, memo))
    for dest in input_data[position][1]:
        options.append(released_pressure(input_data, dest, opened_valves, remaining_time - input_data[position][1][dest], memo))

    p = max(options)
    memo[(position, frozenset(opened_valves), remaining_time)] = p
    return p


def simplify_tunnels(input_data: InputData) -> None:
    """
    Simplify map of tunnels, by removing areas with 0 flow rate valves.
    E.g. (with path costs in <>)
        5 <1> 0 <1> 8
    becomes
        5 <2> 8
    If this leads to multiple connections between a pair of valves, the lowest cost one is retained.
    Tunnel AA, as the starting point, will not be removed.
    """
    to_remove = [valve for valve in input_data if input_data[valve][0] == 0 and valve != valve_name_to_id("AA")]
    while to_remove:
        removed = to_remove.pop()
        for a, b in itertools.permutations(input_data[removed][1], 2):
            cost = input_data[a][1][removed] + input_data[removed][1][b]
            if b in input_data[a][1]:
                cost = min(cost, input_data[a][1][b])
            input_data[a][1][b] = cost
            del input_data[a][1][removed]
        del input_data[removed]


def part1(input_data: InputData) -> int:
    simplify_tunnels(input_data)
    return released_pressure(input_data, valve_name_to_id("AA"), [], 30)


def part2(input_data: InputData) -> int:
    simplify_tunnels(input_data)
    valves = sorted(input_data.keys())
    assert len(valves) <= 32  # Ensure opened_valves bitset will fit in 32bit int
    # Transform valve ids into integers 0 .. n
    input_data = {valves.index(v): (flow, {valves.index(dest): cost for dest, cost in tunnels.items()}) for v, (flow, tunnels) in input_data.items()}

    memo: dict[tuple[int, int, int, int, int, int], int] = {}

    def released_pressure_with_elephant(my_pos: int,
                                        my_time_walking: int,
                                        elephant_pos: int,
                                        elephant_time_walking: int,
                                        opened_valves: int,  # Bitset,
                                        remaining_time: int) -> int:
        """
        Same as released_pressure(), but with an elephant helping.
        time_walking parameters must be 0 for each actor to perform an action. Otherwise, the actor is still walking between valves.
        This is so while actors are walking between valves along tunnels of length >= 2, the other actor can still perform actions.
        Time walking also includes time spent turning a valve.
        """
        nonlocal memo
        nonlocal input_data

        memo_key = (my_pos, my_time_walking, elephant_pos, elephant_time_walking, opened_valves, remaining_time) if \
            (my_pos, my_time_walking) < (elephant_pos, elephant_time_walking) else \
            (elephant_pos, elephant_time_walking, my_pos, my_time_walking, opened_valves, remaining_time)
        if memo_key in memo:
            return memo[memo_key]

        if remaining_time <= 0:
            return 0
        # Pressures released by taking different actions this turn.
        options = []
        match my_time_walking == 0, elephant_time_walking == 0:
            case True, _:
                # I move.
                if not ((1 << my_pos) & opened_valves):
                    t = min(1, elephant_time_walking)
                    rp = input_data[my_pos][0] * (remaining_time - 1)
                    options.append(rp + released_pressure_with_elephant(my_pos, 1 - t, elephant_pos, elephant_time_walking - t, opened_valves | (1 << my_pos), remaining_time - t))
                for dest in input_data[my_pos][1]:
                    t = min(input_data[my_pos][1][dest], elephant_time_walking)
                    options.append(released_pressure_with_elephant(dest, input_data[my_pos][1][dest] - t, elephant_pos, elephant_time_walking - t, opened_valves, remaining_time - t))
            case False, True:
                # Elephant moves.
                if not ((1 << elephant_pos) & opened_valves):
                    t = min(1, my_time_walking)
                    rp = input_data[elephant_pos][0] * (remaining_time - 1)
                    options.append(rp + released_pressure_with_elephant(my_pos, my_time_walking - t, elephant_pos, 1 - t, opened_valves | (1 << elephant_pos), remaining_time - t))
                for dest in input_data[elephant_pos][1]:
                    t = min(input_data[elephant_pos][1][dest], my_time_walking)
                    options.append(released_pressure_with_elephant(my_pos, my_time_walking - t, dest, input_data[elephant_pos][1][dest] - t, opened_valves, remaining_time - t))
            case False, False:
                assert False

        p = max(options)
        memo[memo_key] = p
        return p

    return released_pressure_with_elephant(valves.index(valve_name_to_id("AA")), 0, valves.index(valve_name_to_id("AA")), 0, 0, 26)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-1", "--part1", action="store_true")
    parser.add_argument("-2", "--part2", action="store_true")
    parser.add_argument("input")
    args = parser.parse_args()

    if args.part1 == args.part2:
        sys.exit("Exactly one of --part1 or --part2 must be specified.")

    data = load(Path(args.input))
    if args.part1:
        print(part1(data))
    else:  # part2
        print(part2(data))

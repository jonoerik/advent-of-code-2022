#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
import re
import itertools

# List of dicts {valve name: (flow rate, dict of tunnels {destination valve: travel cost in minutes}}
InputData = dict[str, tuple[int, list[str]]]


def load(input_path: Path) -> InputData:
    valves = {}
    line_regex = re.compile("^Valve (?P<valve>[A-Z]{2}) has flow rate=(?P<flow>[0-9]+); tunnels? leads? to valves? (?P<tunnels>[A-Z]{2}(?:, [A-Z]{2})*)$")
    with open(input_path) as f:
        while line := f.readline():
            match = line_regex.fullmatch(line.strip())
            assert match is not None
            valves[match.group("valve")] = (int(match.group("flow")), {tunnel: 1 for tunnel in match.group("tunnels").split(", ")})
    return valves


def released_pressure(input_data: InputData, position: str, opened_valves: list[str], remaining_time: int, memo: dict[tuple[str, frozenset[str], int], int] = {}) -> int:
    """
    Find the maximum pressure that can be released from `position`, having already opened `opened_valves`,
    with `remaining_time` minutes left.
    Pressure released by opening a valve is calculated when the valve is opened, projected into the future for
    the remaining time.
    """
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
    to_remove = [valve for valve in input_data if input_data[valve][0] == 0 and valve != "AA"]
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
    return released_pressure(input_data, "AA", [], 30)


def part2(input_data: InputData) -> int:
    pass  # TODO


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

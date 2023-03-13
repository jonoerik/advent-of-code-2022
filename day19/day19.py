#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from enum import Enum
import re
import math


class Resource(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


# A list of quantities of each of the 4 resources (or robots for those resources),
#  as 4 16bit integers, packed into a single 64bit int. Least significant bits are ore, then clay, then obsidian,
#  then geodes.
ResourcePile = int
# As only one robot can be built each minute, and we only start with 1 ore robot, we can't reach more than 33 of any
# robot type.
# The cheapest robot recipes use 2 ore. By building ore robots, the maximum ore stockpile that can be reached in 32 steps
# should be around 1 + 1 + 2 + 3 + 4 + ... + 31 == 1 + 496 < 2^16, so this fits in 16bits.

# Dictionary of resource-mining-robot, to the cost of that robot.
# Costs are represented as a dictionary of resource to the quantity of that resource required.
Blueprint = dict[Resource, ResourcePile]
InputData = list[Blueprint]


def make_resource_pile(d: dict[Resource, int]) -> ResourcePile:
    """Convert from 'dict of resources to quantity of each resource' to a ResourcePile"""
    return sum([d[res] << (res.value * 16) for res in d])


def load(input_path: Path) -> InputData:
    blueprints = []
    line_regex = re.compile(
        "^Blueprint (?P<blueprint_no>[0-9]+): "
        "Each ore robot costs (?P<ore_robot_ore_cost>[0-9]+) ore. "
        "Each clay robot costs (?P<clay_robot_ore_cost>[0-9]+) ore. "
        "Each obsidian robot costs (?P<obs_robot_ore_cost>[0-9]+) ore and (?P<obs_robot_clay_cost>[0-9]+) clay. "
        "Each geode robot costs (?P<geo_robot_ore_cost>[0-9]+) ore and (?P<geo_robot_obs_cost>[0-9]+) obsidian.$")

    with open(input_path) as f:
        while line := f.readline():
            re_match = line_regex.fullmatch(line.strip())
            assert re_match is not None
            blueprints.append({
                Resource.ORE: make_resource_pile({Resource.ORE: int(re_match.group("ore_robot_ore_cost"))}),
                Resource.CLAY: make_resource_pile({Resource.ORE: int(re_match.group("clay_robot_ore_cost"))}),
                Resource.OBSIDIAN: make_resource_pile({
                    Resource.ORE: int(re_match.group("obs_robot_ore_cost")),
                    Resource.CLAY: int(re_match.group("obs_robot_clay_cost"))
                }),
                Resource.GEODE: make_resource_pile({
                    Resource.ORE: int(re_match.group("geo_robot_ore_cost")),
                    Resource.OBSIDIAN: int(re_match.group("geo_robot_obs_cost"))
                })
            })

    return blueprints


def max_geodes(bp: Blueprint, time_limit: int) -> int:
    """
    :param bp: Blueprint to use for robot costs.
    :param time_limit: Number of minutes over which to build robots and collect geodes.
    :return: Maximum possible number of geodes that can be produced in time_limit minutes using the selected blueprint.
    """
    def can_build(recipe: ResourcePile, resources: ResourcePile) -> bool:
        for element in Resource:
            if (recipe >> (element.value * 16)) & 0xFFFF > (resources >> (element.value * 16)) & 0xFFFF:
                return False
        return True

    # A potential state in this puzzle;
    # a set of built robots, set of accumulated resources, and a time remaining.
    PuzzleState = tuple[ResourcePile, ResourcePile, int]

    current_best = 0
    highest_lower_bound = 0

    def process_node(robots: ResourcePile, resources: ResourcePile, time_remaining: int) -> list[PuzzleState]:
        nonlocal current_best
        nonlocal highest_lower_bound

        geodes = (resources >> (Resource.GEODE.value * 16)) & 0xFFFF
        geode_robots = (robots >> (Resource.GEODE.value * 16)) & 0xFFFF
        if time_remaining == 0:
            if geodes > current_best:
                current_best = geodes
            if geodes > highest_lower_bound:
                highest_lower_bound = geodes
            return []

        lower_bound = geodes + (time_remaining * geode_robots)
        if lower_bound > highest_lower_bound:
            highest_lower_bound = lower_bound

        # Assume we build 1 geode robot every remaining turn.
        # If 1 turn remains, geodes produced = current geodes + number of geode robots
        # If 2 turns remain, geodes produced = geodes + robots + (robots + 1)
        # For t turns remaining, geodes produced = geodes + t * robots + T(n-1), where T(n) is the nth triangular number
        upper_bound = lower_bound + (((time_remaining - 1) * time_remaining) // 2)
        if upper_bound < highest_lower_bound:
            # Can't beat the minimum guaranteed by a different puzzle state, so give up on this branch.
            return []

        possible_builds = [res for res in Resource if can_build(bp[res], resources)]

        return [(robots + (1 << (possible_build.value * 16)), resources + robots - bp[possible_build], time_remaining - 1)
                for possible_build in possible_builds] + [(robots, resources + robots, time_remaining - 1)]

    # Dict of robots and resources, to the greatest (earliest) time_remaining that has been seen with those resources.
    best_time_remaining: dict[tuple[ResourcePile, ResourcePile], int] = {}
    to_process: set[PuzzleState] = {(1, 0, time_limit)}

    while len(to_process) > 0:
        state = to_process.pop()

        previous_time_remaining = best_time_remaining.get(state[:2], None)
        if previous_time_remaining is not None and previous_time_remaining >= state[2]:
            # We've already seen this state with equal or greater time_remaining.
            # We can't beat the number of geodes mined with >= time, so give up on this state.
            continue

        best_time_remaining[state[:2]] = state[2]
        to_process.update(process_node(*state))

    return current_best


def part1(input_data: InputData) -> int:
    return sum([(i+1) * max_geodes(bp, 24) for i, bp in enumerate(input_data)])


def part2(input_data: InputData) -> int:
    return math.prod([max_geodes(bp, 32) for bp in input_data[:3]])


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

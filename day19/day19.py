#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from enum import Enum
import re


class Resource(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


# A list of quantities of each of the 4 resources (or robots for those resources),
#  as 4 16bit integers, packed into a single 64bit int. Least significant bits are ore, then clay, then obsidian,
#  then geodes.
ResourcePile = int
# As only one robot can be built each minute, and we only start with 1 ore robot, we can't reach more than 25 of any
# robot type.
# The cheapest robot recipes use 2 ore. By building ore robots, the maximum ore stockpile that can be reached in 24 days
# should be around 1 + 1 + 2 + 3 + 4 + ... + 23 == 1 + 276 < 2^16, so this fits in 16bits.

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


def max_geodes(bp: Blueprint) -> int:
    """
    :param bp: Blueprint to use for robot costs.
    :return: Maximum possible number of geodes that can be produced in 24 minutes using the selected blueprint.
    """
    def can_build(recipe: ResourcePile, resources: ResourcePile) -> bool:
        for element in Resource:
            if (recipe >> (element.value * 16)) & 0xFFFF > (resources >> (element.value * 16)) & 0xFFFF:
                return False
        return True

    # A potential state in this puzzle;
    # a set of built robots, set of accumulated resources, and a time remaining.
    PuzzleState = tuple[ResourcePile, ResourcePile, int]

    processed: set[PuzzleState] = set()
    to_process: set[PuzzleState] = {(1, 0, 24)}
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
        upper_bound = geodes + (time_remaining * geode_robots) + (((time_remaining - 1) * time_remaining) // 2)
        if upper_bound < highest_lower_bound:
            # Can't beat the minimum guaranteed by a different puzzle state, so give up on this branch.
            return []

        possible_builds = [res for res in Resource if can_build(bp[res], resources)]

        return [(robots + (1 << (possible_build.value * 16)), resources + robots - bp[possible_build], time_remaining - 1)
                for possible_build in possible_builds] + [(robots, resources + robots, time_remaining - 1)]

    while len(to_process) > 0:
        state = to_process.pop()
        if state not in processed:
            processed.add(state)
            to_process.update(process_node(*state))

    return current_best


def part1(input_data: InputData) -> int:
    return sum([(i+1) * max_geodes(bp) for i, bp in enumerate(input_data)])


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

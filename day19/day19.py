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


# Dictionary of resource-mining-robot, to the cost of that robot.
# Costs are represented as a dictionary of resource to the quantity of that resource required.
Blueprint = dict[Resource, dict[Resource, int]]
InputData = list[Blueprint]


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
                Resource.ORE: {Resource.ORE: int(re_match.group("ore_robot_ore_cost"))},
                Resource.CLAY: {Resource.ORE: int(re_match.group("clay_robot_ore_cost"))},
                Resource.OBSIDIAN: {
                    Resource.ORE: int(re_match.group("obs_robot_ore_cost")),
                    Resource.CLAY: int(re_match.group("obs_robot_clay_cost"))
                },
                Resource.GEODE: {
                    Resource.ORE: int(re_match.group("geo_robot_ore_cost")),
                    Resource.OBSIDIAN: int(re_match.group("geo_robot_obs_cost"))
                }
            })

    return blueprints


def max_geodes(bp: Blueprint) -> int:
    """
    :param bp: Blueprint to use for robot costs.
    :return: Maximum possible number of geodes that can be produced in 24 minutes using the selected blueprint.
    """
    def can_build(recipe: dict[Resource, int], resources: dict[Resource, int]) -> bool:
        for element in recipe:
            if recipe[element] > resources[element]:
                return False
        return True

    def max_geodes_int(robots: dict[Resource, int], resources: dict[Resource, int], time_remaining: int) -> int:
        if time_remaining == 0:
            return resources[Resource.GEODE]

        possible_builds = [res for res in Resource if can_build(bp[res], resources)]
        possible_builds += [None]

        return max([max_geodes_int(
                {res: robots[res] + (1 if res == possible_build else 0) for res in Resource},
                {res: resources[res] + robots[res] for res in Resource},
                time_remaining - 1)
            for possible_build in possible_builds])

    return max_geodes_int({i: 1 if i == Resource.ORE else 0 for i in Resource}, {i: 0 for i in Resource}, 24)


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

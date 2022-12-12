#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
import string

# map of elevations, start_pos (row, col), goal_pos (row, col)
InputData = tuple[list[list[int]], tuple[int, int], tuple[int, int]]


def load(input_path: Path) -> InputData:
    start = None
    goal = None
    heightmap = []

    def point_height(c: str, row: int, col: int):
        if c == "S":
            nonlocal start
            start = (row, col)
            c = "a"
        elif c == "E":
            nonlocal goal
            goal = (row, col)
            c = "z"
        return string.ascii_lowercase.index(c)

    with open(input_path) as f:
        r = 0
        while line := f.readline():
            heightmap.append([point_height(c, r, i) for i, c in enumerate(line.strip())])
            r += 1

    return heightmap, start, goal


def part1(input_data: InputData) -> int:
    heightmap, start, goal = input_data
    distance = [[None for col in range(len(heightmap[0]))] for row in range(len(heightmap))]

    # dict of (position: tentative distance)
    next_nodes = {start: 0}
    while distance[goal[0]][goal[1]] is None:
        current, current_dist = sorted(next_nodes.items(), key=lambda x: x[1])[0]
        del next_nodes[current]
        distance[current[0]][current[1]] = current_dist

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_r = current[0] + dr
            next_c = current[1] + dc
            # If destination is within heightmap bounds, unvisited, and can be moved to from the current position
            if 0 <= next_r < len(heightmap) and 0 <= next_c < len(heightmap[0]) and \
                    distance[next_r][next_c] is None and \
                    heightmap[next_r][next_c] <= heightmap[current[0]][current[1]] + 1:
                next_pos = (next_r, next_c)
                if next_pos in next_nodes:
                    next_nodes[next_pos] = min(current_dist + 1, next_nodes[next_pos])
                else:
                    next_nodes[next_pos] = current_dist + 1

    return distance[goal[0]][goal[1]]


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

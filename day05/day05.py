#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

StartingStacks = list[list[str]]
Moves = list[tuple[int, int, int]]
InputData = tuple[StartingStacks, Moves]


def load(input_path: Path) -> InputData:
    starting_stacks = []
    moves = []
    with open(input_path) as f:
        while True:
            line = f.readline()[:-1]  # Remove newline.
            if not line.strip().startswith("["):
                # This should be the stack numbers line (1 2 3...).
                # Also skip the blank line.
                f.readline()
                break
            for _ in range(len(starting_stacks), (len(line) + 1) // 4):
                starting_stacks.append([])
            for i in range((len(line) + 1) // 4):
                if (c := line[i * 4 + 1]) != " ":
                    starting_stacks[i].append(c)
        starting_stacks = [list(reversed(l)) for l in starting_stacks]

        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip().split(" ")
            moves.append((int(line[1]), int(line[3]) - 1, int(line[5]) - 1))
    return starting_stacks, moves


def part1(input_data: InputData) -> str:
    stacks, moves = input_data
    for count, s_from, s_to in moves:
        assert s_from != s_to
        stacks[s_to].extend(reversed(stacks[s_from][-count:]))
        stacks[s_from] = stacks[s_from][:-count]
    return "".join([l[-1] for l in stacks])


def part2(input_data: InputData) -> str:
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

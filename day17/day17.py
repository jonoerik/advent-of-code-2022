#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
import typing

# -1: Left, 1: Right
InputData = list[int]


def load(input_path: Path) -> InputData:
    with open(input_path) as f:
        return [{"<": -1, ">": 1}[c] for c in f.readline().strip()]


def gust_generator(input_data) -> typing.Generator[int, None, None]:
    while True:
        for x in input_data:
            yield x


rock_shapes_str = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
""".strip()
# Rock rows are upside down, to match bottom-left origin of chamber.
rock_shapes = [list(reversed([[{"#": True, ".": False}[c] for c in line] for line in rock.split("\n")]))
               for rock in rock_shapes_str.split("\n\n")]


def rock_generator() -> typing.Generator[list[list[bool]], None, None]:
    while True:
        for rock in rock_shapes:
            yield rock


def part1(input_data: InputData) -> int:
    gusts = gust_generator(input_data)
    rocks = rock_generator()
    # Chamber origin in bottom-left corner, so it can grow upwards.
    chamber = [[True for _ in range(9)]] + [[True] + [False for _ in range(7)] + [True] for _ in range(7)]

    def rows_free():
        i = 0
        for row in reversed(chamber):
            if row != [True] + [False for _ in range(7)] + [True]:
                return i
            i += 1

    for _ in range(2022):
        # Add extra height to chamber, for next rock.
        chamber.extend([[True] + [False for _ in range(7)] + [True] for _ in range(7 - rows_free())])

        rock = next(rocks)
        # Position of bottom-left corner of rock.
        rock_pos = (3, len(chamber) - 4)

        def rock_obstructed(dx: int, dy: int) -> bool:
            new_pos = (rock_pos[0] + dx, rock_pos[1] + dy)
            for y in range(len(rock)):
                for x in range(len(rock[0])):
                    if rock[y][x] and chamber[new_pos[1] + y][new_pos[0] + x]:
                        return True
            return False

        def stop_rock() -> None:
            for y in range(len(rock)):
                for x in range(len(rock[0])):
                    if rock[y][x]:
                        assert not chamber[rock_pos[1] + y][rock_pos[0] + x]
                        chamber[rock_pos[1] + y][rock_pos[0] + x] = True

        while True:  # i.e. until rock stops against an obstruction.
            gust = next(gusts)
            if not rock_obstructed(gust, 0):
                rock_pos = (rock_pos[0] + gust, rock_pos[1])
            if rock_obstructed(0, -1):
                stop_rock()
                break
            else:
                rock_pos = (rock_pos[0], rock_pos[1] - 1)

    return len(chamber) - rows_free() - 1


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

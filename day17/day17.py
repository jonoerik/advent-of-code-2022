#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
import typing
from collections import deque

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
max_rock_height = max([len(rock) for rock in rock_shapes])


def rock_generator() -> typing.Generator[list[list[bool]], None, None]:
    while True:
        for rock in rock_shapes:
            yield rock


chamber_width = 7


def fill_cavity(chamber: deque[int]) -> deque[int]:
    """
    Fill in inaccessible cavities in chamber.
    """
    height = len(chamber)
    # Cells not accessible from the top, or filled.
    inaccessible = deque([(1 << chamber_width) - 1 for _ in range(height)])

    def fill(r: int, c: int) -> None:
        nonlocal inaccessible
        if not (chamber[r] & (1 << c)) and (inaccessible[r] & (1 << c)):
            inaccessible[r] &= ~(1 << c)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if 0 <= r + dr < height and 0 <= c + dc < chamber_width:
                    fill(r + dr, c + dc)

    for i in range(chamber_width):
        fill(len(inaccessible) - 1, i)
    return inaccessible


def tower_height(input_data: InputData, rock_count: int) -> int:
    gusts = gust_generator(input_data)
    rocks = rock_generator()
    # Chamber origin in bottom-left corner, so it can grow upwards.
    chamber = deque()
    rows_removed = 0

    def rows_free() -> int:
        i = 0
        for row in reversed(chamber):
            if row != 0x0:
                return i
            i += 1
        return i

    for _ in range(rock_count):
        # Add extra height to chamber, for next rock.
        chamber.extend([0x0 for _ in range(3 + max_rock_height - rows_free())])
        # Remove completely covered layers at bottom.
        while chamber[0] == (1 << chamber_width) - 1:
            chamber.popleft()
            rows_removed += 1

        rock = next(rocks)
        # Position of bottom-left corner of rock.
        rock_pos = (2, len(chamber) - max_rock_height)

        def rock_obstructed(dx: int, dy: int) -> bool:
            if rock_pos[0] + dx < 0 or \
                    rock_pos[0] + dx + len(rock[0]) > chamber_width or \
                    rock_pos[1] + dy < 0 or \
                    rock_pos[1] + dy + len(rock) > len(chamber):
                return True
            for y in range(len(rock)):
                for x in range(len(rock[0])):
                    if rock[y][x] and (chamber[rock_pos[1] + dy + y] & (1 << (rock_pos[0] + dx + x))):
                        return True
            return False

        def stop_rock() -> None:
            nonlocal chamber
            nonlocal rows_removed
            for y in range(len(rock)):
                for x in range(len(rock[0])):
                    if rock[y][x]:
                        assert not chamber[rock_pos[1] + y] & (1 << (rock_pos[0] + x))
                        chamber[rock_pos[1] + y] |= (1 << (rock_pos[0] + x))
            chamber = fill_cavity(chamber)

        while True:  # i.e. until rock stops against an obstruction.
            gust = next(gusts)
            if not rock_obstructed(gust, 0):
                rock_pos = (rock_pos[0] + gust, rock_pos[1])
            if rock_obstructed(0, -1):
                stop_rock()
                break
            else:
                rock_pos = (rock_pos[0], rock_pos[1] - 1)

    return len(chamber) - rows_free() + rows_removed


def part1(input_data: InputData) -> int:
    return tower_height(input_data, 2022)


def part2(input_data: InputData) -> int:
    return tower_height(input_data, 1000000000000)


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

#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

# List of moves (dx, dy, dist)
# +ve x is right, +ve y is up
InputData = list[tuple[int, int, int]]


def load(input_path: Path) -> InputData:
    moves: InputData = []
    with open(input_path) as f:
        while line := f.readline().strip():
            line = line.split(" ")
            moves.append({"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}[line[0]] + (int(line[1]),))
    return moves


def moved_tail(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    if abs(dx) <= 1 and abs(dy) <= 1:
        return tail
    dx = min(1, max(-1, dx))
    dy = min(1, max(-1, dy))
    return (tail[0] + dx, tail[1] + dy)


def part1(input_data: InputData) -> int:
    head = (0, 0)
    tail = (0, 0)
    tail_visited = {tail}
    for dx, dy, dist in input_data:
        for _ in range(dist):
            head = (head[0] + dx, head[1] + dy)
            tail = moved_tail(head, tail)
            tail_visited.add(tail)
    return len(tail_visited)


def part2(input_data: InputData) -> int:
    knots = [(0, 0) for _ in range(10)]
    tail_visited = {knots[-1]}
    for dx, dy, dist in input_data:
        for _ in range(dist):
            knots[0] = (knots[0][0] + dx, knots[0][1] + dy)
            for i in range(1, len(knots)):
                knots[i] = moved_tail(knots[i-1], knots[i])
            tail_visited.add(knots[-1])
    return len(tail_visited)


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

#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from enum import Enum


class Move(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


class Outcome(Enum):
    Loss = 0
    Draw = 3
    Win = 6


def load(input_path: Path) -> list[tuple[Move, Move]]:
    moves = []
    with open(input_path) as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip().split(" ")
            moves.append(({"A": Move.Rock, "B": Move.Paper, "C": Move.Scissors}[line[0]],
                          {"X": Move.Rock, "Y": Move.Paper, "Z": Move.Scissors}[line[1]]))
    return moves


def match_outcome(opponent: Move, own: Move) -> Outcome:
    if opponent == own:
        return Outcome.Draw
    elif {Move.Rock: Move.Paper, Move.Paper: Move.Scissors, Move.Scissors: Move.Rock}[opponent] == own:
        return Outcome.Win
    else:
        return Outcome.Loss


def score(move: tuple[Move, Move]) -> int:
    return {Move.Rock: 1, Move.Paper: 2, Move.Scissors: 3}[move[1]] + match_outcome(move[0], move[1]).value


def part1(moves: list[list[int]]) -> int:
    return sum([score(m) for m in moves])


def part2(moves: list[list[int]]) -> int:
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

#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from enum import Enum
from PIL import Image
import pytesseract


class Opcode(Enum):
    noop = 0
    addx = 1


# List of instructions (opcode, operand)
InputData = list[tuple[Opcode, int]]


def load(input_path: Path) -> InputData:
    instructions = []
    with open(input_path) as f:
        while line := f.readline().strip():
            line = line.split()
            op = Opcode[line[0]]
            if op == Opcode.addx:
                x = int(line[1])
            else:
                x = None
            instructions.append((op, x))
    return instructions


def part1(input_data: InputData) -> int:
    # Convert to 1-cycle-per-instruction format
    instructions = []
    for i in input_data:
        if i[0] == Opcode.addx:
            instructions.append((Opcode.noop, None))
        instructions.append(i)
    checked_cycles = range(20, 20+40*6, 40)
    x = 1
    sig_strength_sum = 0
    for i in range(1, max(checked_cycles) + 1):
        if i in checked_cycles:
            sig_strength_sum += i * x
        if instructions[i-1][0] == Opcode.addx:
            x += instructions[i-1][1]
    return sig_strength_sum


def part2(input_data: InputData) -> str:
    # Convert to 1-cycle-per-instruction format
    instructions = []
    for i in input_data:
        if i[0] == Opcode.addx:
            instructions.append((Opcode.noop, None))
        instructions.append(i)
    x = 1
    width = 40
    height = 6
    video_buffer = [[False for col in range(width)] for row in range(height)]

    for i in range(width * height):
        op, operand = instructions[i]
        beam_pos = i % width
        video_buffer[i // width][i % width] = (abs(beam_pos - x) <= 1)
        if op == Opcode.addx:
            x += operand

    # Use Tesseract OCR to convert video buffer to a string
    border = 1
    img = Image.new("1", (width + border * 2, height + border * 2), 1)
    for row in range(height):
        for col in range(width):
            if video_buffer[row][col]:
                img.putpixel((col + border, row + border), 0)
    return pytesseract.image_to_string(img, lang="eng", config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8").strip()


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

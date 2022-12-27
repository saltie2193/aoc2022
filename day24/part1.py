"""
Day 24: Blizzard Basin - Part 1
https://adventofcode.com/2022/day/24
"""
from __future__ import annotations

import math
import operator
import os
from collections import defaultdict, deque

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")

Position = tuple[int, int]  # row, column
Blizzards = defaultdict[Position, list[str]]  # (row, column) -> [direction, ...]
Weather = defaultdict[
    tuple[int, int, int], list[str]
]  # (cycle, row, column) -> [direction, ...]

RIGHT, DOWN, LEFT, UP = ">", "v", "<", "^"
EMPTY, SOLID = ".", "#"
DIRECTION_MAP = {RIGHT: (0, 1), DOWN: (1, 0), LEFT: (0, -1), UP: (0, -1)}


def print_board(
    position: Position, blizzards: Blizzards, maxs: tuple[int, int]
) -> None:
    for i in range(maxs[0] + 1):
        row = []
        for j in range(maxs[1] + 1):
            if (i, j) == position:
                row.append("E")
                continue

            blizzs = blizzards[(i, j)]
            if len(blizzs) == 0:
                row.append(EMPTY)
            elif len(blizzs) == 1:
                row.append(blizzs[0])
            else:
                row.append(str(len(blizzs)))

        print("".join(row))


def parse(input_str: str) -> tuple[Position, Position, Blizzards, Position]:
    lines = input_str.splitlines()

    maxs = len(lines) - 1, len(lines[0]) - 1
    start = (int(0), lines[0].find("."))
    end = (maxs[0], lines[-1].find("."))
    blizzards = defaultdict(list)
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c in (RIGHT, DOWN, LEFT, UP, SOLID):
                blizzards[(i, j)].append(c)

    return start, end, blizzards, maxs


def _move(direction: str, position: Position) -> Position:
    row, col = position
    if direction == RIGHT:
        return row, col + 1
    if direction == DOWN:
        return row + 1, col
    if direction == LEFT:
        return row, col - 1
    if direction == UP:
        return row - 1, col
    if direction == SOLID:
        return position
    raise ValueError(f"Unknown direction '{direction}'")


def move_blizzard(
    position: Position, direction: str, max_row: int, max_col
) -> Position:
    if direction == SOLID:
        return position
    row, col = _move(direction, tuple(position))
    if col >= max_col:
        col = 1
    elif col <= 0:
        col = max_col - 1

    if row >= max_row:
        row = 1
    elif row <= 0:
        row = max_row - 1

    return row, col


def update_blizzards(blizzards: Blizzards, max_row: int, max_col: int) -> Blizzards:
    new_blizzards: Blizzards = defaultdict(list)
    for position, directions in blizzards.items():
        for direction in directions:
            new_blizzards[move_blizzard(position, direction, max_row, max_col)].append(
                direction
            )
    return new_blizzards


def predict_weather_n(_initial: Blizzards, maxs: tuple[int, int]) -> Weather:
    max_row, max_col = maxs
    magic = (max_row - 1) * (max_col - 1)

    weather: Weather = defaultdict(list)
    updated = _initial
    for i in range(magic):
        weather.update({(i, *k): v for k, v in updated.items()})
        updated = update_blizzards(updated, max_row, max_col)

    return weather


def find_path_length(
    position: Position,
    target: Position,
    weather: Weather,
    cycle_length: int,
    time_offset=0,
) -> int:
    max_row = max(blizzard[1] for blizzard in weather)
    max_col = max(blizzard[2] for blizzard in weather)
    to_visit: deque[tuple[int, Position]] = deque()
    to_visit.append((0, position))
    visited: set[tuple[int, int, int]] = set()
    while to_visit:
        length, _position = to_visit.popleft()
        if _position == target:
            return length

        # visited.add(((time_offset + length) % cycle_length, _position[0], _position[1]))

        # get possible moves
        for direction in (0, 1), (1, 0), (0, 0), (0, -1), (-1, 0):
            new_position: tuple[int, int] = tuple(
                map(operator.add, _position, direction)
            )
            # tuple(p + o for p, o in zip(_position, direction))
            # new_position = _move(direction, _position)

            # blizzard at position
            new_time_state = (
                ((time_offset + length + 1) % cycle_length),
                *new_position,
            )
            if new_time_state in weather:
                continue

            if new_position[0] < 0 or new_position[0] > max_row:
                continue

            if new_time_state in visited:
                continue

            to_visit.append((length + 1, new_position))
            visited.add(new_time_state)

    return math.inf


def compute(input_str: str) -> str:
    start, end, blizzards, maxs = parse(input_str)

    magic = math.lcm((maxs[0] - 1), (maxs[1] - 1))
    print("predicting weather")
    weather = predict_weather_n(blizzards, maxs)

    print("start solving")
    res = find_path_length(start, end, weather, magic)
    return str(res)


def test_move_blizzard() -> None:
    blizzards = [(RIGHT, 2, 1), (DOWN, 4, 4), (LEFT, 1, 1), (RIGHT, 2, 5)]
    outs = [(2, 2), (5, 4), (1, 5), (2, 1)]

    for (direction, *pos), out in zip(blizzards, outs):
        assert move_blizzard(pos, direction, 6, 6) == out


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "18"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part)


if __name__ == "__main__":
    main()

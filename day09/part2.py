from __future__ import annotations

import os

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def grid_to_str(rope: list[tuple[int, int]], visited: set[tuple[int, int]]) -> str:
    upper, right, lower, left = 0, 0, 0, 0
    for row, col in [*rope, *visited]:
        if row > upper:
            upper = row
        elif row < lower:
            lower = row

        if col > right:
            right = col
        elif col < left:
            left = col

    offset_row = abs(lower)
    offset_col = abs(left)

    lines: list[list[str]] = []
    for row in range(lower, upper + 1):
        lines.append([])
        for col in range(left, right + 1):
            if (row, col) in visited:
                lines[row + offset_row].append("#")
            else:
                lines[row + offset_row].append(".")

    lines[offset_row][offset_col] = "S"

    for i, (row, col) in enumerate(reversed(rope)):
        v = len(rope) - i - 1
        lines[row + offset_row][col + offset_col] = str(v) if v != 0 else "H"

    return "\n".join("".join(line) for line in lines)


def parse(input_str: str) -> list[tuple[str, int]]:
    return [(a, int(b)) for a, b in [line.split() for line in input_str.splitlines()]]


def move_tail(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    dist = (head[0] - tail[0], head[1] - tail[1])

    # close enough no move
    if dist[0] in (-1, 0, 1) and dist[1] in (-1, 0, 1):
        return tail

    # move
    d0 = min(max(dist[0], -1), 1)
    d1 = min(max(dist[1], -1), 1)
    return (tail[0] + d0, tail[1] + d1)


def move_rope(action: str, rope: list[tuple[int, int]]) -> list[tuple[int, int]]:
    head = rope[0]
    if action == "R":
        rope[0] = (head[0], head[1] + 1)
    elif action == "U":
        rope[0] = (head[0] + 1, head[1])
    elif action == "L":
        rope[0] = (head[0], head[1] - 1)
    elif action == "D":
        rope[0] = (head[0] - 1, head[1])
    else:
        raise ValueError(f"unknown action {action}")

    for i, part in enumerate(rope[1:], 1):
        rope[i] = move_tail(rope[i - 1], part)

    return rope


def compute(input_str: str) -> str:
    moves = parse(input_str)
    rope = [(0, 0) for _ in range(10)]
    visited: set[tuple[int, int]] = set()

    for action, distance in moves:
        while distance > 0:
            rope = move_rope(action, rope)
            visited.add(rope[-1])
            distance -= 1

    return str(len(visited))


def test_move_tail_no_move() -> None:
    cords = [(r, c) for r in range(-1, 2) for c in range(-1, 2)]
    ins = [
        (a, b)
        for a in cords
        for b in cords
        if abs(a[0] - b[0]) < 2 and abs(a[1] - b[1]) < 2
    ]

    for head, tail in ins:
        assert move_tail(head, tail) == tail


def test_move_tail_simple() -> None:
    ins = [
        ((2, 0), (0, 0)),
        ((0, 2), (0, 0)),
        ((-2, 0), (0, 0)),
        ((0, -2), (0, 0)),
    ]
    outs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for (head, tail), out in zip(ins, outs):
        assert move_tail(head, tail) == out


def test_move_tail_diag() -> None:
    ins = [
        ((2, 1), (0, 0)),
        ((1, 2), (0, 0)),
        ((-2, -1), (0, 0)),
        ((1, -2), (0, 0)),
        ((2, -1), (0, 0)),
        ((-2, 1), (0, 0)),
        ((-1, 2), (0, 0)),
        ((1, -2), (0, 0)),
    ]
    outs = [(1, 1), (1, 1), (-1, -1), (1, -1), (1, -1), (-1, 1), (-1, 1), (1, -1)]

    for (head, tail), out in zip(ins, outs):
        assert move_tail(head, tail) == out


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "1"


def test_long() -> None:
    input_s = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
    assert compute(input_s) == "36"


def main():
    API_TOKEN = ""
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()

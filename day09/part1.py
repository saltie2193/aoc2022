from __future__ import annotations

import os

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def grid_to_str(grid: list[list[int]]) -> str:
    return "\n".join("".join(str(i) for i in row) for row in grid)


def parse(input_str: str) -> list[tuple[str, int]]:
    return [(a, int(b)) for a, b in [line.split() for line in input_str.splitlines()]]


def move_tail(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    dist = (head[0] - tail[0], head[1] - tail[1])

    # close enough no move
    if dist[0] in (-1, 0, 1) and dist[1] in (-1, 0, 1):
        return tail

    # in same row or column, move closer to head
    if dist[0] == 0 or dist[1] == 0:
        d0 = min(max(dist[0], -1), 1)
        d1 = min(max(dist[1], -1), 1)
        return (tail[0] + d0, tail[1] + d1)

    # move diagonally?
    d0 = min(max(dist[0], -1), 1)
    d1 = min(max(dist[1], -1), 1)
    return (tail[0] + d0, tail[1] + d1)


def move_rope(
    action: str, rope: tuple[tuple[int, int], tuple[int, int]]
) -> tuple[tuple[int, int], tuple[int, int]]:
    head, tail = rope
    if action == "R":
        head = (head[0], head[1] + 1)
    elif action == "U":
        head = (head[0] + 1, head[1])
    elif action == "L":
        head = (head[0], head[1] - 1)
    elif action == "D":
        head = (head[0] - 1, head[1])
    else:
        raise ValueError(f"unknown action {action}")

    tail = move_tail(head, tail)

    return (head, tail)


def compute(input_str: str) -> str:
    moves = parse(input_str)
    print(moves)
    rope = ((0, 0), (0, 0))
    visited: set[tuple[int, int]] = set()

    for action, distance in moves:
        while distance > 0:
            rope = move_rope(action, rope)
            visited.add(rope[1])
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
    input_s = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
    assert compute(input_s) == "13"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part)


if __name__ == "__main__":
    main()

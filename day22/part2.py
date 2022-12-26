from __future__ import annotations

import os

import pytest
from aoc import AOC
from dotenv import load_dotenv

from day22.part1 import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Actions,
    Position,
    Solids,
    parse_actions, parse_map, turn,
)

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")

Terrain = tuple[list[range], list[range], Solids]

JUMP_MAP = {
    **{
        (LEFT, 0 + row, 50): (RIGHT, 149 - row, 0) for row in range(50)
    },  # move left on upper left edge
    **{
        (RIGHT, 0 + row, 149): (LEFT, 149 - row, 99) for row in range(50)
    },  # move right on upper right edge
    **{
        (LEFT, 50 + row, 50): (DOWN, 100, 0 + row) for row in range(50)
    },  # move left on upper middle left edge
    **{
        (RIGHT, 50 + row, 99): (UP, 49, 100 + row) for row in range(50)
    },  # move right on upper middle right edge
    **{
        (LEFT, 150 + row, 0): (DOWN, 0, 50 + row) for row in range(50)
    },  # move left on lower left edge
    **{
        (RIGHT, 150 + row, 49): (UP, 149, 50 + row) for row in range(50)
    },  # move right on lower right edge
    **{
        (DOWN, 199, 0 + col): (DOWN, 0, 100 + col) for col in range(50)
    },  # move down on left lower edge -> down right upper edge
}

test_jump_map = {
    **{
        (LEFT, 0 + row, 8): (DOWN, 4, 4 + row) for row in range(4)
    },  # move left on upper left edge
    **{
        (RIGHT, 0 + row, 11): (DOWN, 8 + row, 15) for row in range(4)
    },  # move right on upper right edge
    **{
        (LEFT, 4 + row, 0): (LEFT, 11, 12 + row) for row in range(4)
    },  # move left on middle left edge
    **{
        (RIGHT, 4 + row, 11): (DOWN, 8, 15 - row) for row in range(4)
    },  # move right on middle right edge
    **{
        (LEFT, 8 + row, 8): (UP, 7, 7 - row) for row in range(4)
    },  # move left on left lower edge
    **{
        (RIGHT, 8 + row, 7): (LEFT, 3 - row, 11) for row in range(4)
    },  # move right on right lower edge
    **{
        (DOWN, 7, 0 + col): (UP, 11, 11 - col) for col in range(4)
    },  # move down on left lower edge
}

# JUMP_MAP = test_jump_map
JUMP_MAP = {
    **{
        ((v[0] + 2) % 4, v[1], v[2]): ((k[0] + 2) % 4, k[1], k[2])
        for k, v in JUMP_MAP.items()
    },
    **JUMP_MAP,
}


def _parse_map(map_str: str) -> Terrain:
    rows, solids = parse_map(map_str)

    max_j = max(map(lambda a: a.stop, rows))
    cols: list[list[None | int]] = [[None, None] for _ in range(max_j)]

    for i, row in enumerate(rows):
        for j in row:
            cols[j][1] = i
            if cols[j][0] is not None:
                continue
            cols[j][0] = i

    return rows, [range(i, j + 1) for i, j in cols], solids


def parse(input_str: str) -> tuple[Terrain, Actions]:
    map_str, actions_str = input_str.split("\n\n")
    return _parse_map(map_str), parse_actions(actions_str)


def move_up_down(position: Position, distance: int, terrain: Terrain) -> Position:
    if distance == 0:
        return position

    facing, row, col = position
    if facing not in (UP, DOWN):
        raise AttributeError(f"Unsupported direction '{facing}'")

    offset = 1 if facing == DOWN else -1
    _, cols, solids = terrain
    i, j = row + offset, col
    # print(i, j, cols[j])
    if i not in cols[j]:
        jump = JUMP_MAP.get(position)
        # print(f"jump: {pos} -> {jump}")
        facing, i, j = jump

    if (i, j) in solids:
        return position

    return move((facing, i, j), distance - 1, terrain)


def move_left_right(position: Position, distance: int, terrain: Terrain) -> Position:
    if distance == 0:
        return position

    facing, row, col = position
    if facing not in (RIGHT, LEFT):
        raise ValueError(f"Unsupported direction {facing}")

    offset = 1 if facing == RIGHT else -1
    i, j = row, col + offset

    rows, _, solid = terrain
    if j not in rows[i]:
        jump = JUMP_MAP.get(position)
        print(f"jump: {position} -> {jump}")
        facing, i, j = jump

    if (i, j) in terrain[2]:
        return position
    return move((facing, i, j), distance - 1, terrain)


def move(position: Position, distance: int, terrain: Terrain) -> Position:
    # print(f"move {distance}")
    direction = position[0]
    if direction in (RIGHT, LEFT):  # right, left
        return move_left_right(position, distance, terrain)
    if direction in (DOWN, UP):  # down, up
        return move_up_down(position, distance, terrain)
    raise ValueError(f"Unknown direction '{direction}'")


def apply_action(position: Position, action: str | int, terrain: Terrain) -> Position:
    if action in ("L", "R"):
        return turn(position, action)

    if type(action) is not int:
        raise TypeError(f"Unsupported action {action} of type {type(action)}")

    return move(position, action, terrain)


def compute(input_str: str) -> str:
    terrain, actions = parse(input_str)
    pos = (RIGHT, 0, terrain[0][0].start)
    for action in actions:
        pos = apply_action(pos, action, terrain)
        # print(pos)
    pos = pos[0], pos[1] + 1, pos[2] + 1
    return str(sum(v * f for v, f in zip(pos, (1, 1000, 4))))


@pytest.mark.skip
def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "6032"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()

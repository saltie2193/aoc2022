from __future__ import annotations

import os

from dotenv import load_dotenv

from aoc import AOC

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")

Field = tuple[int, int]  # row, col
Solids = set[Field]
Terrain = tuple[list[range], Solids]
Position = tuple[int, int, int]  # direction, i, j

Actions = list[str, int]


def parse_map(map_str: str) -> Terrain:
    res = []
    solids = set()
    for i, line in enumerate(map_str.splitlines()):
        start = None
        for j, char in enumerate(line):
            if char == " ":
                continue

            if start is None:
                start = j

            if char == "#":
                solids.add((i, j))

        res.append(range(start, len(line)))

    return res, solids


def parse_actions(actions_str: str) -> list[str, int]:
    string = actions_str.strip()
    res = []
    lc = 0
    for i, char in enumerate(string):
        if char in ("L", "R"):
            res.append(int(string[lc:i]))
            res.append(char)
            lc = i + 1
    res.append(int(string[lc:]))
    return res


def parse(input_str: str) -> tuple[Terrain, Actions]:
    map_str, actions_str = input_str.split("\n\n")
    return parse_map(map_str), parse_actions(actions_str)


def turn(pos: Position, action: str) -> Position:
    # print(f"turn {action}")
    if action == "L":
        return (pos[0] - 1) % 4, pos[1], pos[2]
    if action == "R":
        return (pos[0] + 1) % 4, pos[1], pos[2]
    raise ValueError(f"Unknown action '{action}'")


def move_up_down(pos: Position, distance: int, terrain: Terrain) -> Position:
    if distance == 0:
        return pos

    facing = pos[0]
    if facing not in (1, 3):
        raise AttributeError(f"Unsupported direction '{facing}'")

    offset = 1 if facing == 1 else -1
    _fields, solids = terrain
    i, j = (pos[1] + offset) % len(_fields), pos[2]
    while j not in _fields[i]:
        i = (i + offset) % len(_fields)

    if (i, j) in solids:
        return pos
    return move_up_down((facing, i, j), distance - 1, terrain)


def move_left_right(pos: Position, distance: int, terrain: Terrain) -> Position:
    if distance == 0:
        return pos

    facing = pos[0]
    if facing not in (0, 2):
        raise ValueError(f"Unsupported direction {facing}")

    offset = 1 if facing == 0 else -1
    i, j = pos[1], pos[2] + offset

    row = terrain[0][i]
    if j not in row:
        j = row.start + ((j - row.start) % len(row))

    if (i, j) in terrain[1]:
        return pos
    return move_left_right((facing, i, j), distance - 1, terrain)


def move_left_right_i(pos: Position, distance: int, terrain: Terrain) -> Position:
    facing, i, j = pos
    if facing not in (0, 2):
        raise ValueError(f"Unsupported direction {facing}")

    offset = 1 if facing == 0 else -1
    row = terrain[0][i]

    for _ in range(distance):
        new_j = row.start + ((j + offset - row.start) % len(row))

        if (i, new_j) in terrain[1]:
            break
        j = new_j
    return facing, i, j


def move(pos: Position, distance: int, terrain: Terrain) -> Position:
    # print(f"move {distance}")
    direction = pos[0]
    if direction in (0, 2):  # right, left
        return move_left_right(pos, distance, terrain)
    if direction in (1, 3):  # down, up
        return move_up_down(pos, distance, terrain)
    raise ValueError(f"Unknown direction '{direction}'")


def apply_action(pos: Position, action: str | int, terrain: Terrain) -> Position:
    if action in ("L", "R"):
        return turn(pos, action)

    if type(action) is not int:
        raise TypeError(f"Unsupported action {action} of type {type(action)}")

    return move(pos, action, terrain)


def compute(input_str: str) -> str:
    terrain, actions = parse(input_str)
    pos = (0, 0, terrain[0][0].start)
    # print(actions)
    # print(f"start: {pos}")
    for action in actions:
        pos = apply_action(pos, action, terrain)
        # print(pos)
    pos = pos[0], pos[1] + 1, pos[2] + 1
    return str(sum(v * f for v, f in zip(pos, (1, 1000, 4))))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "6032"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part)


if __name__ == "__main__":
    main()

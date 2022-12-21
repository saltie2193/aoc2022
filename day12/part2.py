from __future__ import annotations

import math
import os
from typing import Optional

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


class Node:
    i: int
    j: int
    weight: float = math.inf
    height: int
    prev: Optional[Node] = None
    complete: bool = False

    def __init__(self, i, j, height) -> None:
        self.i = i
        self.j = j
        self.height = height

    def __lt__(self, other):
        return self.weight < other.weight

    def __repr__(self) -> str:
        i = self.i
        j = self.j
        height = self.height
        weight = self.weight
        s = f"Node({i=}, {j=}, {height=}, {weight=}"
        if self.prev is not None:
            s += f", {(self.prev.i, self.prev.j)} )"
        else:
            s += ")"

        return s


def nodes_visited_2_str(
    nodes: list[list[Node]], unvisited: set[tuple[int, int]]
) -> str:
    res = ""
    for row in nodes:
        for node in row:
            if (node.i, node.j) in unvisited:
                res += chr(node.height + 96)
            else:
                res += chr(node.height + 96).upper()

        res += "\n"
    return res


def parse(
    input_str: str,
) -> tuple[tuple[int, int], list[list[Node]]]:
    start: Node | None = None
    nodes: list[list[Node]] = []

    for i, line in enumerate(input_str.splitlines()):
        nodes.append([])
        for j, char in enumerate(line):
            if char == "E":
                start = Node(i, j, 26)
                nodes[i].append(start)
                continue

            nodes[i].append(Node(i, j, ord(char) - 96))

    assert start is not None
    return (start.i, start.j), nodes


def get_current(unvisited: set[tuple[int, int]], nodes: list[list[Node]]) -> Node:
    current: Optional[Node] = None
    for i, j in unvisited:
        if current is None or nodes[i][j].weight < current.weight:
            current = nodes[i][j]

    assert current is not None
    return current


def get_path_from_end(
    end: tuple[int, int],
    backtrack: list[list[Optional[tuple[int, int]]]],
    nodes: list[list[Node]],
) -> list[Node]:
    res: list[Node] = []
    curr = backtrack[end[0]][end[1]]
    while curr is not None:
        print(curr)
        res.append(nodes[curr[0]][curr[1]])
        curr = backtrack[curr[0]][curr[1]]

    return list(reversed(res))


def compute(input_str: str) -> str:
    start, nodes = parse(input_str)
    unvisited: set[tuple[int, int]] = set()
    backtrack: list[list[Optional[tuple[int, int]]]] = [
        [None for _ in enumerate(row)] for row in nodes
    ]
    for i, _ in enumerate(nodes):
        for j, _ in enumerate(nodes[i]):
            unvisited.add((i, j))

    nodes[start[0]][start[1]].weight = 0

    while len(unvisited) > 0:
        current = get_current(unvisited, nodes)
        for i, j in [
            (current.i, current.j - 1),
            (current.i, current.j + 1),
            (current.i - 1, current.j),
            (current.i + 1, current.j),
        ]:
            if i < 0 or i >= len(nodes) or j < 0 or j >= len(nodes[i]):
                continue

            if i == current.i and j == current.j:
                # print(f"skip {(i,j)} (current node)")
                continue

            if not (i, j) in unvisited:
                # print(f"skip {(i,j)} not in unvisited")
                continue

            node = nodes[i][j]
            if node.complete:
                continue

            if current.height - node.height > 1:
                continue

            if current.weight == math.inf:
                pass
                # print(current)

            weight = current.weight + 1
            if weight < node.weight:
                nodes[i][j].weight = weight
                nodes[i][j].prev = current
                backtrack[i][j] = (current.i, current.j)

        unvisited.remove((current.i, current.j))
        nodes[current.i][current.j].complete = True

        if current.height == 1:
            p = get_path_from_end((current.i, current.j), backtrack, nodes)
            return str(len(p))

    return "-1"


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "29"


def main():
    aoc = AOC(API_TOKEN if API_TOKEN is not None else "", HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()

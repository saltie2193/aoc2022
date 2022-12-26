from __future__ import annotations

import os
from typing import TypedDict

from aoc import AOC
from dotenv import load_dotenv
from tqdm import tqdm

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")

resource_map: dict[str, int] = {
    "ore": 0,
    "clay": 1,
    "obsidian": 2,
    "geode": 3,
    "time": 4,
}

Resources = tuple[int, int, int, int]
Robots = Resources
RobotCost = tuple[int, int, int, int]
RobotCosts = tuple[RobotCost, RobotCost, RobotCost, RobotCost]


class Factory(TypedDict):
    id: int
    costs: RobotCosts


def parse_robot_costs(string: str) -> RobotCost:
    costs = [0, 0, 0, 0, 1]
    for resource in string.strip().split(" and "):
        quant, key = resource.split(" ")
        costs[resource_map[key]] = int(quant)

    return tuple(costs)


def parse_factory(line: str) -> Factory:
    info, robots_str = line.split(":")
    i = int(info.split(" ")[1])

    costs = []
    for robot_str in robots_str[:-1].split("."):
        _, c = robot_str.strip().split("costs")
        costs.append(parse_robot_costs(c))

    return {"id": i, "costs": tuple(costs)}


def mine(robots: Robots, inventory: Resources) -> Resources:
    new_inventory = tuple(rob + res for rob, res in zip(robots, inventory))
    # print(f"mine: {inventory} -> {new_inventory}")
    return new_inventory


def add_robot(index: int, robots: Robots) -> Robots:
    tmp = list(robots)
    tmp[index] += 1
    return tuple(tmp)


def build_robot(
    index: int, robots: Robots, inventory: Resources, cost: RobotCost
) -> tuple[Robots, Resources]:
    # print(f"build {index} ({cost}):")
    new_robots = add_robot(index, robots)
    # print(f"    robots: {robots} -> {new_robots}")
    new_inventory = tuple(i - c for i, c in zip(inventory, cost))
    # print(f"    inventory: {inventory} -> {new_inventory}")

    return new_robots, new_inventory


def get_max_geodes(
    depth: int, costs: RobotCosts, robots: Robots, inventory: Resources
) -> int:
    to_visit = [
        (depth, robots, inventory, (0, 0))
    ]  # time to go, robots, inventory, (geodes robots, geodes)
    visited: set[tuple[int, Robots, Resources]] = set()
    max_cost = tuple(max(x) for x in zip(*costs))
    max_seen = 0
    max_index = 3
    end_states = []

    while to_visit:
        time, _robots, _inventory, _geo = to_visit.pop()

        if time <= 0:
            max_seen = max(_inventory[max_index], max_seen)
            end_states.append((time, _robots, _inventory))
            continue
        if (time, _robots, _inventory) in visited:
            continue

        visited.add((time, _robots, _inventory))
        max_seen = max(_inventory[max_index], max_seen)

        # print(f"{_res[max_index]} + {sum(range(remaining))} < {max_seen}?" )
        if _geo[1] + sum(range(time)) < max_seen:
            continue

        mined_inventory = mine(_robots, _inventory)

        if all(r >= c for r, c in zip(_inventory, costs[max_index])):
            # print(f"mine geode: {_geo}")
            new_rob, new_inv = build_robot(
                max_index, _robots, mined_inventory, costs[max_index]
            )
            to_visit.append(
                (time - 1, new_rob, new_inv, (_geo[0] + 1, _geo[1] + time - 1))
            )
            max_seen = max(max_seen, _geo[1] + time - 1)
            continue

        # idle
        to_visit.append((time - 1, _robots, mined_inventory, _geo))

        # build robots
        for i, cost in enumerate(costs[:3]):
            # can we afford the robot?
            if any(r < c for r, c in zip(_inventory, cost)):
                continue

            if _robots[i] >= max_cost[i]:
                continue

            # do we need the robot
            if (
                i != max_index
                and _robots[i] * time + _inventory[i] > time * max_cost[i]
            ):
                continue

            to_visit.append(
                (time - 1, *build_robot(i, _robots, mined_inventory, cost), _geo)
            )

    return max_seen


def parse(input_str: str) -> list[Factory]:
    return list(map(parse_factory, input_str.splitlines()))


def compute(input_str: str) -> str:
    factories = parse(input_str)
    target = 24
    sims = [
        factory["id"]
        * get_max_geodes(target, factory["costs"], (1, 0, 0, 0), (0, 0, 0, 0))
        for factory in tqdm(factories)
    ]
    return str(sum(sims))


def test_build_robot() -> None:
    inventory = (10, 10, 10, 10)
    ins: list[tuple[int, Robots, RobotCost]] = [
        (1, (1, 2, 3, 4), (1, 2, 3, 4)),
        (0, (0, 2, 0, 0), (1, 2, 0, 0)),
        (2, (0, 3, 4, 0), (10, 3, 5, 0)),
        (3, (2, 2, 4, 0), (2, 2, 4, 1)),
    ]
    outs = [
        ((1, 3, 3, 4), (9, 8, 7, 6)),
        ((1, 2, 0, 0), (9, 8, 10, 10)),
        ((0, 3, 5, 0), (0, 7, 5, 10)),
        ((2, 2, 4, 1), (8, 8, 6, 9)),
        #       ((2, 2, 4, 1), (8, 8, 6, 9)),
    ]

    for (i, r, c), o in zip(ins, outs):
        assert build_robot(i, r, inventory, c) == o


def test_add_robot() -> None:
    robots = (0, 0, 0, 0)

    tests = [
        (0, (1, 0, 0, 0)),
        (1, (0, 1, 0, 0)),
        (2, (0, 0, 1, 0)),
        (3, (0, 0, 0, 1)),
    ]

    for i, o in tests:
        assert add_robot(i, robots) == o


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "33"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part, compute, test=True)


if __name__ == "__main__":
    main()

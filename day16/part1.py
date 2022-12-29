"""
Day 16: Proboscidea Volcanium
https://adventofcode.com/2022/day/16
"""
from __future__ import annotations

import os
import re

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")

Tunnel = tuple[str, int]
Valve = tuple[int, list[Tunnel]]
Valves = dict[str, Valve]


def parse(input_str: str) -> dict:
    patter = re.compile(
        "^Valve (.{2}) has flow rate=([0-9]+); tunnel(s)? lead(s)? to valve(s)? (.*)$"
    )
    valves = dict()
    for line in input_str.splitlines():
        match = patter.match(line)
        key, rate, _, _, _, tunnels = match.groups()
        valves[key] = (int(rate), [(valv.strip(), 1) for valv in tunnels.split(", ")])

    return valves


def optimize_valve(valve: str, valves: Valves) -> Valve:
    # print(f"optimize: {valve}")
    zero_valves = set(key for key, (rate, _) in valves.items() if rate == 0)
    visited = set()
    tmp = valves[valve]
    to_visit = [*tmp[1]]
    new_tunnels: list[tuple[str, int]] = []
    while to_visit:
        to_visit.sort(key=lambda a: a[1], reverse=True)
        # print(f"{to_visit=}")
        dest, cost = to_visit.pop()
        # print(f"{dest=}, {cost=}")

        if dest in visited:
            continue
        visited.add(dest)

        if dest == valve:
            continue

        new_tunnels.append((dest, cost))

        if dest not in zero_valves:
            pass
            # continue

        dests_of_tunnel = valves[dest][1]
        # print(f"dests of {dest}: {dests_of_tunnel}")
        for n, c in dests_of_tunnel:
            to_visit.append((n, cost + c))

        # print(dests_of_tunnel, visited)
        # print(f"{new_tunnels=}")

    return tmp[0], new_tunnels


def optimize_valves(valves: Valves, start="AA") -> Valves:
    new_valves = {k: v for k, v in valves.items()}

    for key in valves:
        new_valves[key] = optimize_valve(key, valves)

    zero_valves = set(key for key, (rate, _) in valves.items() if rate == 0)

    for key, (rate, tunnels) in new_valves.items():
        new_valves[key] = (
            rate,
            list(filter(lambda x: x[0] not in zero_valves, tunnels)),
        )

    return new_valves


def max_pressure_single_path(paths: list[tuple[int, frozenset[str]]]) -> int:
    return max(p[0] for p in paths)


def max_releasable_pressure(
    start: str, time: int, valves: Valves, intermediate_paths=False
) -> list[tuple[int, frozenset[str]]]:
    to_visit: list[tuple[int, str, int, set[str]]] = [(time, start, 0, set())]
    visited = set()
    max_flow = 0
    max_open_valves = len([v for v in valves.values() if v[0] > 0])
    paths: set[tuple[int, frozenset[str]]] = set()

    while to_visit:
        remaining, valve, flow, open_valves = to_visit.pop()

        if intermediate_paths:
            paths.add((flow, frozenset(open_valves)))

        if remaining == 0:
            max_flow = max(max_flow, flow)
            paths.add((flow, frozenset(open_valves)))

        if remaining <= 0:
            continue

        if len(open_valves) == max_open_valves:
            max_flow = max(max_flow, flow)
            paths.add((flow, frozenset(open_valves)))
            continue

        if (remaining, valve, flow, frozenset(open_valves)) in visited:
            continue

        max_flow_unopened = sum(
            f for k, (f, _) in valves.items() if k not in open_valves
        )
        if flow + remaining * max_flow_unopened < max_flow:
            continue

        visited.add((remaining, valve, flow, frozenset(open_valves)))

        # print(remaining, valve, flow, sorted(open_valves))
        rate, tunnels = valves.get(valve)

        # valve open?
        if rate > 0 and valve not in open_valves:
            valve_rate = (remaining - 1) * rate
            new_flow = flow + valve_rate
            # print(f"{time}: open {valve} ({flow} -> {new_flow})")
            to_visit.append(
                (remaining - 1, valve, new_flow, open_valves.union({valve}))
            )

        for (dest, cost) in tunnels:
            if remaining - cost < 0:
                continue
            to_visit.append((remaining - cost, dest, flow, open_valves))

    return list(paths)


def compute(input_str: str) -> str:
    valves = parse(input_str)
    # print("valves:", *valves.items(), sep="\n")
    print(f"optimize valves (?) ...")
    optimized = optimize_valves(valves)
    # print("optimized: ", *optimized.items(), sep="\n")
    print(f"maximize released pressure ...")
    paths = max_releasable_pressure("AA", 30, optimized)
    return str(max_pressure_single_path(paths))


def test() -> None:
    with open(os.path.join(HERE, "test.txt"), encoding="utf-8") as file:
        input_s = file.read()

    assert compute(input_s) == "1651"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 0, 0

    aoc.run_part(year, day, part)


if __name__ == "__main__":
    main()

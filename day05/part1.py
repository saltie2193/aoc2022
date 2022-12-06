import os
from functools import reduce
from typing import List, Tuple

from aoc import AOC
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


def parse_state(input_str: str) -> List[List[str]]:
    lines = input_str.splitlines()
    buckets = int(lines[-1].split(" ")[-2])
    state = [[] for _ in range(buckets)]
    offset = 4

    for line in lines[:-1]:
        i = 0
        while 1 + (i * offset) < len(line):
            index = 1 + (i * offset)
            value = line[index]
            if value != " ":
                state[i].append(value)
            i += 1
    for _s in state:
        _s.reverse()
    return state


def parse_actions(input_str: str) -> List[Tuple[int, int, int]]:
    return [
        (int(values[1]), int(values[3]), int(values[5]))
        for values in [line.split(" ") for line in input_str.splitlines()]
    ]


def apply_action(
    state: List[List[str]], count: int, src: int, dst: int
) -> List[List[str]]:
    _dst = dst - 1
    _src = src - 1
    state[_dst].extend(list(reversed(state[_src][-count:])))
    state[_src] = state[_src][:-count]
    return state


def compute(input_str: str) -> str:
    [state_str, actions_str] = input_str.split("\n\n")

    state = parse_state(state_str)
    actions = parse_actions(actions_str)
    for action in actions:
        state = apply_action(state, *action)
    return reduce(lambda a, b: a + b[-1], state, "")


def test_apply_action() -> None:
    state = [["Z", "N"], ["M", "C", "D"], ["P"]]

    expected = [["Z", "N", "D"], ["M", "C"], ["P"]]

    state_new = apply_action(state, 1, 2, 1)
    assert state_new == expected


def test_apply_action_move2() -> None:
    state = [["Z", "N"], ["M", "C", "D"], ["P"]]
    expected = [[], ["M", "C", "D", "N", "Z"], ["P"]]

    state_new = apply_action(state, 2, 1, 2)
    assert state_new == expected


def test_parse_state() -> None:
    input_str = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
"""
    expected = [["Z", "N"], ["M", "C", "D"], ["P"]]
    state = parse_state(input_str)
    print(state)
    print(expected)
    assert state == expected


def test_parse_actions() -> None:
    input_str = """\
move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
    excepted = [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)]

    assert parse_actions(input_str) == excepted


def test() -> None:
    input_s = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
    assert compute(input_s) == "CMZ"


def main():
    aoc = AOC(API_TOKEN, HERE)
    year, day, part = 2022, 5, 1

    aoc.run_part(year, day, part, compute)


if __name__ == "__main__":
    main()

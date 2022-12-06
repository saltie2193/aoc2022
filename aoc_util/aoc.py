import json
import os
from typing import Callable, Dict, Optional

from aoc_api import AOC_API, SubmitResult


class AOC:
    _aoc_api: AOC_API
    _cache_dir: str

    def __init__(self, session_cookie: str, cache_dir: str) -> None:
        self._aoc_api = AOC_API(session_cookie, cache_dir)
        self._cache_dir = cache_dir

    def cache_answer(self, year: int, day: int, part: int, answer: int, res) -> None:
        path = os.path.join(self._cache_dir, "aoc_cache.json")

        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as file:
                file.write(
                    json.dumps({year: {day: {part: {answer: res}}}}, default=str)
                )
                return

        with open(path, encoding="utf-8") as file:
            cache: Dict = json.loads(file.read())

        k_year, k_day, k_part = str(year), str(day), str(part)

        _w = False
        dict_year: Dict | None = cache.get(k_year)
        if dict_year is None:
            cache[k_year] = {k_day: {k_part: {answer: res}}}

        dict_day: Dict | None = dict_year.get(k_day)
        if not _w and dict_day is None:
            cache[k_year][k_day] = {k_part: {answer: res}}

        dict_part: Dict | None = dict_day.get(k_part)
        if not _w and dict_part is None:
            cache[k_year][k_day][k_part][answer] = res

        with open(path, encoding="utf-8") as file:
            file.write(json.dumps(cache, default=str))

    def get_cached_answer(
        self, year: int, day: int, part: int, answer: str
    ) -> Optional[SubmitResult]:
        # get json from file
        path = os.path.join(self._cache_dir, "aoc_cache.json")

        if not os.path.exists(path):
            return None

        with open(path, encoding="utf-8") as file:
            cache: Dict = json.load(file)

        dict_year: Dict | None = cache.get(str(year))
        if dict_year is None:
            return None

        dict_day: Dict | None = dict_year.get(str(day))
        if dict_day is None:
            return None

        dict_part: Dict | None = dict_day.get(str(part))
        if dict_part is None:
            return None

        return dict_part.get(answer)

    def run_part(
        self,
        year: int,
        day: int,
        part: int,
        compute: Callable[[str], str],
        auto_submit=False,
    ) -> str:
        input_str = self._aoc_api.get_input(year, day)

        answer = str(compute(input_str))
        print(answer)

        if auto_submit:
            self.submit_solution(year, day, part, answer)
        else:
            print("Skip submission. auto_submit disabled")

    def submit_solution(self, year: int, day: int, part: int, answer: str) -> None:
        cached = self.get_cached_answer(year, day, part, answer)

        if cached == SubmitResult.RIGHT:
            print(f"Skip submission, '{answer}' already submitted successfully.")
            return

        if cached == SubmitResult.ALREADY_DONE:
            print("Skip submission, solution has already been submitted.")
            return

        if cached == SubmitResult.WRONG:
            print(
                f"Skip submission, '{answer}' already submitted as wrong solution. (Set force_submit=True to submit anyway)"
            )
            return

        print(f"Submitting solution '{answer}'.")

        result, txt = self._aoc_api.submit_solution(year, day, part, answer)
        if result == SubmitResult.RIGHT:
            print(f"'{answer}' was correct!")
        else:
            print(result, txt)

        self.cache_answer(year, day, part, answer, result)


def get_year_day() -> tuple[int, int]:
    cwd = os.getcwd()
    day_s = os.path.basename(cwd)
    year_s = os.path.basename(os.path.dirname(cwd))

    if not day_s.startswith("day") or not year_s.startswith("aoc"):
        raise AssertionError(f"unexpected working dir: {cwd}")

    return int(year_s[len("aoc") :]), int(day_s[len("day") :])


def _get_test_data(path="test.txt") -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

import importlib.machinery
import importlib.util
import json
import os
import re
import shutil
from datetime import date
from typing import Callable, Dict, Optional

import pytest
from aoc_api import AOC_API, SubmitResult
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(HERE, "../.env"))
API_TOKEN = os.getenv("API_TOKEN")


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
        compute: Callable[[str], str] = None,
        auto_submit=False,
    ) -> None:
        input_str = self._aoc_api.get_input(year, day)

        if compute is None:
            print("Skip calculation of answer, 'compute' not provided.")
            return

        answer = str(compute(input_str))
        print(f"Answer: {answer}")

        if auto_submit:
            self.submit_solution(year, day, part, answer)
        else:
            print("Skip submission. auto_submit disabled")

    def get_input(self, year: int, day: int) -> Optional[str]:
        today = date.today()
        d = date(year, 12, day)
        if today < d:
            print(f"Skip getting input, {d!r} is in the future.")
            return None
        return self._aoc_api.get_input(year, day)

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


def get_input(directory: str, year: int, day: int):
    path_day = os.path.join(directory, f"day{day:0>2}")
    today = date.today()
    d = date(year, 12, day)
    if today < d:
        print(f"Skip getting input, {d} is in the future.")
        return
    aoc_api = AOC_API(API_TOKEN, directory)
    aoc_api.get_input(year, day)


def init_day(directory: str, year: int, day: int, force=False) -> None:
    """
    Creates the base folder for the given day.

        Parameters:
            directory (str): Directory the day directory is created in.
            day (int): Day to create.

        Returns:
            None:


    """
    print(f"Init day {day}")

    day_s = f"day{day:0>2}"
    # check if we are already in the dayXX folder
    folder_name = os.path.basename(directory)
    if not folder_name.startswith("day"):
        # create folder 'dayXX'
        dst = os.path.join(directory, day_s)
        if not os.path.exists(dst):
            print(f"Creating dir '{dst}'.")
            os.mkdir(dst)
        src = os.path.join(directory, "day00")
    elif folder_name == day_s:
        dst = directory
        src = os.path.join(directory, "../day00")
    else:
        print("Unexpected working directory")
        return

    for file in os.listdir(src):
        file_s = os.path.join(src, file)
        file_d = os.path.join(dst, file)

        if os.path.exists(file_d) and not force:
            print(f"Skip '{file}'. File already exists.")
            continue
        shutil.copy(file_s, file_d)

    get_input(dst, year, day)


def init_day_auto(directory: str) -> None:
    """
    Automatically create the folder stub for the next missing days.

        Parameters:
            directory (str): Directory used as base

        Returns:
            None
    """
    try:
        year = get_year(directory)
        day = None
        path_2_year = directory
    except AssertionError:
        year, day = get_year_day(directory)
        path_2_year = os.path.dirname(directory)
        init_day(path_2_year, year, day)
        return

    if not os.path.exists(os.path.join(path_2_year, "day00")):
        print("Folder 'day00' does not exist, are you in the right directory?")
        return

    day_today = date.today().day
    path_2_tody = os.path.join(path_2_year, f"day{day_today:0>2}")
    if not os.path.exists(path_2_tody):
        print(f"Init current day {day_today}")
        init_day(path_2_year, get_year(path_2_year), day_today)
        return

    re_day = re.compile(r"^day([0-9]{2})$")
    days = []

    for file in os.listdir(path_2_year):
        p = os.path.join(path_2_year, file)
        if not os.path.isdir(p):
            continue

        found = re_day.search(file)
        if found:
            days.append(int(found.group(1)))

    days.sort()
    for i, d in enumerate(days):
        if i != d:
            init_day(path_2_year, year, i)
            return

    init_day(path_2_year, year, len(days))
    return


def run_day(directory: str, year: int, day: int, part: int, auto_submit: bool):
    print(f"Running: year {year}, day {day}, part {part}")

    path_day = os.path.join(directory, f"day{day:0>2}")
    if not os.path.exists(path_day):
        print(f"Directory for day {day} does not exist.")
        return

    print("Running tests...")

    path_module = os.path.join(path_day, f"part{part}.py")
    retcode = pytest.main([path_module])
    if retcode != pytest.ExitCode.OK:
        print("Test did not succeed, aborting run")
        return

    loader = importlib.machinery.SourceFileLoader("mymodule", path_module)
    spec = importlib.util.spec_from_loader("mymodule", loader)
    module_part = importlib.util.module_from_spec(spec)
    loader.exec_module(module_part)

    aoc = AOC(API_TOKEN, path_day)
    aoc.run_part(year, day, part, module_part.compute, auto_submit)


def get_year(path: str) -> int:
    year_s = os.path.basename(path)
    if not year_s.startswith("aoc"):
        raise AssertionError(f"unexpected working dir: {path}")

    return int(year_s[len("aoc") :])


def get_year_day(path: str) -> tuple[int, int]:
    day_s = os.path.basename(path)
    year_s = os.path.basename(os.path.dirname(path))

    if not day_s.startswith("day") or not year_s.startswith("aoc"):
        raise AssertionError(f"unexpected working dir: {path}")

    return int(year_s[len("aoc") :]), int(day_s[len("day") :])


def _get_test_data(path="test.txt") -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

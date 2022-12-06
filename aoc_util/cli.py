import argparse
import os

from aoc import get_year, get_year_day, init_day, init_day_auto, run_day


def cli_init_day() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int, nargs="?")
    parser.add_argument("--force", action=argparse.BooleanOptionalAction)
    parser.add_argument("--download", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    day = args.day
    cwd = os.getcwd()
    if args.download:
        get_input(cwd, day)
        return

    if day:
        init_day(cwd, get_year(cwd), day, force=args.force)

    init_day_auto(cwd)


def cli_run_day() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int, nargs="?", choices=range(1, 26))
    parser.add_argument("--part", type=int, choices=range(1, 3), default=1)
    parser.add_argument("--year", type=int)
    parser.add_argument("--submit", action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    year_a = args.year
    day_a = args.day

    if year_a and day_a is None:
        print("Day needs to be provided if year is given")
        return 1
    cwd = os.getcwd()
    if year_a and day_a:
        # check if we are already in the dayXX folder
        year = year_a
        day = day_a
        path = "?"
    elif day_a and year_a is None:
        year = get_year(cwd)
        day = day_a
        path = cwd
    else:
        year, day = get_year_day(cwd)
        path = cwd
        path = os.path.join(cwd, "..")

    run_day(path, year, day, args.part, args.submit)


def main():
    cli_run_day()


if __name__ == "__main__":
    main()

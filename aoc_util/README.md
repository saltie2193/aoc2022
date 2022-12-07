# aoc util
Utilities for advent of code

## aoc-init

Commandline utility to initiate the folder of a single day.
The tool expects to be run in the base directory of the project (`aocYYYY`) or in the directory of a day (`aocYYYY/dayDD`).

When initializing the folder the input for the given day will be downloaded automatically. If the day is set in the future, the download of the input data will be skipped. The input data can be downloaded on a later point by providing the `--download` flag.

    aoc2022$ aoc-init 13 --download

In general the tool will skip existing already existing files. This behavior can be overwritten by setting the `--force` flag.

### Base directory

If it's run in the base directory without a given day, it will create the next missing day. The next missing day is either today or the next consecutive missing day.

    # aoc2022
    # |- day00
    # |- day01
    # |_ day04
    # 
    # will create day03

    aoc2022$ aoc-init

If it's run in the base directory with a given day, it will create the directory for the given day and copy the contents of `day00/` to it. Already existing files will be skipped.

    # create folder for day 13
    aoc2022> aoc-init 13

### Day directory

Inside a day directory the parameter for the day can be omitted. It will be detected automatically.

If it's run in the in the directory of a day it will get the day from the directory itself. It will try to copy the contents of `day00/` to the folder. Already existing files will be skipped.

    # copy contents of day00/ to day13/
    aoc2022/day13$ aoc-init

    # download input for day13
    aoc2022/day13$ aoc-init --download

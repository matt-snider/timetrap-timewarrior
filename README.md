# Timetrap to Timewarrior Migration

A simple script to migrate timer entries from [timetrap](https://github.com/samg/timetrap) to [timewarrior](https://github.com/GothenburgBitFactory/timewarrior).

## Usage

```sh
$ python migrate.py --help
usage: migrate.py [-h] [--timew-path TIMEW_PATH] [--dry-run] [--adjust]
                  DATABASE_PATH

Migrate timer entries from timetrap to timewarrior.

positional arguments:
  DATABASE_PATH         Path to the timetrap sqlite database.

optional arguments:
  -h, --help            show this help message and exit
  --timew-path TIMEW_PATH
                        Path to the timew executable.
  --dry-run             Prints the generated commands but do not execute them.
  --adjust              Whether to add the :adjust hint to generated commands
                        to automatically correct overlapping intervals.
```

## Requirements

* Python 3


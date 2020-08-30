import sqlite3
import subprocess
from argparse import ArgumentParser
from datetime import datetime


def migrate(db_path, timew_path, dry_run, adjust, where):
    """ Migrate time entries from timetrap to timewarrior """

    conn = sqlite3.connect(db_path)

    if where:
        where = f'where {where}'

    # See schema: https://github.com/samg/timetrap/blob/master/lib/timetrap/schema.rb
    for (_, note, start, end, sheet) in conn.execute('select * from entries {}'.format(where)):
        print(f'Import {sheet}: {start} to {end}')

        # Strip the leading _ from archived sheets
        tags = [sheet.strip('_')]

        # Build command and run or print depending on dry_run
        commands = build_commands(timew_path, start, end, tags, note, adjust)
        for command in commands:
            if dry_run:
                command_str = ' '.join(command)
                print(f'$ {command_str}')
            else:
                subprocess.run(command, check=True)


def build_commands(timew, start, end, tags, annotation, adjust):
    start = datetime.fromisoformat(start).isoformat('T', 'seconds')
    end = datetime.fromisoformat(end).isoformat('T', 'seconds')
    tags = ' '.join(tags)

    # Note: the :adjust hint will cause overlapping intervals to be automatically adjusted
    commands = [[
        timew, 'track',
        ':adjust' if adjust else '',
        start, 'to', end,
        tags
    ]]

    if annotation:
        commands.append([timew, 'annotate', "@1", f'"{annotation}"'])

    return commands


if __name__ == '__main__':
    parser = ArgumentParser(description='Migrate timer entries from timetrap to timewarrior.')
    parser.add_argument('database_path', metavar='DATABASE_PATH',
        help='Path to the timetrap sqlite database.')
    parser.add_argument('--timew-path', default='timew',
        help='Path to the timew executable.')
    parser.add_argument('--dry-run', action='store_true',
        help='Prints the generated commands but do not execute them.')
    parser.add_argument('--adjust', action='store_true',
        help='Whether to add the :adjust hint to generated commands '
        + 'to automatically correct overlapping intervals.')
    parser.add_argument('--where', metavar='WHERE_CLAUSE',
        help='A SQL where clause to filter the timetrap entries '
        + "(e.g. --where \"start > '2020-01-01'\")")

    args = parser.parse_args()
    migrate(
        args.database_path,
        args.timew_path,
        args.dry_run,
        args.adjust,
        args.where)

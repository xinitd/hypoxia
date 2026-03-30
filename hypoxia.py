#!/usr/bin/env python3


import argparse
from argparse import RawTextHelpFormatter
import sys
import uuid
from pathlib import Path
from utils import *
from colors import info, error


__version__ = '1.2.2'


def dir_path(path_string):
    path_obj = Path(path_string)
    if path_obj.is_dir():
        return path_obj
    else:
        raise argparse.ArgumentTypeError(f'Directory not found or access denied: "{path_string}"')


def main():
    task_id = str(uuid.uuid4())
    result = False

    parser = argparse.ArgumentParser(
        description='Hypoxia: Targeted file extraction and backup utility.',
        epilog='''
Options Summary:
  Logging level:        -v, --verbosity
  Target location:      -s, --search-path
  Target files:         -e, --extensions
  Copy behavior:        -m, --keep-metadata
  Timeframe filters:    --date-from, --date-to
  Size limits:          --size-min, --size-max
''',
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    parser.add_argument(
        '-v', '--verbosity',
        choices=['silent', 'info'],
        required=True,
        help='Set logging level. "silent" suppresses output, "info" logs all actions.'
    )
    parser.add_argument(
        '-s', '--search-path',
        type=dir_path,
        required=True,
        help='Absolute or relative path to the target directory.'
    )
    parser.add_argument(
        '-e', '--extensions',
        type=str,
        required=True,
        help='Comma-separated list of target file extensions (e.g., pdf,docx,txt).'
    )
    parser.add_argument(
        '-m', '--keep-metadata',
        choices=['yes', 'no'],
        default='yes',
        help='Preserve original file metadata (timestamps, permissions). "no" speeds up copying.'
    )
    parser.add_argument(
        '--date-from',
        type=str,
        required=False,
        help='Filter for files modified on or after this date (YYYY-MM-DD).'
    )
    parser.add_argument(
        '--date-to',
        type=str,
        required=False,
        help='Filter for files modified on or before this date (YYYY-MM-DD).'
    )
    parser.add_argument(
        '--size-min',
        type=str,
        required=False,
        help='Minimum file size boundary (e.g., 10kb, 100mb, 2gb).'
    )
    parser.add_argument(
        '--size-max',
        type=str,
        required=False,
        help='Maximum file size boundary (e.g., 10kb, 100mb, 2gb).'
    )

    args = parser.parse_args()

    verbosity = (args.verbosity == 'info')
    keep_metadata = (args.keep_metadata == 'yes')

    try:
        target_extensions = args.extensions.split(',')
    except Exception as e:
        error('Invalid --extensions format. Expected a comma-separated list.')
        sys.exit()

    if verbosity:
        info('Initializing Hypoxia...')
        info(f'Task ID: {task_id}')

    preparation_result = prepare_workspace(task_id, target_extensions, verbosity)
    if preparation_result:
        result = collect_files(
            task_id, target_extensions, verbosity, keep_metadata, args.search_path, args.date_from, args.date_to, args.size_min, args.size_max
        )

    if result:
        if verbosity:
            info('Extraction task completed successfully.')


if __name__ == '__main__':
    main()

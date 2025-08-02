#!/usr/bin/python3


import argparse
import sys
import uuid
from pathlib import Path
from utils import *


def dir_path(path_string):
    path_obj = Path(path_string)
    if path_obj.is_dir():
        return path_obj
    else:
        raise argparse.ArgumentTypeError(f'"{path_string}" is not a valid directory.')


def main():
    task_id = str(uuid.uuid4())

    parser = argparse.ArgumentParser(description='Hypoxia. Every byte will be found.')

    parser.add_argument(
        '-v', '--verbosity',
        choices=['silent', 'info'],
        required=True,
        help='Set verbosity level for display additional information in runtime: "silent" - no any prints in terminal, "info" - print every action.'
    )
    parser.add_argument(
        '-s', '--search-path',
        type=dir_path,
        required=True,
        help='Setting up searching path. The absolute or relative path to the directory to search in.'
    )
    parser.add_argument(
        '-e', '--extensions',
        type=str,
        required=True,
        help='File extensions to search for, separated by commas (e.g., "pdf,docx,txt").'
    )
    parser.add_argument(
        '-m', '--keep-metadata',
        choices=['yes', 'no'],
        default='no',
        help='Defines if file metadata should be preserved. "yes" keeps it, "no" discards it (faster).'
    )

    args = parser.parse_args()

    verbosity = (args.verbosity == 'info')
    keep_metadata = (args.keep_metadata == 'yes')

    try:
        target_extensions = args.extensions.split(',')
    except Exception as e:
        print('Wrong --extensions argument.')
        sys.exit()

    if verbosity:
        print('Starting Hypoxia...')
        print(f'Setting up task: {task_id}')

    preparation_result = prepare_workspace(task_id, target_extensions, verbosity)
    if preparation_result:
        copy_result = hypoxia_copy(task_id, target_extensions, verbosity, keep_metadata, args.search_path)

    if verbosity:
        print('Hypoxia finished work. Bye!')


if __name__ == '__main__':
    main()

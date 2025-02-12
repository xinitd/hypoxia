#!/usr/bin/python3


import argparse
import sys
import uuid

from utils import *


def main():
    task_id = str(uuid.uuid4())

    parser = argparse.ArgumentParser(description='Hi! I am Hypoxia - forensic tool. I may help you in file searching')

    parser.add_argument(
        '-v', '--verbosity', type=str, required=True,
        help='Set verbosity level for view additional information while program working: silent - no any prints in terminal, info - print every action'
    )

    parser.add_argument(
        '-s', '--search-path', type=str, required=True,
        help='Set searching path'
    )

    parser.add_argument(
        '-e', '--extensions', type=str, required=True,
        help='Set file extensions for search'
    )

    parser.add_argument(
        '-m', '--keep-metadata', default='no', type=str,
        help='Metadata saving mode for collected files: no - copy files without metadata (faster), yes - attempts to keep all metadata'
    )

    args = parser.parse_args()

    target_extensions = None
    verbosity = None
    keep_metadata = None

    if args.verbosity == 'silent':
        verbosity = False
    elif args.verbosity == 'info':
        verbosity = True
    else:
        print('Wrong --verbosity argument.')
        sys.exit()

    if args.keep_metadata == 'yes':
        keep_metadata = True
    elif args.keep_metadata == 'no':
        keep_metadata = False
    else:
        print('Wrong --keep-metadata argument.')
        sys.exit()

    try:
        target_extensions = args.extensions.split(',')
    except Exception as e:
        print('Wrong --extensions argument.')
        sys.exit()

    if verbosity:
        print('Starting Hypoxia...')

    preparation_result = prepare_workspace(task_id, target_extensions, verbosity)
    if preparation_result:
        if verbosity:
            print('Setting up task id: ' + task_id)
        copy_result = hypoxia_copy(task_id, target_extensions, verbosity, keep_metadata, args.search_path)

    if verbosity:
        print('Hypoxia finished work. Bye!')


if __name__ == '__main__':
    main()

import sys
import shutil
import datetime
from pathlib import Path


WORKSPACE = Path.cwd()
workdir = 'data'


def prepare_workspace(task_id, file_extensions, verbosity):
    if verbosity:
        print('Preparing environment. Please wait...')
    (WORKSPACE / workdir).mkdir(exist_ok=True)
    (WORKSPACE / workdir / task_id).mkdir(exist_ok=True)

    for file_extension in file_extensions:
        (WORKSPACE / workdir / task_id / file_extension).mkdir(exist_ok=True)
    if verbosity:
        print('Environment ready.')
    return True


def parse_start_date(date_from_str=None):
    if not date_from_str:
        return None
    try:
        return datetime.datetime.strptime(date_from_str, '%Y-%m-%d').date()
    except ValueError:
        print(f'Error: Incorrect date format for "{date_from_str}". Please use the YYYY-MM-DD format.')
        sys.exit(1)


def parse_end_date(date_to_str=None):
    if not date_to_str:
        return None
    try:
        return datetime.datetime.strptime(date_to_str, '%Y-%m-%d').date()
    except ValueError:
        print(f'Error: Incorrect date format for "{date_to_str}". Please use the YYYY-MM-DD format.')
        sys.exit(1)


def hypoxia_copy(task_id, file_extensions, verbosity, keep_metadata, search_path):
    if verbosity:
        print(f'Started search at {search_path}')

    copy_function = shutil.copy2 if keep_metadata else shutil.copy

    search_path_obj = Path(search_path)

    for file_extension in file_extensions:
        files_to_copy = search_path_obj.rglob(f'*.{file_extension}')

        for source_file in files_to_copy:
            try:
                if verbosity:
                    print(f'Copying: {source_file}')

                destination_file = WORKSPACE / workdir / task_id / file_extension / source_file.name

                copy_function(source_file, destination_file)

            except (IOError, OSError) as e:
                if verbosity:
                    print(f'Error copying file {source_file}: {e}')

    if verbosity:
        print('Copying done.')

    return True

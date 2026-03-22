import sys
import shutil
import datetime
from pathlib import Path
from colors import info, success, warning, error


WORKSPACE = Path.cwd()
workdir = 'data'

WARNING_FREE_SPACE  = 500 * 1024 * 1024
CRITICAL_FREE_SPACE = 50  * 1024 * 1024


def prepare_workspace(task_id, file_extensions, verbosity):
    if verbosity:
        info('Initializing workspace...')
    (WORKSPACE / workdir).mkdir(exist_ok=True)
    (WORKSPACE / workdir / task_id).mkdir(exist_ok=True)

    for file_extension in file_extensions:
        (WORKSPACE / workdir / task_id / file_extension).mkdir(exist_ok=True)
    if verbosity:
        success('Workspace initialized.')
    return True


def parse_size(size_str=None):
    if not size_str:
        return None
    units = {'gb': 1024 ** 3, 'mb': 1024 ** 2, 'kb': 1024, 'b': 1}
    normalized = size_str.strip().lower()
    for unit, multiplier in units.items():
        if normalized.endswith(unit):
            try:
                return int(float(normalized[:-len(unit)]) * multiplier)
            except ValueError:
                error(f'Invalid size value: "{size_str}".')
                sys.exit(1)
    try:
        return int(normalized)
    except ValueError:
        error(f'Invalid size format: "{size_str}". Supported formats: 500b, 10kb, 100mb, 2gb.')
        sys.exit(1)


def parse_start_date(date_from_str=None):
    if not date_from_str:
        return None
    try:
        return datetime.datetime.strptime(date_from_str, '%Y-%m-%d').date()
    except ValueError:
        error(f'Invalid date format: "{date_from_str}". Expected format: YYYY-MM-DD.')
        sys.exit(1)


def parse_end_date(date_to_str=None):
    if not date_to_str:
        return None
    try:
        return datetime.datetime.strptime(date_to_str, '%Y-%m-%d').date()
    except ValueError:
        error(f'Invalid date format: "{date_to_str}". Expected format: YYYY-MM-DD.')
        sys.exit(1)


def collect_files(task_id, file_extensions, verbosity, keep_metadata, search_path, date_from_str, date_to_str, size_min_str, size_max_str):
    if verbosity:
        info(f'Scanning directory: {search_path}')

    copy_function = shutil.copy2 if keep_metadata else shutil.copy

    search_path_obj = Path(search_path)

    start_date = parse_start_date(date_from_str)
    end_date = parse_end_date(date_to_str)
    size_min = parse_size(size_min_str)
    size_max = parse_size(size_max_str)

    low_space_warned = False

    for file_extension in file_extensions:
        files_to_copy = search_path_obj.rglob(f'*.{file_extension}')

        for source_file in files_to_copy:
            free_space = shutil.disk_usage(WORKSPACE).free

            if free_space < CRITICAL_FREE_SPACE:
                error(f'CRITICAL: Insufficient disk space ({free_space // (1024 * 1024)}MB remaining). Halting execution.')
                return False

            if free_space < WARNING_FREE_SPACE and not low_space_warned:
                warning(f'WARNING: Low disk space ({free_space // (1024 * 1024)}MB remaining).')
                low_space_warned = True

            file_stat = source_file.stat()
            file_mtime = datetime.datetime.fromtimestamp(file_stat.st_mtime).date()
            file_size = file_stat.st_size

            if start_date and file_mtime < start_date:
                continue
            if end_date and file_mtime > end_date:
                continue
            if size_min and file_size < size_min:
                continue
            if size_max and file_size > size_max:
                continue

            try:
                if verbosity:
                    print(f' Copying: {source_file}')

                destination_file = WORKSPACE / workdir / task_id / file_extension / source_file.name

                copy_function(source_file, destination_file)

            except (IOError, OSError) as e:
                if verbosity:
                    error(f'Failed to copy {source_file}: {e}')

    if verbosity:
        success('File collection complete.')

    return True

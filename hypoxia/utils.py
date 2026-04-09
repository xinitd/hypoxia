import sys
import shutil
import zipfile
import datetime
from pathlib import Path
from hypoxia.colors import info, success, warning, error
from hypoxia.forensic import compute_hash, create_manifest, ForensicLog


WORKSPACE = Path.cwd()
WORKDIR = 'data'

WARNING_FREE_SPACE  = 500 * 1024 * 1024
CRITICAL_FREE_SPACE = 50  * 1024 * 1024


def prepare_workspace(task_id, file_extensions, verbosity):
    if verbosity:
        info('Initializing workspace...')
    (WORKSPACE / WORKDIR).mkdir(exist_ok=True)
    (WORKSPACE / WORKDIR / task_id).mkdir(exist_ok=True)

    for file_extension in file_extensions:
        (WORKSPACE / WORKDIR / task_id / file_extension).mkdir(exist_ok=True)
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


def parse_date(date_str=None, label='date'):
    if not date_str:
        return None
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        error(f'Invalid {label} format: "{date_str}". Expected format: YYYY-MM-DD.')
        sys.exit(1)


def collect_files(task_id, file_extensions, verbosity, keep_metadata, search_path, date_from_str, date_to_str, size_min_str, size_max_str, exclude_dirs=None, hash_algorithm='sha256'):
    if verbosity:
        info(f'Scanning directory: {search_path}')

    copy_function = shutil.copy2 if keep_metadata else shutil.copy

    search_path_obj = Path(search_path)

    start_date = parse_date(date_from_str, label='--date-from')
    end_date = parse_date(date_to_str, label='--date-to')
    size_min = parse_size(size_min_str)
    size_max = parse_size(size_max_str)

    if exclude_dirs is None:
        exclude_dirs = []

    use_hashing = hash_algorithm and hash_algorithm != 'none'
    manifest_entries = []

    log_path = WORKSPACE / WORKDIR / task_id / 'forensic.log'
    forensic_log = ForensicLog(log_path)

    low_space_warned = False

    files_copied = 0
    files_skipped = 0
    total_bytes = 0

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

            if exclude_dirs:
                file_parts = [p.lower() for p in source_file.parts]
                if any(excluded in file_parts for excluded in exclude_dirs):
                    files_skipped += 1
                    forensic_log.file_skipped(source_file, 'excluded directory')
                    continue

            file_stat = source_file.stat()
            file_mtime = datetime.datetime.fromtimestamp(file_stat.st_mtime).date()
            file_size = file_stat.st_size

            if start_date and file_mtime < start_date:
                files_skipped += 1
                forensic_log.file_skipped(source_file, 'before date range')
                continue
            if end_date and file_mtime > end_date:
                files_skipped += 1
                forensic_log.file_skipped(source_file, 'after date range')
                continue
            if size_min and file_size < size_min:
                files_skipped += 1
                forensic_log.file_skipped(source_file, 'below size minimum')
                continue
            if size_max and file_size > size_max:
                files_skipped += 1
                forensic_log.file_skipped(source_file, 'above size maximum')
                continue

            try:
                if verbosity:
                    info(f'Copying: {source_file}')

                destination_file = WORKSPACE / WORKDIR / task_id / file_extension / source_file.name

                if destination_file.exists():
                    stem = source_file.stem
                    suffix = source_file.suffix
                    counter = 1
                    while destination_file.exists():
                        destination_file = WORKSPACE / WORKDIR / task_id / file_extension / f'{stem}_{counter}{suffix}'
                        counter += 1
                    if verbosity:
                        warning(f'Name collision resolved: {source_file.name} -> {destination_file.name}')

                copy_function(source_file, destination_file)

                file_hash = None
                if use_hashing:
                    file_hash = compute_hash(destination_file, hash_algorithm)

                manifest_entries.append({
                    'original_path': str(source_file),
                    'destination_path': str(destination_file),
                    'file_size': file_size,
                    'modified_at': file_mtime.isoformat(),
                    'copied_at': datetime.datetime.now().isoformat(),
                    'hash': file_hash
                })

                forensic_log.file_copied(source_file, destination_file, file_hash)

                files_copied += 1
                total_bytes += file_size

            except (IOError, OSError) as e:
                if verbosity:
                    error(f'Failed to copy {source_file}: {e}')
                forensic_log.file_error(source_file, str(e))

    if verbosity:
        success('File collection complete.')
        info(f'Files copied: {files_copied}')
        info(f'Files skipped: {files_skipped}')
        if total_bytes < 1024 * 1024:
            info(f'Total size: {total_bytes / 1024:.1f} KB')
        elif total_bytes < 1024 * 1024 * 1024:
            info(f'Total size: {total_bytes / (1024 * 1024):.1f} MB')
        else:
            info(f'Total size: {total_bytes / (1024 * 1024 * 1024):.2f} GB')

    forensic_log.complete(files_copied, files_skipped, total_bytes)

    if verbosity:
        success(f'Forensic log saved: {log_path.name}')

    manifest_path = WORKSPACE / WORKDIR / task_id / 'manifest.json'
    manifest_file, manifest_checksum = create_manifest(manifest_entries, task_id, manifest_path, hash_algorithm if use_hashing else 'none')
    if verbosity:
        success(f'Forensic manifest saved: {manifest_path.name}')
        info(f'Manifest checksum (SHA-256): {manifest_checksum}')

    return True


def archive_output(task_id, verbosity):
    task_dir = WORKSPACE / WORKDIR / task_id
    archive_path = WORKSPACE / WORKDIR / f'{task_id}.zip'

    if verbosity:
        info(f'Creating archive: {archive_path.name}')

    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in task_dir.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(task_dir)
                zf.write(file, arcname)

    if verbosity:
        archive_size = archive_path.stat().st_size
        if archive_size < 1024 * 1024:
            success(f'Archive created: {archive_path.name} ({archive_size / 1024:.1f} KB)')
        elif archive_size < 1024 * 1024 * 1024:
            success(f'Archive created: {archive_path.name} ({archive_size / (1024 * 1024):.1f} MB)')
        else:
            success(f'Archive created: {archive_path.name} ({archive_size / (1024 * 1024 * 1024):.2f} GB)')

    return archive_path

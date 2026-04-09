import argparse
from argparse import RawTextHelpFormatter
import sys
import uuid
from pathlib import Path
from hypoxia import __version__
from hypoxia.utils import prepare_workspace, collect_files, archive_output
from hypoxia.colors import info, error
from hypoxia.forensic import parse_resume_log


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
  Directory exclusion:  --exclude
  Archive output:       --zip
  Hashing:              --hash
  Resume:               --resume
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
    parser.add_argument(
        '--exclude',
        type=str,
        required=False,
        help='Comma-separated list of directory names to exclude from scan (e.g., "windows,program files,.git").'
    )
    parser.add_argument(
        '--zip',
        action='store_true',
        default=False,
        help='Compress the output folder into a .zip archive after collection is complete.'
    )
    parser.add_argument(
        '--hash',
        type=str,
        choices=['sha256', 'none'],
        default='sha256',
        help='Hash algorithm for forensic manifest (default: sha256). Use "none" to disable hashing.'
    )
    parser.add_argument(
        '--resume',
        type=str,
        required=False,
        help='Path to a forensic log file from a previous interrupted run. Resumes collection from where it stopped.'
    )

    args = parser.parse_args()

    verbosity = (args.verbosity == 'info')
    keep_metadata = (args.keep_metadata == 'yes')

    try:
        target_extensions = args.extensions.split(',')
    except Exception as e:
        error('Invalid --extensions format. Expected a comma-separated list.')
        sys.exit(1)

    exclude_dirs = [d.strip().lower() for d in args.exclude.split(',')] if args.exclude else []

    resumed_files = {}
    if args.resume:
        resume_path = Path(args.resume)
        if not resume_path.exists():
            error(f'Resume log not found: "{args.resume}"')
            sys.exit(1)
        if verbosity:
            info(f'Resuming from: {args.resume}')
        resumed_files = parse_resume_log(resume_path)
        if verbosity:
            info(f'Previously completed files: {len(resumed_files)}')

    if verbosity:
        info('Initializing Hypoxia...')
        info(f'Task ID: {task_id}')

    preparation_result = prepare_workspace(task_id, target_extensions, verbosity)
    if preparation_result:
        result = collect_files(
            task_id, target_extensions, verbosity, keep_metadata, args.search_path, args.date_from, args.date_to, args.size_min, args.size_max, exclude_dirs, args.hash, resumed_files
        )

    if result:
        if args.zip:
            archive_path = archive_output(task_id, verbosity)
        if verbosity:
            info('Extraction task completed successfully.')import argparse
from argparse import RawTextHelpFormatter
import sys
import uuid
from pathlib import Path
from hypoxia import __version__
from hypoxia.utils import prepare_workspace, collect_files, archive_output
from hypoxia.colors import info, error
from hypoxia.forensic import parse_resume_log


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
  Directory exclusion:  --exclude
  Archive output:       --zip
  Hashing:              --hash
  Resume:               --resume
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
    parser.add_argument(
        '--exclude',
        type=str,
        required=False,
        help='Comma-separated list of directory names to exclude from scan (e.g., "windows,program files,.git").'
    )
    parser.add_argument(
        '--zip',
        action='store_true',
        default=False,
        help='Compress the output folder into a .zip archive after collection is complete.'
    )
    parser.add_argument(
        '--hash',
        type=str,
        choices=['sha256', 'sha512', 'md5', 'none'],
        default='sha256',
        help='Hash algorithm for forensic manifest (default: sha256). Use "none" to disable hashing.'
    )
    parser.add_argument(
        '--resume',
        type=str,
        required=False,
        help='Path to a forensic log file from a previous interrupted run. Resumes collection from where it stopped.'
    )

    args = parser.parse_args()

    verbosity = (args.verbosity == 'info')
    keep_metadata = (args.keep_metadata == 'yes')

    try:
        target_extensions = args.extensions.split(',')
    except Exception as e:
        error('Invalid --extensions format. Expected a comma-separated list.')
        sys.exit(1)

    exclude_dirs = [d.strip().lower() for d in args.exclude.split(',')] if args.exclude else []

    resumed_files = {}
    if args.resume:
        resume_path = Path(args.resume)
        if not resume_path.exists():
            error(f'Resume log not found: "{args.resume}"')
            sys.exit(1)
        if verbosity:
            info(f'Resuming from: {args.resume}')
        resumed_files = parse_resume_log(resume_path)
        if verbosity:
            info(f'Previously completed files: {len(resumed_files)}')

    if verbosity:
        info('Initializing Hypoxia...')
        info(f'Task ID: {task_id}')

    preparation_result = prepare_workspace(task_id, target_extensions, verbosity)
    if preparation_result:
        result = collect_files(
            task_id, target_extensions, verbosity, keep_metadata, args.search_path, args.date_from, args.date_to, args.size_min, args.size_max, exclude_dirs, args.hash, resumed_files
        )

    if result:
        if args.zip:
            archive_path = archive_output(task_id, verbosity)
        if verbosity:
            info('Extraction task completed successfully.')

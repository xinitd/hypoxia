import shutil
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

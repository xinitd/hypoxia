import os
import glob
import shutil


WORKSPACE = os.getcwd()
workdir = 'data'


def prepare_workspace(task_id, file_extensions, verbosity):
    if verbosity:
        print('Preparing environment. Please wait...')
    os.makedirs(WORKSPACE + '/' + workdir, exist_ok=True)
    os.makedirs(WORKSPACE + '/' + workdir + '/' + task_id, exist_ok=True)

    for file_extension in file_extensions:
        os.makedirs(WORKSPACE + '/' + workdir + '/' + task_id + '/' + file_extension)
    if verbosity:
        print('Environment ready.')
    return True


def copy(task_id, file_extensions, verbosity, keep_metadata, search_path):
    if verbosity:
        print('Started search at ' + search_path)

    for file_extension in file_extensions:
        files = glob.glob(search_path + '/**/*.{}'.format(file_extension), recursive=True)
        for file in files:
            if keep_metadata:
                try:
                    if verbosity:
                        print('Copying: ' + file)
                    shutil.copy2(file, WORKSPACE + '/' + workdir + '/' + task_id + '/' + file_extension + '/' + os.path.basename(file), follow_symlinks=True)
                except Exception as e:
                    if verbosity:
                        print('Something went wrong.')
            else:
                try:
                    if verbosity:
                        print('Copying: ' + file)
                    shutil.copy(file, WORKSPACE + '/' + workdir + '/' + task_id + '/' + file_extension + '/' + os.path.basename(file), follow_symlinks=True)
                except Exception as e:
                    if verbosity:
                        print('Something went wrong.')
    if verbosity:
        print('Copying done.')
    return True

import os
import sys
import pathlib

__all__ = ['get_base_path', 'get_storage_path', 'alter_last_path', 'join_path']


def get_base_path() -> pathlib.Path:
    """
    Return absolute base path and set it on python path variable
    if it is not in python path variable.
    """
    # Get this path.
    initial_path = os.getcwd()
    
    # Define few variables to use later.
    base_path = None
    split_initial_path = None

    while base_path is None or not split_initial_path[0]:
        # Split the initial path in two slices.
        split_initial_path = os.path.split(initial_path)

        if split_initial_path[-1] == 'sakurajima':
            base_path = split_initial_path[0]
        else:
            initial_path = split_initial_path[0]

    if not (path := pathlib.Path(base_path)) in sys.path and base_path is not None:
        sys.path.insert(0, path)

    return base_path


def get_storage_path() -> pathlib.Path:
    """
    Return the absolute path of database storage.
    """
    BASE_PATH = get_base_path()
    STORAGE_PATH = os.path.join(BASE_PATH, 'sakurajima/appstorage')
    return pathlib.Path(STORAGE_PATH)


def alter_last_path(initial_path: str or pathlib.Path, new_path: str) -> pathlib.Path:
    """
    Change the last directory|file name and return a new path with the changes.
    """
    altered_path = os.path.join(os.path.split(initial_path)[0], new_path)
    return pathlib.Path(altered_path)


def join_path(base_path: str, path: str) -> pathlib.Path:
    final_path = os.path.join(base_path, path)
    return pathlib.Path(final_path)

#!/usr/bin/env python3

import colorama
import os
import re

colorama.init()

creset = colorama.Fore.RESET
cgreen = colorama.Fore.GREEN
cred = colorama.Fore.RED

# Define patterns to search for various resolutions
resolution_patterns = {
    2160: r"(4096x2160|3840x2160|2880p|2160p|2160|1440p|4k)",
    1080: r"(1920x1080|1080p|1080)",
    720: r"(1280x720|720p|720)",
}

# Wrap each pattern to only match when isolated by non-alphanumeric chars or string boundaries
resolution_patterns = {
    res: rf"(?<![a-zA-Z0-9]){pat}(?![a-zA-Z0-9])"
    for res, pat in resolution_patterns.items()
}


def apply_resolution_rename(name, max_height):
    """
    Apply resolution substitution to a filename or directory name if an isolated
    resolution pattern greater than max_height is found.

    Args:
        name (str): The filename or directory name to process (without path).
        max_height (int): The target resolution height to substitute to.

    Returns:
        str: The renamed string if a match was found, or the original string unchanged.
    """
    for resolution, pattern in resolution_patterns.items():
        if resolution > max_height and re.search(pattern, name, re.IGNORECASE):
            return re.sub(pattern, f"{max_height}p", name, flags=re.IGNORECASE)
    return name


def deletefile(filepath):
    """Delete a file, Returns a boolean

    Args:
        filepath    :   A string containing the full filepath
    Returns:
        Bool        :   The success of the operation
    """
    try:
        os.remove(filepath)
    except OSError:
        print(f"{cred}Error deleting {filepath}{creset}")
        return False

    print(f"{cgreen}Successfully deleted {filepath}{creset}")
    return True


def get_intermediate_dirs(input_path, file_path):
    """
    Return the list of directory paths between input_path (exclusive) and
    the directory containing file_path (inclusive), ordered deepest first.

    Args:
        input_path (str): The root path (exclusive upper bound).
        file_path (str): The full path to a file.

    Returns:
        list: List of directory paths, deepest first.

    Raises:
        ValueError: If file_path not under input_path.
    """
    input_path = os.path.realpath(input_path)
    current = os.path.realpath(os.path.dirname(file_path))

    if current != input_path and not current.startswith(input_path + os.sep):
        raise ValueError(
            f"file_path '{file_path}' is not under input_path '{input_path}'"
        )

    dirs = []

    while current != input_path and current != os.path.dirname(current):
        dirs.append(current)
        current = os.path.dirname(current)

    return dirs


def findfreename(filepath, attempt=0):
    """
    Given a filepath, it will try to find a free filename by appending a number to the name.
    First, it tries using the filepath passed in the argument, then adds a number to the end. If all fail, it appends (#).

    Args:
        filepath (str): A string containing the full filepath.
        attempt (int): The number of attempts already made to find a free filename.

    Returns:
        str: The first free filepath found.
    """
    attempt += 1
    filename = str(filepath)[: str(filepath).rindex(".")]
    extension = str(filepath)[str(filepath).rindex(".") :]
    copynumpath = filename + f"({attempt})" + extension

    if not os.path.exists(filepath) and attempt <= 2:
        return filepath
    elif not os.path.exists(copynumpath):
        return copynumpath
    return findfreename(filepath, attempt)


def get_spacer(name: str) -> str:
    """
    Determine the spacer character ('-' or '_') to use for naming a virtual environment
    based on the given project name. Default to underscore.

    Args:
        name (str): The project name to analyze.

    Returns:
        str: The detected spacer ('-' or '_'), or '_' if none found.
    """
    if "-" in name:
        return "-"
    elif "_" in name:
        return "_"
    return "_"

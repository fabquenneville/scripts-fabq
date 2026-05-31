#!/usr/bin/env python3
# video_autoreduce_rename.py

import argparse
import argcomplete
import colorama
import os
import sys
from pathlib import Path

# Allow importing from scripts/library even when run directly
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# === Local import ===
from scripts.library import apply_resolution_rename

colorama.init()

creset = colorama.Fore.RESET
ccyan = colorama.Fore.CYAN
cyellow = colorama.Fore.YELLOW
cgreen = colorama.Fore.GREEN
cred = colorama.Fore.RED


def autorename(input_path, max_height=720, debug=False):
    """
    Rename video files and folders in the specified directory tree that contain a resolution
    in their name to the specified max_height resolution.

    Args:
        input_path (str): The path of the directory to search for video files and folders.
        max_height (int, optional): The maximum height (in pixels) of the video to consider for conversion. Default is 720.
        debug (bool, optional): If True, print debug messages. Default is False.
    """

    files_to_rename = []
    dirs_to_rename = []

    for dirpath, dirnames, filenames in os.walk(input_path, topdown=True):
        # Collect files to rename
        for filename in filenames:
            new_filename = apply_resolution_rename(filename, max_height)
            if new_filename != filename:
                old_file = os.path.join(dirpath, filename)
                new_file = os.path.join(dirpath, new_filename)
                files_to_rename.append((old_file, new_file))

        # Collect directories to rename
        for dirname in dirnames:
            new_dirname = apply_resolution_rename(dirname, max_height)
            if new_dirname != dirname:
                old_dir = os.path.join(dirpath, dirname)
                new_dir = os.path.join(dirpath, new_dirname)
                dirs_to_rename.append((old_dir, new_dir))

    # Rename files first
    for old_file, new_file in files_to_rename:
        if os.path.exists(new_file):
            print(f"Error: Target filename {new_file} already exists.")
            continue
        os.rename(old_file, new_file)
        if debug:
            print(f"Renamed file: {old_file} -> {new_file}")

    # Rename directories after
    for old_dir, new_dir in sorted(dirs_to_rename, key=lambda x: -len(x[0])):
        if os.path.exists(new_dir):
            print(f"Error: Target directory name {new_dir} already exists.")
            continue
        os.rename(old_dir, new_dir)
        if debug:
            print(f"Renamed directory: {old_dir} -> {new_dir}")


def main():
    """
    Main function to parse command line arguments and initiate file renamings.
    """

    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Rename video files containing resolutions in their filenames to a specified max_height resolution."
    )

    # Define command line arguments
    parser.add_argument(
        "input_path",
        nargs="?",
        default=os.getcwd(),
        help="directory path to search for video files (default: current directory)",
    )
    parser.add_argument(
        "-mh",
        "--max-height",
        type=int,
        default=720,
        help="maximum height of videos to be converted (default: 720)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable debug mode for printing additional messages",
    )

    # Enable autocomplete for argparse
    argcomplete.autocomplete(parser)

    # Parse command line arguments
    args = parser.parse_args()

    # Rename videos
    autorename(args.input_path, args.max_height, args.debug)


if __name__ == "__main__":
    # Execute main function when the script is run directly
    main()

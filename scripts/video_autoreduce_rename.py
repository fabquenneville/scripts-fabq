#!/usr/bin/env python3
# video_autoreduce_rename.py

import argparse
import argcomplete
import colorama
import os
import re

colorama.init()

creset = colorama.Fore.RESET
ccyan = colorama.Fore.CYAN
cyellow = colorama.Fore.YELLOW
cgreen = colorama.Fore.GREEN
cred = colorama.Fore.RED


def autorename(input_path, max_height=720, debug=False):
    '''
    Rename video files and folders in the specified directory tree that contain a resolution
    in their name to the specified max_height resolution.

    Args:
        input_path (str): The path of the directory to search for video files and folders.
        max_height (int, optional): The maximum height (in pixels) of the video to consider for conversion. Default is 720.
        debug (bool, optional): If True, print debug messages. Default is False.
    '''
    # Define patterns to search for various resolutions
    resolution_patterns = {
        2160: r'(4096x2160|3840x2160|2880p|2160p|2160|1440p|4k)',
        1080: r'(1920x1080|1080p|1080)',
        720: r'(1280x720|720p|720)',
    }

    files_to_rename = []
    dirs_to_rename = []

    for dirpath, dirnames, filenames in os.walk(input_path, topdown=True):
        # Collect files to rename
        for filename in filenames:
            for resolution, pattern in resolution_patterns.items():
                # Only process resolutions greater than max_height
                if resolution > max_height and re.search(
                        pattern, filename, re.IGNORECASE):
                    old_file = os.path.join(dirpath, filename)
                    new_filename = re.sub(pattern,
                                          f'{max_height}p',
                                          filename,
                                          flags=re.IGNORECASE)
                    new_file = os.path.join(dirpath, new_filename)
                    if old_file != new_file:
                        files_to_rename.append((old_file, new_file))
                    break

        # Collect directories to rename
        for dirname in dirnames:
            for resolution, pattern in resolution_patterns.items():
                # Only process resolutions greater than max_height
                if resolution > max_height and re.search(
                        pattern, dirname, re.IGNORECASE):
                    old_dir = os.path.join(dirpath, dirname)
                    new_dirname = re.sub(pattern,
                                         f'{max_height}p',
                                         dirname,
                                         flags=re.IGNORECASE)
                    new_dir = os.path.join(dirpath, new_dirname)
                    if old_dir != new_dir:
                        dirs_to_rename.append((old_dir, new_dir))
                    break

    # Rename files first
    for old_file, new_file in files_to_rename:
        if os.path.exists(new_file):
            print(f"Error: Target filename {new_file} already exists.")
            continue
        os.rename(old_file, new_file)
        if debug:
            print(f'Renamed file: {old_file} -> {new_file}')

    # Rename directories after
    for old_dir, new_dir in sorted(dirs_to_rename, key=lambda x: -len(x[0])):
        if os.path.exists(new_dir):
            print(f"Error: Target directory name {new_dir} already exists.")
            continue
        os.rename(old_dir, new_dir)
        if debug:
            print(f'Renamed directory: {old_dir} -> {new_dir}')


def main():
    '''
    Main function to parse command line arguments and initiate file renamings.
    '''

    # Create argument parser
    parser = argparse.ArgumentParser(
        description=
        'Rename video files containing resolutions in their filenames to a specified max_height resolution.'
    )

    # Define command line arguments
    parser.add_argument(
        'input_path',
        nargs='?',
        default=os.getcwd(),
        help=
        'directory path to search for video files (default: current directory)'
    )
    parser.add_argument(
        '-mh',
        '--max-height',
        type=int,
        default=720,
        help='maximum height of videos to be converted (default: 720)')
    parser.add_argument(
        '--debug',
        action='store_true',
        help='enable debug mode for printing additional messages')

    # Enable autocomplete for argparse
    argcomplete.autocomplete(parser)

    # Parse command line arguments
    args = parser.parse_args()

    # Rename videos
    autorename(args.input_path, args.max_height, args.debug)


if __name__ == "__main__":
    # Execute main function when the script is run directly
    main()

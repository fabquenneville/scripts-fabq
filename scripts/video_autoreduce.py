#!/usr/bin/env python3
# video_autoreduce.py

import argparse
import colorama
import os
import re
import subprocess
import sys
import json

colorama.init()

creset = colorama.Fore.RESET
ccyan = colorama.Fore.CYAN
cyellow = colorama.Fore.YELLOW
cgreen = colorama.Fore.GREEN
cred = colorama.Fore.RED


def get_ffmpeg_codecs(codec_type="S"):
    """
    Retrieve a list of supported codecs for a specific type from ffmpeg.

    This function runs the `ffmpeg -codecs` command and parses its output to extract
    the list of supported codecs based on the provided `codec_type` (e.g., 'S' for subtitles,
    'V' for video, 'A' for audio). The list of codecs is returned as a set for efficient lookup.

    Args:
        codec_type (str): The type of codecs to retrieve. 
                          - "S" for subtitles (default)
                          - "V" for video
                          - "A" for audio
                          - "D" for data
                          - "T" for attachment

    Returns:
        set: A set of codec names of the specified type.
             If an error occurs or no codecs are found, an empty set is returned.
    """
    try:
        # Run ffmpeg -codecs
        result = subprocess.run(["ffmpeg", "-codecs"],
                                capture_output=True,
                                text=True,
                                check=True)
        output = result.stdout

        # Extract codecs using regex
        codec_pattern = re.compile(rf"^[ D.E]+{codec_type}[ A-Z.]+ (\S+)",
                                   re.MULTILINE)
        codecs = codec_pattern.findall(output)

        return set(codecs)  # Return as a set for easy lookup

    except subprocess.CalledProcessError as e:
        print("Error running ffmpeg:", e)
        return set()


def findfreename(filepath, attempt=0):
    ''' 
    Given a filepath, it will try to find a free filename by appending a number to the name.
    First, it tries using the filepath passed in the argument, then adds a number to the end. If all fail, it appends (#).

    Args:
        filepath (str): A string containing the full filepath.
        attempt (int): The number of attempts already made to find a free filename.

    Returns:
        str: The first free filepath found.
    '''
    attempt += 1
    filename = str(filepath)[:str(filepath).rindex(".")]
    extension = str(filepath)[str(filepath).rindex("."):]
    copynumpath = filename + f"({attempt})" + extension

    if not os.path.exists(filepath) and attempt <= 2:
        return filepath
    elif not os.path.exists(copynumpath):
        return copynumpath
    return findfreename(filepath, attempt)


def deletefile(filepath):
    '''Delete a file, Returns a boolean

    Args:
        filepath    :   A string containing the full filepath
    Returns:
        Bool        :   The success of the operation
    '''
    try:
        os.remove(filepath)
    except OSError:
        print(f"{cred}Error deleting {filepath}{creset}")
        return False

    print(f"{cgreen}Successfully deleted {filepath}{creset}")
    return True


def ensure_output_path(output_path):
    '''
    Ensure that the output directory exists. If it doesn't, attempt to create it.

    Args:
        output_path (str): The path of the output directory to be ensured.

    Returns:
        None
    '''
    try:
        os.makedirs(output_path, exist_ok=True)
        # Attempts to create the output directory if it doesn't exist.
        # exist_ok=True ensures that an OSError is not raised if the directory already exists.
    except OSError as e:
        # If an OSError occurs during directory creation, print an error message and exit the program.
        print(f"{cred}Failed to create output directory:{creset} {e}",
              file=sys.stderr)
        sys.exit(1)


def has_supported_subs(video_file, supported_subtitle_codecs, debug=False):
    """
    Check if the given video file contains subtitles in a supported codec.

    This function uses `ffprobe` to extract subtitle stream information from the 
    video file and checks whether any subtitle stream has a codec that matches 
    one of the supported codecs provided in the `supported_subtitle_codecs` list.

    Args:
        video_file (str): Path to the video file to be checked.
        supported_subtitle_codecs (set): Set of subtitle codec names that are considered supported.
        debug (bool): If True, prints debug information for errors. Defaults to False.

    Returns:
        bool: True if at least one subtitle stream is found with a supported codec, 
              False otherwise or in case of an error.
    """
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-select_streams', 's', '-show_entries',
            'stream=index,codec_name', '-of', 'json', video_file
        ],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)

        if result.returncode != 0:
            if debug:
                print(f"ffprobe error: {result.stderr.strip()}")
            return False  # Assume no supported subtitles on failure

        try:
            streams = json.loads(result.stdout).get("streams", [])
        except json.JSONDecodeError as e:
            if debug:
                print(f"JSON parsing error: {e}")
            return False  # Assume no supported subtitles if JSON is malformed

        return any(
            stream.get("codec_name") in supported_subtitle_codecs
            for stream in streams)

    except Exception as e:
        if debug:
            print(f"Unexpected error: {e}")
        return False  # Assume no supported subtitles


def find_videos_to_convert(input_path, max_height=720, debug=False):
    '''
    Find video files in the specified directory tree that meet conversion criteria.

    Args:
        input_path (str): The path of the directory to search for video files.
        max_height (int, optional): The maximum height (in pixels) of the video to consider for conversion. Default is 720.
        debug (bool, optional): If True, print debug messages. Default is False.

    Returns:
        list: A list of paths to video files that meet the conversion criteria.
    '''
    # Print a message indicating the start of the scanning process
    print(
        f"{cgreen}Scanning {input_path} for video files to convert.{creset}\n")

    # Initialize lists to store all video files and valid video files
    video_files = []
    valid_videos_files = []

    # Find all video files in the directory tree
    for root, dirs, files in os.walk(input_path):
        for file in files:
            fullpath = os.path.join(root, file)
            # Check if the file is a video file with one of the specified extensions
            if (file.lower().endswith(
                ('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.divx'))
                    and os.path.isfile(fullpath)):
                video_files.append(fullpath)

    # List of encodings to try for decoding output from ffprobe
    ENCODINGS_TO_TRY = ['utf-8', 'latin-1', 'iso-8859-1']

    # Iterate through each video file
    for video_file in video_files:
        try:
            # Run ffprobe command to get video resolution
            resolution_output = subprocess.check_output(
                [
                    'ffprobe', '-v', 'error', '-select_streams', 'v:0',
                    '-show_entries', 'stream=width,height', '-of', 'csv=p=0',
                    video_file
                ],
                stderr=subprocess.STDOUT)

            # Attempt to decode the output using different encodings
            dimensions_str = None
            for encoding in ENCODINGS_TO_TRY:
                try:
                    dimensions_str = resolution_output.decode(
                        encoding).strip().rstrip(',')

                    dimensions = [
                        int(d) for d in dimensions_str.split(',')
                        if d.strip().isdigit()
                    ]
                    if len(dimensions) >= 2:
                        width, height = dimensions[:2]
                    else:
                        raise ValueError(
                            f"Unexpected dimensions format: {dimensions_str}")
                    break  # Stop trying encodings once successful decoding and conversion
                except (UnicodeDecodeError, ValueError):
                    continue  # Try the next encoding

            # If decoding was unsuccessful with all encodings, skip this video
            if dimensions_str is None:
                if debug:
                    print(
                        f"{cred}Error processing {video_file}: Unable to decode output from ffprobe using any of the specified encodings.{creset}",
                        file=sys.stderr)
                continue  # Skip this video and continue with the next one

            # Ignore vertical videos
            if height > width:
                continue  # Skip this video and continue with the next one

            # Check if the video height exceeds the maximum allowed height
            if height > max_height:
                valid_videos_files.append(video_file)

        except subprocess.CalledProcessError as e:
            if debug:
                # Print error message if subprocess call fails
                if e.output is not None:
                    decoded_error = e.output.decode("utf-8")
                    print(
                        f"{cred}Error processing {video_file}: {decoded_error}{creset}\n",
                        file=sys.stderr)
                else:
                    print(
                        f"{cred}Error processing {video_file}: No output from subprocess{creset}\n",
                        file=sys.stderr)
        except ValueError as e:
            if debug:
                # Print error message if value error occurs during decoding
                print(
                    f"{cred}Error processing {video_file}: ValueError decoding the file{creset}\n",
                    file=sys.stderr)

    valid_videos_files.sort()

    return valid_videos_files


def convert_videos(input_path, output_path, max_height=720, debug=False):
    '''
    Convert videos taller than a specified height to 720p resolution with x265 encoding and MKV container.

    Args:
        input_path (str): The path of the directory containing input video files.
        output_path (str): The path of the directory where converted video files will be saved.
        max_height (int, optional): The maximum height (in pixels) of the video to consider for conversion. Default is 720.
        debug (bool, optional): If True, print debug messages. Default is False.

    Returns:
        bool: True if conversion succeeds, False otherwise.
    '''

    # Get supported subtitle codecs
    supported_subtitle_codecs = get_ffmpeg_codecs("S")

    # Find video files to convert in the input directory
    video_files = find_videos_to_convert(input_path, max_height, debug)
    counter = 0

    # If no video files found, print a message and return False
    if len(video_files) == 0:
        print(f"No video files to convert found.\n")
        return False

    # Ensure the output directory exists
    ensure_output_path(output_path)

    # Print a message indicating the start of the conversion process
    print(
        f"Converting {len(video_files)} videos taller than {max_height} pixels to 720p resolution with x265 encoding and MKV container...\n"
    )

    # Variable to keep a track of the current_file in case of failure
    current_file = None

    # Iterate through each video file for conversion
    for video_file in video_files:
        counter += 1

        # Print conversion progress information
        print(
            f"{cgreen}******  Starting conversion {counter} of {len(video_files)}: '{os.path.basename(video_file)}'...{creset}"
        )
        print(f"{ccyan}Original file:{creset}")
        print(video_file)

        # Generate output file path and name
        output_file = findfreename(
            os.path.join(
                output_path,
                os.path.splitext(os.path.basename(video_file))[0] + '.mkv'))

        try:
            # Get original video width and height
            video_info = subprocess.run([
                'ffprobe', '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height', '-of', 'csv=p=0',
                video_file
            ],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True)
            width, height = map(
                int,
                video_info.stdout.strip().rstrip(',').split(','))

            # Calculate the scaled width maintaining aspect ratio
            scaled_width = int(max_height * (width / height))
            # Ensure the width is even
            if scaled_width % 2 != 0:
                scaled_width += 1

            # Keep a track of the current_file in case of failure
            current_file = output_file

            # Check if the video has supported subtitles
            include_subs = has_supported_subs(video_file,
                                              supported_subtitle_codecs, debug)

            # Construct the FFmpeg command dynamically
            ffmpeg_command = [
                'ffmpeg', '-n', '-i', video_file, '-map', '0:v', '-c:v',
                'libx265', '-vf', f'scale={scaled_width}:{max_height}',
                '-preset', 'medium', '-crf', '28', '-map', '0:a?', '-c:a',
                'copy'
            ]

            # Only include subtitles if they are supported
            if include_subs:
                ffmpeg_command.extend(['-map', '0:s?', '-c:s', 'copy'])

            ffmpeg_command.append(output_file)

            # Print the FFmpeg command as a single string
            if (debug):
                print("FFmpeg command: " + ' '.join(ffmpeg_command))

            # Run the FFmpeg command
            process = subprocess.run(ffmpeg_command,
                                     check=True,
                                     stdout=subprocess.DEVNULL,
                                     stderr=subprocess.STDOUT)

            # Check if ffmpeg process returned successfully
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode,
                                                    process.args,
                                                    output=process.stderr)

        except subprocess.CalledProcessError as e:
            # If we have a partial video converted, delete it due to the failure
            if current_file:
                deletefile(current_file)

            # Handle subprocess errors
            if debug:
                if e.output is not None:
                    decoded_error = e.output.decode("utf-8")
                    print(
                        f"{cred}Error processing {video_file}: {decoded_error}{creset}\n",
                        file=sys.stderr)
                else:
                    print(
                        f"{cred}Error processing {video_file}: No output from subprocess{creset}\n",
                        file=sys.stderr)

        except KeyboardInterrupt:
            print(f"{cyellow}Conversions cancelled, cleaning up...{creset}")

            # If we have a partial video converted, delete it due to the failure
            if current_file:
                deletefile(current_file)
                current_file = None

            exit()

        except Exception as e:
            # If we have a partial video converted, delete it due to the failure
            if current_file:
                deletefile(current_file)

            # Handle other exceptions
            if debug:
                print(
                    f"{cred}Error processing {video_file}: {str(e)}{creset}\n",
                    file=sys.stderr)

        else:

            # Print success message if conversion is successful
            print(
                f"{ccyan}Successfully converted video to output file:{creset}")
            print(f"{output_file}\n")

            try:
                os.chmod(output_file, 0o777)
            except PermissionError:
                print(f"{cred}PermissionError on: '{output_file}'{creset}")

            # Remove the now succefully converted filepath
            current_file = None

    return True


def main():
    '''
    Main function to parse command line arguments and initiate video conversion.
    '''

    # Create argument parser
    parser = argparse.ArgumentParser(
        description=
        'Convert videos taller than a certain height to 720p resolution with x265 encoding and MKV container.'
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
        '-o',
        '--output-path',
        default=os.path.join(os.getcwd(), 'converted'),
        help='directory path to save converted videos (default: ./converted)')
    parser.add_argument(
        '-mh',
        '--max-height',
        type=int,
        default=720,
        help='maximum height of videos to be converted (default: 720)')
    parser.add_argument(
        '--debug',
        action='store_true',
        help='enable debug mode for printing additional error messages')

    # Parse command line arguments
    args = parser.parse_args()

    # Convert videos
    convert_videos(args.input_path, args.output_path, args.max_height,
                   args.debug)


if __name__ == "__main__":
    # Execute main function when the script is run directly
    main()

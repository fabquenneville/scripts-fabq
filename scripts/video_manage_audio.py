#!/usr/bin/env python3
# video_manage_audio.py

import argparse
import argcomplete
import colorama
import os
import subprocess

# Initialize colorama for colored output in the terminal
colorama.init()

creset = colorama.Fore.RESET
ccyan = colorama.Fore.CYAN
cyellow = colorama.Fore.YELLOW
cgreen = colorama.Fore.GREEN
cred = colorama.Fore.RED


def process_audio(file_path, track, command):
    """
    Modify audio tracks of a video file based on the given command.
    - 'remove': Remove the specified audio track while keeping everything else.
    - 'keep': Keep only the specified audio track and remove all others.
    The function preserves video, subtitles, and metadata.
    """
    print(f"{cgreen}Processing file: {file_path}{creset}")
    output_file = f"{os.path.splitext(file_path)[0]}_{command}_audio{os.path.splitext(file_path)[1]}"

    # Construct ffmpeg command based on user choice
    if command == "remove":
        # Remove only the specified audio track while keeping all other streams
        ffmpeg_command = [
            "ffmpeg", "-i", file_path, "-map", "0", "-map", f"-0:a:{track}",
            "-c", "copy", output_file
        ]
    elif command == "keep":
        # Keep only the specified audio track while preserving video, subtitles, and metadata
        ffmpeg_command = [
            "ffmpeg", "-i", file_path, "-map", "0:v", "-map", f"0:a:{track}",
            "-map", "0:s?", "-map", "0:t?", "-c", "copy", output_file
        ]
    else:
        print(f"{cred}Invalid command: {command}{creset}")
        return

    try:
        # Execute the ffmpeg command and capture output
        result = subprocess.run(ffmpeg_command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)

        if result.returncode == 0:
            print(
                f"{ccyan}Audio processing complete. Output saved to {output_file}{creset}\n"
            )
        else:
            print(
                f"{cred}Command failed with return code {result.returncode}{creset}\n"
            )
            print(f"{cred}Error output:\n{result.stderr}{creset}\n")

    except subprocess.CalledProcessError as e:
        print(f"{cred}Error processing audio: {e}{creset}\n")


def process_directory(dir_path, track, command):
    """
    Recursively processes all video files in the specified directory.
    Applies the chosen audio modification (remove or keep) to each file.
    """
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith((".mp4", ".mkv", ".avi", ".mov")):
                file_path = os.path.join(root, file)
                process_audio(file_path, track, command)


def main():
    """
    Main function to parse command-line arguments and initiate the audio processing.
    """

    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Manage audio tracks in video files.")

    # Define command line arguments
    # Add a positional argument for the command
    parser.add_argument('command',
                        choices=['remove', 'keep'],
                        help='Command to run')

    # Add other arguments with both short and long options, including defaults
    parser.add_argument("--track",
                        type=int,
                        default=0,
                        help="Audio track index (default is 0).")
    parser.add_argument("--file",
                        type=str,
                        help="Path to a specific video file.")
    parser.add_argument(
        "--dir",
        type=str,
        default=os.getcwd(),
        help="Directory to process (default is current directory).")

    # Enable autocomplete for command-line arguments
    argcomplete.autocomplete(parser)

    # Parse command line arguments
    args = parser.parse_args()

    # Process a single file if provided, otherwise process a directory
    if args.file:
        if os.path.isfile(args.file):
            process_audio(args.file, args.track, args.command)
        else:
            print(f"{cred}File {args.file} does not exist.{creset}")
    else:
        if os.path.isdir(args.dir):
            process_directory(args.dir, args.track, args.command)
        else:
            print(f"{cred}Directory {args.dir} does not exist.{creset}")


if __name__ == "__main__":
    main()

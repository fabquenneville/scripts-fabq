#!/usr/bin/env python3

import os
import argparse
import argcomplete
import colorama
import subprocess

colorama.init()

creset = colorama.Fore.RESET
ccyan = colorama.Fore.CYAN
cyellow = colorama.Fore.YELLOW
cgreen = colorama.Fore.GREEN
cred = colorama.Fore.RED


# Function to remove audio track from a video using ffmpeg
def remove_audio_track(file_path, track):
    print(f"{cgreen}Processing file: {file_path}{creset}")
    output_file = f"{os.path.splitext(file_path)[0]}_no_audio{os.path.splitext(file_path)[1]}"
    # ffmpeg command to remove the specified audio track and keep other streams
    command = [
        "ffmpeg", "-i", file_path, "-map", "0", "-map", f"-0:a:{track}", "-c",
        "copy", output_file
    ]

    try:
        result = subprocess.run(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)

        if result.returncode == 0:
            print(
                f"{ccyan}Audio track {track} removed. Output saved to {output_file}{creset}\n"
            )
        else:
            print(
                f"{cred}Command failed with return code {result.returncode}{creset}\n"
            )
            print(f"{cred}Error output:", result.stderr, f"{creset}\n")

    except subprocess.CalledProcessError as e:
        print(f"{cred}Error removing audio track: {e}{creset}\n")


# Function to recursively process videos in a directory
def process_directory(dir_path, track):
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith((".mp4", ".mkv", ".avi",
                              ".mov")):  # Add more formats as needed
                file_path = os.path.join(root, file)
                remove_audio_track(file_path, track)


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Remove audio track from video files.")
    parser.add_argument("--track",
                        type=int,
                        default=0,
                        help="Audio track index to remove (default is 0).")
    parser.add_argument("--file",
                        type=str,
                        help="Path to a specific video file.")
    parser.add_argument(
        "--dir",
        type=str,
        default=os.getcwd(),
        help="Directory to process (default is current directory).")

    # Enable autocomplete for argparse
    argcomplete.autocomplete(parser)

    args = parser.parse_args()

    # Process single file if provided
    if args.file:
        if os.path.isfile(args.file):
            remove_audio_track(args.file, args.track)
        else:
            print(f"File {args.file} does not exist.")
    # Otherwise, process all files in the specified directory
    else:
        if os.path.isdir(args.dir):
            process_directory(args.dir, args.track)
        else:
            print(f"Directory {args.dir} does not exist.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# video_manage_audio.py

import argparse
import argcomplete
import colorama
import json
import os
import subprocess
import sys
from pathlib import Path

# Allow importing from scripts/library even when run directly
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# === Local import ===
from scripts.library import deletefile

# Initialize colorama for colored output in the terminal
colorama.init()

creset = colorama.Fore.RESET
ccyan = colorama.Fore.CYAN
cyellow = colorama.Fore.YELLOW
cgreen = colorama.Fore.GREEN
cred = colorama.Fore.RED


def get_audio_metadata(file_path):
    """
    Uses ffprobe to extract audio stream information.
    Returns a list of dicts with track details.
    """
    abs_file_path = os.path.abspath(file_path)
    ffprobe_command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a",
        "-show_entries",
        "stream=index,codec_name:stream_tags=language,title",
        "-of",
        "json",
        abs_file_path,
    ]

    try:
        result = subprocess.run(
            ffprobe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        if result.returncode != 0:
            return None
        metadata = json.loads(result.stdout)
        return metadata.get("streams", [])
    except Exception:
        return None


def list_audio_tracks(file_path):
    """Displays all audio tracks in a video file."""
    print(f"{ccyan}Analyzing tracks for: {file_path}{creset}")
    streams = get_audio_metadata(file_path)

    if streams is None:
        print(f"{cred}  Failed to read file metadata.{creset}\n")
        return
    if not streams:
        print(f"{cyellow}  No audio tracks found in this file.{creset}\n")
        return

    for audio_idx, stream in enumerate(streams):
        abs_idx = stream.get("index")
        codec = stream.get("codec_name", "unknown")
        tags = stream.get("tags", {})
        lang = tags.get("language", "und")
        title = tags.get("title", "No Title")

        print(
            f"  {cgreen}[Audio Track {audio_idx}]{creset} "
            f"Absolute Stream Index: {abs_idx} | "
            f"Codec: {codec} | Lang: {lang} | Title: {title}"
        )
    print()


def resolve_track_target(streams, target):
    """
    Resolves a track target (either an integer index string like '1'
    or a language code string like 'eng') to a relative audio track index.
    Returns None if no match is found.
    """
    # Case 1: Target is an explicit number (e.g., "0", "1")
    if target.isdigit():
        idx = int(target)
        if 0 <= idx < len(streams):
            return idx
        return None

    # Case 2: Target is a language code (e.g., "eng", "rus")
    for audio_idx, stream in enumerate(streams):
        lang = stream.get("tags", {}).get("language", "").lower()
        if lang == target.lower():
            return audio_idx

    return None


def process_audio(file_path, track_target, command):
    """Modify or list audio tracks of a video file."""
    if command == "list":
        list_audio_tracks(file_path)
        return

    streams = get_audio_metadata(file_path)
    if not streams:
        print(f"{cred}Skipping {file_path}: Could not parse audio streams.{creset}\n")
        return

    # Dynamic target resolution (converts 'eng' or '1' to the proper track index)
    resolved_track = resolve_track_target(streams, track_target)

    if resolved_track is None:
        print(
            f"{cyellow}Skipping {file_path}: Target audio track/language '{track_target}' not found.{creset}\n"
        )
        return

    print(f"{cgreen}Processing file: {file_path}{creset}")
    print(
        f"-> Target resolved to Audio Track {resolved_track} based on '{track_target}'"
    )

    output_file = f"{os.path.splitext(file_path)[0]}_{command}_audio{os.path.splitext(file_path)[1]}"

    if command == "remove":
        # Remove only the specified audio track while keeping all other streams
        ffmpeg_command = [
            "ffmpeg",
            "-i",
            file_path,
            "-map",
            "0",
            "-map",
            f"-0:a:{resolved_track}",
            "-c",
            "copy",
            output_file,
        ]
    elif command == "keep":
        # Keep only the specified audio track while preserving video, subtitles, and metadata
        ffmpeg_command = [
            "ffmpeg",
            "-i",
            file_path,
            "-map",
            "0:v",
            "-map",
            f"0:a:{resolved_track}",
            "-map",
            "0:s?",
            "-map",
            "0:t?",
            "-c",
            "copy",
            output_file,
        ]
    else:
        return

    try:
        # Keep a track of the current_file in case of failure
        current_file = output_file

        result = subprocess.run(
            ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

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
        # If we have a partial video converted, delete it due to the failure
        if current_file:
            deletefile(current_file)

    except KeyboardInterrupt:
        print(f"{cyellow}Conversions cancelled, cleaning up...{creset}")

        # If we have a partial video converted, delete it due to the failure
        if current_file:
            deletefile(current_file)
            current_file = None

        exit()

    except Exception as e:
        print(f"{cred}Error processing audio: {e}{creset}\n")


def process_directory(dir_path, track_target, command):
    """Recursively processes all video files in the specified directory."""
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith((".mp4", ".mkv", ".avi", ".mov")):
                file_path = os.path.join(root, file)
                process_audio(file_path, track_target, command)


def main():
    """
    Main function to parse command-line arguments and initiate the audio processing.
    """

    parser = argparse.ArgumentParser(
        description="Manage or list audio tracks in video files dynamically."
    )

    parser.add_argument(
        "command", choices=["remove", "keep", "list"], help="Command to run"
    )

    parser.add_argument(
        "-t",
        "--track",
        type=str,
        default="0",
        help="Audio track index (e.g., 0, 1) OR language ISO code (e.g., eng, rus). Default is '0'.",
    )
    parser.add_argument("-f", "--file", type=str, help="Path to a specific video file.")
    parser.add_argument(
        "-d",
        "--dir",
        type=str,
        default=os.getcwd(),
        help="Directory to process (default is current directory).",
    )

    argcomplete.autocomplete(parser)
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

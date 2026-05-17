#!/usr/bin/env python3
"""A utility script to repackage video files into MKV containers using FFmpeg.

This script recursively scans a specified directory for non-MKV video files
and uses FFmpeg to repackage them into '.mkv' containers. It explicitly maps
all streams (video, audio, subtitles, data) and preserves all metadata without
re-encoding. It includes options to automatically delete the source files upon
successful conversion.
"""

import argparse
import subprocess
from pathlib import Path
from typing import Sequence

# Define the targeted non-MKV extensions (case-insensitive handling below)
TARGET_EXTENSIONS = {".mp4", ".m4v", ".flv", ".avi", ".mov", ".wmv"}


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the repackaging utility.

    Args:
        args: Optional sequence of strings to parse. If None, sys.argv is used.

    Returns:
        An argparse.Namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Recursively repackage non-MKV video files into MKV containers, preserving all streams and metadata."
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=Path.cwd(),
        help="Path to the root directory to scan for video files (default: current working directory).",
    )

    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        default=False,
        help="Delete the original video files upon successful conversion.",
    )

    # Enable argcomplete support if the module is available
    try:
        import argcomplete

        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    return parser.parse_args(args)


def repackage_to_mkv(input_dir: Path, delete_source: bool) -> None:
    """Recursively scan the input directory and repackage non-MKV videos to MKV.

    Args:
        input_dir: The root Path directory to scan.
        delete_source: If True, deletes the original video file after a
            successful FFmpeg operation.
    """
    if not input_dir.is_dir():
        print(f"Error: The directory '{input_dir}' does not exist.")
        return

    print(f"Scanning '{input_dir}' recursively for video files...")

    video_files = [
        p
        for p in input_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in TARGET_EXTENSIONS
    ]

    if not video_files:
        print("No matching video files found.")
        return

    print(f"Found {len(video_files)} files to process.\n")

    for file_path in video_files:
        output_path = file_path.with_suffix(".mkv")

        if output_path.exists():
            print(
                f"Warning: Destination {output_path.name} already exists. Skipping to avoid accidental overwrite."
            )
            print("-" * 40)
            continue

        cmd = [
            "ffmpeg",
            "-i",
            str(file_path),
            "-map",
            "0",
            "-c",
            "copy",
            "-map_metadata",
            "0",
            str(output_path),
            "-loglevel",
            "error",
            "-y",
        ]

        # Display the relative path from the input directory so it's easier to track progress
        relative_display = file_path.relative_to(input_dir)
        print(f"Processing: {relative_display} -> {output_path.name}...")

        try:
            subprocess.run(cmd, check=True)
            print(f"Successfully converted: {file_path.name}")

            if delete_source:
                file_path.unlink()
                print(f"Deleted original file: {file_path.name}")

        except subprocess.CalledProcessError:
            print(f"Failed to convert: {file_path.name}")
        except OSError as e:
            print(f"System error processing {file_path.name}: {e}")

        print("-" * 40)


def main() -> None:
    """Main execution entry point."""
    args = parse_args()
    repackage_to_mkv(input_dir=args.input, delete_source=args.delete)


if __name__ == "__main__":
    main()

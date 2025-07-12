#!/usr/bin/env python3

# === Standard library ===
import sys
import os
from pathlib import Path
from typing import Optional
from argparse import ArgumentParser, Namespace

# Allow importing from scripts/library even when run directly
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# === Local import ===
from scripts.library import parse_verbose, run_in_venv


def rename_by_case(root_dir: str, case: str, recursive: bool = False) -> None:
    """
    Renames all files and directories in a given directory by changing their case.

    Args:
        root_dir (str): Root path to start renaming.
        case (str): One of "lower", "upper", "capitalize".
        recursive (bool): Whether to apply renaming recursively.

    Returns:
        None
    """

    def apply_case(name: str) -> str:
        if case == "lower":
            return name.lower()
        elif case == "upper":
            return name.upper()
        elif case == "capitalize":
            return name.capitalize()
        else:
            raise ValueError(f"Unsupported case transformation: {case}")

    for current_dir, dirs, files in os.walk(root_dir, topdown=False):
        # Skip descending into subdirectories if not recursive
        if not recursive and current_dir != root_dir:
            continue

        # Rename files
        for name in files:
            old_path = os.path.join(current_dir, name)
            new_name = apply_case(name)
            new_path = os.path.join(current_dir, new_name)
            if old_path != new_path:
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                else:
                    print(
                        f"Cannot rename {old_path} to {new_path}: target already exists."
                    )

        # Rename directories
        for name in dirs:
            old_path = os.path.join(current_dir, name)
            new_name = apply_case(name)
            new_path = os.path.join(current_dir, new_name)
            if old_path != new_path:
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                else:
                    print(
                        f"Cannot rename {old_path} to {new_path}: target already exists."
                    )


def parse_args() -> Namespace:
    """
    Parse and validate command-line arguments.

    Returns:
        Namespace: Parsed arguments with 'case' and 'recursive' options.
    """
    import argcomplete

    parser = ArgumentParser(
        description="Rename files and directories by changing case (lower, upper, capitalize)."
    )

    parser.add_argument(
        "--case",
        "-c",
        type=str,
        choices=["lower", "upper", "capitalize"],
        default="lower",
        help="Case transformation to apply: 'lower', 'upper', or 'capitalize'. Default is 'lower'.",
    )

    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Apply the transformation recursively in all subdirectories.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output (debug information, warnings)",
    )

    argcomplete.autocomplete(parser)
    return parser.parse_args()


def main() -> None:
    """
    Main entry point. Parses arguments and runs case renaming in current working directory.
    """
    args = parse_args()
    cwd: str = os.getcwd()
    rename_by_case(cwd, case=args.case, recursive=args.recursive)


if __name__ == "__main__":
    args = parse_verbose()
    run_in_venv(main, verbose=args.verbose)

#!/usr/bin/env python3

# === Standard library ===
import os
import sys
import subprocess
import venv
from pathlib import Path
from typing import Callable
from argparse import ArgumentParser, Namespace

# === Configuration ===
# Define the virtual environment directory in the user's home folder
VENV_DIR: Path = Path.home() / ".scripts_fabq_venv"

# Define the path to the requirements.txt file in the project root
REQUIREMENTS_FILE: Path = Path(__file__).resolve().parents[2] / "requirements.txt"


def parse_verbose() -> Namespace:
    """
    Parse the --verbose flag before virtual environment setup.

    This is useful when argument parsing requires packages that may
    only be available after the virtual environment is initialized.

    Returns:
        Namespace: Contains a single attribute 'verbose' (bool).
    """
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output.",
    )
    return parser.parse_known_args()[0]


def is_in_venv() -> bool:
    """
    Determine whether the script is currently running inside a virtual environment.

    Returns:
        bool: True if running inside a virtual environment, False otherwise.
    """
    return hasattr(sys, "real_prefix") or sys.prefix != getattr(
        sys, "base_prefix", sys.prefix
    )


def create_venv(verbose: bool = False) -> None:
    """
    Create a virtual environment in the predefined VENV_DIR location.

    Args:
        verbose (bool): If True, prints progress messages.
    """
    if verbose:
        print(f"Creating virtual environment in {VENV_DIR}...")
    venv.create(VENV_DIR, with_pip=True)


def install_requirements(verbose: bool = False) -> None:
    """
    Install Python dependencies from requirements.txt into the venv.

    Args:
        verbose (bool): If True, prints progress and pip output.
    """
    if not REQUIREMENTS_FILE.exists():
        print(f"Error: requirements.txt not found at {REQUIREMENTS_FILE}")
        sys.exit(1)

    if verbose:
        print(f"Installing/updating requirements from {REQUIREMENTS_FILE}...")

    pip_cmd = [str(VENV_DIR / "bin" / "pip")]

    try:
        subprocess.check_call(
            pip_cmd + ["install", "-r", str(REQUIREMENTS_FILE)],
            stdout=None if verbose else subprocess.DEVNULL,
            stderr=None if verbose else subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        sys.exit(1)

    try:
        subprocess.check_call(
            pip_cmd + ["check"],
            stdout=None if verbose else subprocess.DEVNULL,
            stderr=None if verbose else subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        print("Dependency conflict detected — your environment may be broken.")
        raise


def run_in_venv(main_func: Callable[[], None], verbose: bool = False) -> None:
    """
    Ensure the script is running inside the expected virtual environment.

    If not already in the venv:
        - Create it if needed
        - Install requirements
        - Relaunch the script inside the venv

    If already in the venv:
        - Ensure requirements are installed
        - Execute the given main function

    Args:
        main_func (Callable[[], None]): The function to execute after setup.
        verbose (bool): If True, enables progress messages and pip output.
    """
    if not is_in_venv():
        if not VENV_DIR.exists():
            create_venv(verbose)
            install_requirements(verbose)

        # Relaunch the script inside the virtual environment
        os.execv(
            str(VENV_DIR / "bin" / "python"),
            [str(VENV_DIR / "bin" / "python")] + sys.argv,
        )
    else:
        install_requirements(verbose)
        main_func()

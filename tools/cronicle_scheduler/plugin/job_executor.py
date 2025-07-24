#!/usr/bin/env python3
"""
Generic job executor for Cronicle plugin.

This script accepts:
- .env file path (optional)
- executable path (required)
- kwargs as JSON (optional)

Usage:
    python job_executor.py --executable /path/to/script.py
    python job_executor.py --executable /path/to/script.py --env-file /path/to/.env
    python job_executor.py --executable typer_app.py --kwargs '{"arg1": "value1"}'
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import argparse
from dotenv import load_dotenv


def load_environment(env_file: Optional[str] = None) -> None:
    """Load environment variables from .env file if provided."""
    if env_file and Path(env_file).exists():
        load_dotenv(env_file)
        print(f"Loaded environment from: {env_file}")


def execute_job(executable: str, kwargs: Optional[Dict[str, Any]] = None) -> int:
    """
    Execute the job with the given executable and kwargs.
    
    Returns:
        int: Exit code of the executed process
    """
    executable_path = Path(executable)
    
    if not executable_path.exists():
        print(f"Error: Executable not found: {executable}")
        return 1
    
    # Build command
    if executable_path.suffix == '.py':
        # Python script
        cmd = [sys.executable, str(executable_path)]
    else:
        # Other executables (typer, binaries, etc.)
        cmd = [str(executable_path)]
    
    # Add kwargs as command line arguments if provided
    if kwargs:
        for key, value in kwargs.items():
            if isinstance(value, bool):
                if value:
                    cmd.append(f"--{key}")
            else:
                cmd.extend([f"--{key}", str(value)])
    
    print(f"Executing: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=executable_path.parent,
            capture_output=False,  # Let output go to stdout/stderr
            text=True
        )
        return result.returncode
    except Exception as e:
        print(f"Error executing job: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description="Generic job executor for Cronicle")
    parser.add_argument(
        "--executable", 
        required=True,
        help="Path to the executable (Python script, typer app, binary, etc.)"
    )
    parser.add_argument(
        "--env-file",
        help="Path to .env file to load environment variables from"
    )
    parser.add_argument(
        "--kwargs",
        help="JSON string of kwargs to pass to the executable"
    )
    
    args = parser.parse_args()
    
    # Load environment if specified
    load_environment(args.env_file)
    
    # Parse kwargs if provided
    kwargs = None
    if args.kwargs:
        try:
            kwargs = json.loads(args.kwargs)
        except json.JSONDecodeError as e:
            print(f"Error parsing kwargs JSON: {e}")
            return 1
    
    # Execute the job
    exit_code = execute_job(args.executable, kwargs)
    
    print(f"Job completed with exit code: {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
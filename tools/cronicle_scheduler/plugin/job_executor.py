#!/usr/bin/env python3
"""
Generic job executor for Cronicle plugin.

This script reads JSON data from stdin containing job parameters:
- script_path: Path to Python script to execute (required)
- python_exec: Python executable to use (optional, defaults to $CALMMAGE_VENV_PATH/bin/python)
- env_file: Path to .env file (optional, defaults to script_path directory + .env)
- cli_args: Command line arguments to pass to script (optional)

Expected JSON format from Cronicle:
{
  "params": {
    "script_path": "/path/to/script.py",
    "python_exec": "",
    "env_file": "",
    "cli_args": "--verbose --timeout 300"
  },
  "timeout": 3600,
  ...
}
"""

import sys
import json
import subprocess
import os
import shlex
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


def is_empty(value: Optional[str]) -> bool:
    """Check if a parameter value is empty or None."""
    return value is None or value == "" or not value.strip()


def get_python_executable(python_exec: Optional[str]) -> str:
    """Get Python executable, using CALMMAGE_VENV_PATH if python_exec is empty."""
    if not is_empty(python_exec):
        return python_exec.strip()
    
    # Use CALMMAGE_VENV_PATH if available
    venv_path = os.getenv("CALMMAGE_VENV_PATH")
    if venv_path:
        python_path = Path(venv_path) / "bin" / "python"
        if python_path.exists():
            return str(python_path)
        else:
            raise Exception(f"CALMMAGE_VENV_PATH set but {python_path} does not exist")
    else:
        raise Exception("python_exec not provided and CALMMAGE_VENV_PATH environment variable not set")


def get_env_file_path(env_file: Optional[str], script_path: str) -> Optional[str]:
    """Get .env file path, defaulting to script directory if env_file is empty."""
    if not is_empty(env_file):
        return env_file.strip()
        
    # Look for .env in the same directory as the script
    script_dir = Path(script_path).parent
    default_env_file = script_dir / ".env"
    
    if default_env_file.exists():
        return str(default_env_file)
    else:
        # Don't require .env file - it's optional
        return None


def load_environment(env_file: Optional[str]) -> None:
    """Load environment variables from .env file if provided."""
    if env_file and Path(env_file).exists():
        load_dotenv(env_file)
        print(f"Loaded environment from: {env_file}")


def execute_python_job(script_path: str, python_exec: str, env_file: Optional[str], cli_args: Optional[str]) -> int:
    """
    Execute Python script with given parameters.
    
    Returns:
        int: Exit code of the executed process
    """
    script_path_obj = Path(script_path)
    
    if not script_path_obj.exists():
        print(f"Error: Script not found: {script_path}")
        return 1
    
    # Load environment variables if env file provided
    load_environment(env_file)
    
    # Build command
    cmd = [python_exec, str(script_path)]
    
    # Add CLI arguments if provided
    if not is_empty(cli_args):
        # Use shlex to properly parse CLI arguments
        try:
            parsed_args = shlex.split(cli_args.strip())
            cmd.extend(parsed_args)
        except ValueError as e:
            print(f"Error parsing CLI arguments '{cli_args}': {e}")
            return 1
    
    print(f"Executing: {' '.join(cmd)}")
    print(f"Working directory: {script_path_obj.parent}")
    if env_file:
        print(f"Environment file: {env_file}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=script_path_obj.parent,
            text=True
        )
        return result.returncode
    except Exception as e:
        print(f"Error executing job: {e}")
        return 1


def main():
    """Main function that reads JSON from stdin and executes the job."""
    try:
        # Read JSON data from stdin
        data = json.loads(sys.stdin.read())
        params = data.get("params", {})
        
        # Extract parameters
        script_path = params.get("script_path", "")
        python_exec_param = params.get("python_exec", "")
        env_file_param = params.get("env_file", "")
        cli_args = params.get("cli_args", "")
        
        # Validate required parameters
        if is_empty(script_path):
            result = {
                "complete": 0,
                "code": 1,
                "description": "script_path is required"
            }
            print(json.dumps(result))
            return 1
        
        # Get Python executable
        try:
            python_exec = get_python_executable(python_exec_param)
        except Exception as e:
            result = {
                "complete": 0,
                "code": 1,
                "description": f"Error getting Python executable: {e}"
            }
            print(json.dumps(result))
            return 1
        
        # Get .env file path
        env_file = get_env_file_path(env_file_param, script_path)
        
        # Execute the job
        exit_code = execute_python_job(script_path, python_exec, env_file, cli_args)
        
        # Return result in Cronicle format
        if exit_code == 0:
            result = {
                "complete": 1,
                "description": f"Script executed successfully: {script_path}"
            }
        else:
            result = {
                "complete": 0,
                "code": exit_code,
                "description": f"Script failed with exit code {exit_code}: {script_path}"
            }
        
        print(json.dumps(result))
        return exit_code
        
    except json.JSONDecodeError as e:
        result = {
            "complete": 0,
            "code": 1,
            "description": f"Invalid JSON input: {e}"
        }
        print(json.dumps(result))
        return 1
        
    except Exception as e:
        result = {
            "complete": 0,
            "code": 1,
            "description": f"Unexpected error: {e}"
        }
        print(json.dumps(result))
        return 1


if __name__ == "__main__":
    sys.exit(main())
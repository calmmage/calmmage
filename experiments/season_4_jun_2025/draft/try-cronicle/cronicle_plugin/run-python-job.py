#!/opt/homebrew/bin/python3

import os
import sys
import json

data = json.loads(sys.stdin.read())

params = data["params"]
#   "params": {
#     "script_path": "/Users/petrlavrov/work/projects/calmmage/seasonal/season_4_jun_2025/draft/try-cronicle/sample_jobs/1_hello_world.py",
#     "python_exec": "",
#     "env_file": "",
#     "cli_args": ""
#   },

script_path = params["script_path"]
python_exec = params["python_exec"]
env_file = params["env_file"]
cli_args = params["cli_args"]


def is_empty(value):
    return value is None or value == "" or not value.strip()


def run_script(script_path, python_exec, env_file, cli_args):
    # run the script
    # todo: look up how I did this in the past, and re-use.

    if is_empty(script_path):
        raise Exception("script_path is required")
    if is_empty(python_exec):
        # take the default python exec from the system
        # CALMMAGE_DIR="$(realpath "~/calmmage")"
        # CALMMAGE_VENV_PATH="$(realpath "$CALMMAGE_DIR/.venv")"
        # python_exec = "/Users/petrlavrov/.calmmage/dev_env/.venv/bin/python"
        venv_path = os.getenv("CALMMAGE_VENV_PATH")
        if venv_path:
            python_exec = venv_path + "/bin/python"
        else:
            raise Exception("CALMMAGE_VENV_PATH is not set")

    if is_empty(env_file):
        # try the location of the script
        env_file = os.path.dirname(script_path) + "/.env"
        if not os.path.exists(env_file):
            raise Exception("env_file is not set")

    env_vars = {}

    pass


result = {
    "complete": 1,
    # "code": 999,
    # "description": "Failed to execute."
}

print(json.dumps(result))


# data = json.loads(sys.stdin.read())
# {
#   "params": {
#     "script_path": "/Users/petrlavrov/work/projects/calmmage/seasonal/season_4_jun_2025/draft/try-cronicle/sample_jobs/1_hello_world.py",
#     "python_exec": "",
#     "env_file": "",
#     "cli_args": ""
#   },
#   "timeout": 3600,
#   "catch_up": 0,
#   "queue_max": 1000,
#   "timezone": "Europe/Moscow",
#   "plugin": "pmc6gxqss0t",
#   "category": "general",
#   "target": "allgrp",
#   "algo": "random",
#   "multiplex": 0,
#   "stagger": 0,
#   "retries": 0,
#   "retry_delay": 0,
#   "detached": 0,
#   "queue": 0,
#   "chain": "",
#   "chain_error": "",
#   "notify_success": "",
#   "notify_fail": "",
#   "web_hook": "",
#   "cpu_limit": 0,
#   "cpu_sustain": 0,
#   "memory_limit": 0,
#   "memory_sustain": 0,
#   "log_max_size": 0,
#   "notes": "",
#   "category_title": "General",
#   "group_title": "All Servers",
#   "plugin_title": "Run Python Job",
#   "now": 1750524435,
#   "source": "Manual (admin)",
#   "id": "jmc6h1v770x",
#   "time_start": 1750524435.763,
#   "hostname": "petrs-macbook-pro-2",
#   "event": "emc6h0g5k0u",
#   "event_title": "Test Python Job Runner plugin",
#   "nice_target": "All Servers",
#   "command": "/Users/petrlavrov/work/projects/calmmage/seasonal/season_4_jun_2025/draft/try-cronicle/cronicle_plugin/run-python-job.py",
#   "uid": "petrlavrov",
#   "log_file": "/opt/cronicle/logs/jobs/jmc6h1v770x.log",
#   "pid": 18436
# }

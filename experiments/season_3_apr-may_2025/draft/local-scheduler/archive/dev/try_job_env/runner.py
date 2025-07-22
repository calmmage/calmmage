from pathlib import Path
import os
from subprocess import run
from dotenv import dotenv_values

job_path = Path(
    "/Users/petrlavrov/work/projects/calmmage/experiments/season_3_apr_2025/draft/local-scheduler/dev/try_job_env/job.py"
)
env_file_path = Path(
    "/Users/petrlavrov/work/projects/calmmage/experiments/season_3_apr_2025/draft/local-scheduler/dev/try_job_env/.env"
)

calmmage_venv_path = os.getenv("CALMMAGE_VENV_PATH")
if not calmmage_venv_path:
    raise ValueError("CALMMAGE_VENV_PATH environment variable is not set")

python_executable_path = Path(calmmage_venv_path) / "bin" / "python"
from pydantic import BaseModel
from typing import Optional


class TaskDescription(BaseModel):
    # idea: task id?
    # idea: task name?
    # idea: task key? - for easy human-readable identification

    script_path: Path
    python_executable_path: Optional[Path] = (
        None  # path to python executable, default -
    )
    env_file_path: Optional[Path] = None  # default - .env in the location of the script

    # todo: use schedule variables
    # todo: add some kind of validation that cron or period is set
    cron: Optional[str] = None  # cron schedule
    period: Optional[int] = None  # period in seconds


def run_job(task_description: TaskDescription) -> None:
    return run(
        [
            str(task_description.python_executable_path),
            str(task_description.script_path),
        ],
        env=dotenv_values(task_description.env_file_path),
    )


if __name__ == "__main__":
    # Create a new environment dictionary for the subprocess
    # subprocess_env = dict(os.environ)

    sample_task = TaskDescription(
        script_path=job_path,
        python_executable_path=python_executable_path,
        env_file_path=env_file_path,
    )
    run_job(sample_task)

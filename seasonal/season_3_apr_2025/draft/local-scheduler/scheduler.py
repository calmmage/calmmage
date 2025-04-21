"""
FastAPI service
apscheduler scheduler

runs tasks based on configuration

"""
import os
from typing import Optional
from pathlib import Path
from pydantic import BaseModel
from dotenv import dotenv_values
class TaskDescription(BaseModel):
    # idea: task id?
    # idea: task name?
    # idea: task key? - for easy human-readable identification


    script_path: Path
    python_executable_path: Optional[Path] = None # path to python executable, default -
    env_file_path: Optional[Path] = None # default - .env in the location of the script

    # todo: use schedule variables
    # todo: add some kind of validation that cron or period is set
    cron: Optional[str] = None # cron schedule
    period: Optional[int] = None # period in seconds


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: TaskDescription):
        """
        Add a task to the task manager
        """
        self.tasks.append(task)

    def get_all_tasks(self):
        """
        Get all tasks
        """
        return self.tasks

    def task_overdue(self, task: TaskDescription):
        # todo: add task history
        return True

    def run_task(self, task: TaskDescription):
        from subprocess import run, PIPE
        result = run(
            [str(task.python_executable_path), str(task.script_path)],
            check=True,
            stdout=PIPE,
            stderr=PIPE,
            env=dotenv_values(task.env_file_path),
            text=True
        )
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }

    async def arun_task(self, task: TaskDescription):
        from asyncio import create_subprocess_exec
        from asyncio.subprocess import PIPE
        process = await create_subprocess_exec(
            str(task.python_executable_path),
            str(task.script_path),
            stdout=PIPE,
            stderr=PIPE,
            env=dotenv_values(task.env_file_path)
        )
        stdout, stderr = await process.communicate()
        return {
            'stdout': stdout.decode(),
            'stderr': stderr.decode(),
            'returncode': process.returncode
        }

task_manager = TaskManager()


def enrich_task(task: TaskDescription):
    """
    Enrich the task with the default values
    """
    if task.python_executable_path is None:
        default_executable_path = Path(os.getenv("STABLE_VENV_PATH")) / "bin" / "python"
        task.python_executable_path = default_executable_path
    if task.env_file_path is None:
        task.env_file_path = task.script_path.parent / ".env"
    return task


async def on_startup():
    """
    Idea: check the last time each task was run.
    If more than defined by schedule - run the task
    """
    tasks = task_manager.get_all_tasks()

    for task in tasks:
        # todo: run them in parallel.
        if task_manager.task_overdue(task):
            # run the task
            pass
    pass

if __name__ == '__main__':
    # just run a test task for now

    # define test task
    test_task = TaskDescription(
        script_path=Path("/Users/petrlavrov/work/projects/calmmage/seasonal/season_3_apr_2025/draft/local-scheduler/target_job.py"),
        # cron="* * * * *",
        # period=60
    )

    result = task_manager.run_task(test_task)

    print(result)

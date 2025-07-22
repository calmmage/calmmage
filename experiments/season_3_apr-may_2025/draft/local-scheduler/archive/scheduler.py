"""
FastAPI service
apscheduler scheduler

runs tasks based on configuration

"""

from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import Optional
from pathlib import Path
from pydantic import BaseModel
from datetime import datetime
from dotenv import dotenv_values


class TaskDescription(BaseModel):
    # idea: task id?
    # idea: task name?
    task_name: Optional[str] = None
    # idea: task key? - for easy human-readable identification
    task_key: Optional[str] = None

    enabled: bool = True

    script_path: Path
    python_executable_path: Optional[Path] = (
        None  # path to python executable, default -
    )
    env_file_path: Optional[Path] = None  # default - .env in the location of the script

    # todo: use schedule variables
    # todo: add some kind of validation that cron or period is set
    cron: Optional[str] = None  # cron schedule
    period: Optional[int] = None  # period in seconds


class TaskRunRecord(BaseModel):
    task_name: str
    task_key: str

    result: dict

    created_at: datetime


class TaskManager:
    db_name = "scheduler"
    tasks_collection_name = "tasks"
    task_runs_collection_name = "task_runs"

    def __init__(self):
        self.db = AsyncIOMotorClient(os.getenv("MONGO_URI"))[self.db_name]

        self.tasks_collection = self.db[self.tasks_collection_name]
        self.task_runs_collection = self.db[self.task_runs_collection_name]

        # on init - load all tasks from the database
        self._tasks = None

    async def _load_tasks(self) -> list[TaskDescription]:
        """
        Load all tasks from the database
        """
        tasks = await self.tasks_collection.find({}).to_list(None)
        return [TaskDescription(**task) for task in tasks]

    async def add_task(self, task: TaskDescription):
        """
        Add a task to the task manager
        """
        if self._tasks is None:
            self._tasks = await self._load_tasks()

        # let's enrich the task
        task = enrich_task(task)

        self._tasks.append(task)

        await self.tasks_collection.insert_one(task.model_dump())

    async def get_all_tasks(self) -> list[TaskDescription]:
        """
        Get all tasks
        """
        if self._tasks is None:
            self._tasks = await self._load_tasks()
        return self._tasks

    def task_overdue(self, task: TaskDescription):
        # todo: add task history
        return True

    def run_task(self, task: TaskDescription):
        # step 1: enrich the task
        task = enrich_task(task)
        # step 2: run the task
        result = self._run_task(task)
        # todo: log the task run to the database
        # step 3: return the result
        return result

    async def arun_task(self, task: TaskDescription):
        # step 1: enrich the task
        task = enrich_task(task)
        # step 2: run the task
        result = await self._arun_task(task)
        # todo: log the task run to the database
        # step 3: return the result
        return result

    def _run_task(self, task: TaskDescription):
        from subprocess import run, PIPE

        result = run(
            [str(task.python_executable_path), str(task.script_path)],
            check=True,
            stdout=PIPE,
            stderr=PIPE,
            env=dotenv_values(task.env_file_path),
            text=True,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }

    async def _arun_task(self, task: TaskDescription):
        from asyncio import create_subprocess_exec
        from asyncio.subprocess import PIPE

        env = dotenv_values(task.env_file_path)

        process = await create_subprocess_exec(
            str(task.python_executable_path),
            str(task.script_path),
            stdout=PIPE,
            stderr=PIPE,
            env=env.__dict__,
        )

        stdout, stderr = await process.communicate()
        return {
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "returncode": process.returncode,
        }

    # region - Log task runs
    async def _log_task_run(self, task: TaskDescription, result: dict):
        task_run_record = TaskRunRecord(
            task_name=task.task_name,
            task_key=task.task_key,
            result=result,
            created_at=datetime.now(),
        )

        await self.task_runs_collection.insert_one(task_run_record.model_dump())

    # endregion - Log task runs


task_manager = TaskManager()


def enrich_task(task: TaskDescription) -> TaskDescription:
    """
    Enrich the task with the default values
    """
    if task.python_executable_path is None:
        stable_venv_path = os.getenv("STABLE_VENV_PATH")
        if stable_venv_path is None:
            raise ValueError("STABLE_VENV_PATH is not set")
        default_executable_path = Path(stable_venv_path) / "bin" / "python"
        task.python_executable_path = default_executable_path
    if task.env_file_path is None:
        task.env_file_path = task.script_path.parent / ".env"

    if task.task_key is None:
        task.task_key = task.script_path.stem
    if task.task_name is None:
        # "file_name" -> "File Name"
        task.task_name = task.task_key.replace("_", " ").replace("-", " ").title()

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


def main():
    # just run a test task for now
    test_task = TaskDescription(
        script_path=Path(
            "/Users/petrlavrov/work/projects/calmmage/experiments/season_3_apr_2025/draft/local-scheduler/target_job.py"
        ),
        # cron="* * * * *",
        # period=60
    )
    result = task_manager.run_task(test_task)
    print(result)


async def amain():
    # Create 10 tasks with different sleep times
    tasks = []
    for i in range(10):
        task = TaskDescription(
            script_path=Path("target_job.py").absolute(),
        )
        tasks.append(task)

    # Run all tasks concurrently
    start_time = asyncio.get_event_loop().time()
    results = await asyncio.gather(*[task_manager.arun_task(task) for task in tasks])
    end_time = asyncio.get_event_loop().time()

    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    for i, result in enumerate(results):
        print(f"Task {i} completed with return code: {result['returncode']}")


if __name__ == "__main__":
    import asyncio
    # Run either sync or async version
    # main()

    asyncio.run(amain())

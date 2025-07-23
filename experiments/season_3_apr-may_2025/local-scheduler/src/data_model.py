from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
from pydantic import BaseModel
from src.utils import discover_python_executable


class Job(BaseModel):
    # --------------------------------------------------------------------------
    # region: metadata

    name: str  # Fancy, human-readable name
    description: Optional[str] = None  # Description of the job
    # tags: Optional[List[str]] = None # Tags of the job
    # key: Optional[str] = None # A shortcut identifier for easier reference

    # endregion: metadata
    # --------------------------------------------------------------------------
    # region: execution parameters

    # todo: put a specific default value here. Just a simple python runner for everything
    executable: str = (
        discover_python_executable()
    )  # Path to the executable - default - poetry in dev_env
    # todo: actually, support both .py and .sh files

    script_path: Path  # Path to the target file to run. This is the actual script that we want to run. Mandatory field.

    env_file: Optional[Path] = None  # Path to the environment file - default - ~/.env

    # args
    args: Optional[List[str]] = None
    # kwargs
    kwargs: Optional[Dict[str, str]] = None

    # endregion: execution parameters
    # --------------------------------------------------------------------------
    # region: schedule - when to run
    # todo: add other necessary ways to schedule - namely, cron or something.
    # cron: Optional[str] = None # Cron schedule
    # For now, simple period
    period: Optional[int] = None  # Period in seconds
    # endregion: schedule - when to run


class JobExecutionLogRecord(BaseModel):
    # --------------------------------------------------------------------------
    # region: identifyer

    # name? key? id? Or just full job details?
    name: str
    job: Job
    # combo: key details + full detauls
    # endregion: identifyer

    # --------------------------------------------------------------------------
    # region: timestamp
    timestamp: datetime
    # endregion: timestamp

    # --------------------------------------------------------------------------
    # region: results
    return_code: int  # exactly what subprocess.CompletedProcess.returncode gives you
    stdout: str
    stderr: str
    # endregion: results

    @property
    def success(self) -> bool:
        return self.return_code == 0

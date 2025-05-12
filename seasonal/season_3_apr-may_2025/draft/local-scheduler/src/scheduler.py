from datetime import datetime
from textwrap import dedent
from pathlib import Path
import subprocess
from typing import List, Optional
from src.data_model import Job, JobExecutionLogRecord
from src.utils import discover_telegram_bot_token
import yaml
from loguru import logger
from dotenv import dotenv_values
from pymongo import MongoClient

# todo: use abs path?
DEFAULT_YAML_PATH = Path("data/my_jobs.yaml")
DEFAULT_MONGO_CONN_STR = "mongodb://localhost:27017"
DEFAULT_TELEGRAM_CHAT_ID = "291560340"


class Scheduler:
    def __init__(
        self,
        yaml_file: Path = DEFAULT_YAML_PATH,
        mongo_conn_str: str = DEFAULT_MONGO_CONN_STR,
        telegram_bot_token: Optional[str] = None,
        telegram_chat_id: str = DEFAULT_TELEGRAM_CHAT_ID,
    ):
        self.yaml_file = yaml_file
        self.mongo_conn_str = mongo_conn_str
        self._telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id

        self.check_local_mongo()

    @property
    def telegram_bot_token(self) -> str:
        if self._telegram_bot_token is None:
            self._telegram_bot_token = discover_telegram_bot_token()
        return self._telegram_bot_token

    @property
    def jobs_list(self) -> List[Job]:
        return self._load_jobs_list(self.yaml_file)

    @staticmethod
    def _load_jobs_list(yaml_file: Path) -> List[Job]:
        with open(yaml_file) as f:
            logger.info(f"Loading jobs from {yaml_file}")
            jobs_list = yaml.safe_load(f)["jobs"]
        logger.info(f"Loaded {len(jobs_list)} jobs")
        logger.debug(f"Jobs: {jobs_list}")
        return [Job(**job) for job in jobs_list]

    @staticmethod
    def run_job(job: Job) -> JobExecutionLogRecord:
        env_dict = {
            k: v for k, v in dotenv_values(job.env_file).items() if v is not None
        }
        # run the job using subprocess
        res = subprocess.run(
            [job.executable, job.script_path], capture_output=True, env=env_dict
        )

        # log the result
        log_record = JobExecutionLogRecord(
            name=job.name,
            job=job,
            timestamp=datetime.now(),
            return_code=res.returncode,
            stdout=res.stdout.decode("utf-8"),
            stderr=res.stderr.decode("utf-8"),
        )

        return log_record

    def run_all_jobs_once(self):
        results = []
        for job in self.jobs_list:
            res = self.run_job(job)
            results.append(res)
        return results

    def _is_local_mongo_running(self) -> bool:
        # check if local mongo is running
        # if not, ping me to telegram
        conn = MongoClient(self.mongo_conn_str, serverSelectionTimeoutMS=1000)
        try:
            conn.admin.command("ping")
            return True
        except Exception:
            return False

    def check_local_mongo(self):
        if not self._is_local_mongo_running():
            message = dedent("""
                Running scheduler on Calmmage Macbook.
                Local mongo is not running.
                Please start it and try again.
            """)
            # send telegram message
            self._send_telegram_message(message)

            logger.error("Local mongo is not running")
            raise RuntimeError("Local mongo is not running")

    def _send_telegram_message(self, message: str):
        from aiogram import Bot
        from aiogram.enums import ParseMode
        import asyncio

        bot = Bot(token=self.telegram_bot_token)
        asyncio.run(
            bot.send_message(
                chat_id=self.telegram_chat_id, text=message, parse_mode=ParseMode.HTML
            )
        )


if __name__ == "__main__":
    scheduler = Scheduler()

    results = scheduler.run_all_jobs_once()
    for res in results:
        print(res.model_dump_json(indent=2))
        print()

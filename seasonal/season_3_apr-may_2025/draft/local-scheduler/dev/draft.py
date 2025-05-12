# from datetime import datetime
# from pathlib import Path
# import subprocess
# from typing import List
# from src.data_model import Job, JobExecutionLogRecord
# import yaml
# from loguru import logger
# from dotenv import dotenv_values


# def load_jobs_list(yaml_file: Path) -> List[Job]:
#     with open(yaml_file, 'r') as f:
#         logger.info(f"Loading jobs from {yaml_file}")
#         jobs_list = yaml.safe_load(f)['jobs']
#     logger.info(f"Loaded {len(jobs_list)} jobs")
#     logger.debug(f"Jobs: {jobs_list}")
#     return [Job(**job) for job in jobs_list]


# def run_job(job: Job):
#     env_dict = {k: v for k, v in dotenv_values(job.env_file).items() if v is not None}
#     # run the job using subprocess
#     res = subprocess.run([job.executable, job.script_path], capture_output=True,
#                          env=env_dict)

#     # log the result
#     log_record = JobExecutionLogRecord(
#         name=job.name,
#         job=job,
#         timestamp=datetime.now(),
#         return_code=res.returncode,
#         stdout=res.stdout.decode('utf-8'),
#         stderr=res.stderr.decode('utf-8'),
#     )

#     return log_record


# if __name__ == "__main__":
#     jobs_list = load_jobs_list(Path('data/my_jobs.yaml'))
#     print(jobs_list)

#     for job in jobs_list:
#         res = run_job(job)
#         print(res.model_dump_json(indent=2))



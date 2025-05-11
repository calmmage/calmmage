import os
from datetime import datetime

target_path = "/Users/petrlavrov/work/projects/calmmage/seasonal/season_3_apr_2025/draft/local-scheduler/dev/try_job_env/sample.txt"


def main():
    timestamp = datetime.now().strftime("%d %b, %H:%M %Ss")
    sample_output = os.getenv("SAMPLE_ENV_VAR", "Hello World")
    print(sample_output)
    with open(target_path, "a") as f:
        f.write(f"{timestamp} - {sample_output}\n")


if __name__ == "__main__":
    main()

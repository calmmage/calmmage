from src.scheduler import Scheduler


if __name__ == "__main__":
    scheduler = Scheduler()

    results = scheduler.run_all_jobs_once()
    for res in results:
        print(res.model_dump_json(indent=2))
        print()

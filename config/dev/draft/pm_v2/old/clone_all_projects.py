from pathlib import Path

import dev_env.core.git_utils
import git
from dotenv import load_dotenv
from loguru import logger
from tqdm.auto import tqdm

load_dotenv()

allowed_teams = [
    "calmmage",
    "Augmented-development",
    "engineering-friends",
    "lavrpetrov",
]


def clone_repos(repos, target_dir):
    stats = {
        "total": len(repos),
        "allowed": 0,
        "cloned": 0,
        "skipped": 0,
    }

    for repo in tqdm(repos):
        full_repo_name = repo.full_name
        if not any([full_repo_name.startswith(team) for team in allowed_teams]):
            logger.info(f"Skipping {full_repo_name}")
            continue
        stats["allowed"] += 1

        target_path = Path(target_dir) / repo.name
        if not target_path.exists():
            git.Repo.clone_from(repo.clone_url, target_path)
            stats["cloned"] += 1
        else:
            stats["skipped"] += 1

    return stats


if __name__ == "__main__":
    # dev_env = CalmmageDevEnv()
    # todo: rework this better
    target_dir = dev_env.all_projects_dir

    import os

    from github import Github

    token = os.getenv("GITHUB_API_TOKEN")
    if token is None:
        raise ValueError("Missing GitHub API token")
    github_client = Github(token)

    # get all my projects
    my_repos = list(github_client.get_user().get_repos())

    stats = clone_repos(my_repos, target_dir)
    print(stats)

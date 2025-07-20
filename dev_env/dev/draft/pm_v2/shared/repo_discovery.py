import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import git
from loguru import logger
from pydantic_settings import BaseSettings
from tqdm.auto import tqdm

from dev_env.tools.project_arranger.src.utils import is_git_repo


class Settings(BaseSettings):
    projects_root_dirs: List[str] = [".", "~/projects", "~/work"]
    repo_cache_ttl_days: int = 7  # cache validity period in days
    repo_cache_path: Path = Path("~/.calmmage/cache/repo_discovery.json")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class RepoCache:
    def __init__(self, cache_path: Path, ttl_days: int):
        self.cache_path = cache_path.expanduser().resolve()
        self.ttl = timedelta(days=ttl_days)
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Optional[Dict]:
        """Load cache if it exists and is not expired"""
        if not self.cache_path.exists():
            return None

        try:
            data = json.loads(self.cache_path.read_text())
            cached_time = datetime.fromisoformat(data["timestamp"])

            if datetime.now() - cached_time > self.ttl:
                logger.debug("Cache expired")
                return None

            return data
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")
            return None

    def save(self, repos: List[Path], authors_map: Dict[str, List[str]]):
        """Save repository data to cache"""
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "repos": [str(repo) for repo in repos],
            "authors": authors_map,
        }

        try:
            self.cache_path.write_text(json.dumps(cache_data, indent=2))
            logger.debug(f"Cache saved to {self.cache_path}")
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")


def get_repo_authors(repo_path: Path) -> List[str]:
    """Get list of authors who contributed to the repository"""
    try:
        repo = git.Repo(repo_path)
        authors = set()
        for commit in repo.iter_commits():
            authors.add(commit.author.name)
        return list(authors)
    except Exception as e:
        logger.warning(f"Failed to get authors for {repo_path}: {e}")
        return ["Unknown"]


def discover_local_projects(
    use_cache: bool = True,
) -> tuple[List[Path], Dict[str, List[str]]]:
    """
    Discover all local git repositories in configured directories.

    Args:
        use_cache: Whether to use cached results if available

    Returns:
        Tuple of (list of repository paths, dict mapping repo paths to authors)
    """
    settings = Settings()
    cache = RepoCache(settings.repo_cache_path, settings.repo_cache_ttl_days)

    # Try to load from cache first
    if use_cache:
        cached_data = cache.load()
        if cached_data:
            logger.info("Using cached repository data")
            return ([Path(p) for p in cached_data["repos"]], cached_data["authors"])

    discovered_repos = []
    authors_map = {}

    for root_dir in settings.projects_root_dirs:
        root_path = Path(root_dir).expanduser().resolve()
        logger.info(f"Scanning {root_path} for git repositories...")

        if not root_path.exists():
            logger.warning(f"Directory {root_path} does not exist, skipping...")
            continue

        # Walk through all subdirectories
        for path in tqdm(list(root_path.rglob("*"))):
            # Skip if not a directory or if it's inside .git
            if not path.is_dir() or ".git" in path.parts:
                continue

            if is_git_repo(path):
                discovered_repos.append(path)
                authors_map[str(path)] = get_repo_authors(path)
                logger.debug(f"Found git repository: {path}")

    logger.info(f"Discovered {len(discovered_repos)} git repositories")

    # Save to cache
    cache.save(discovered_repos, authors_map)

    return discovered_repos, authors_map


def get_repo_name(repo_path: Path) -> str:
    """Extract repository name from path."""
    return repo_path.name


def is_author_match(authors: List[str], patterns: List[str]) -> bool:
    """Check if any author matches any of the patterns"""
    return any(pattern in author for pattern in patterns for author in authors)


def filter_repos_by_author(
    repos: List[Path], authors_map: Dict[str, List[str]], author_patterns: List[str]
) -> List[Path]:
    """Filter repositories by author patterns"""
    return [
        repo
        for repo in repos
        if is_author_match(authors_map[str(repo)], author_patterns)
    ]


if __name__ == "__main__":
    # Test the discovery function
    repos, authors = discover_local_projects()
    print("\nRepositories found:")
    for repo in repos:
        print(f"Repository: {repo}")
        print(f"Authors: {authors[str(repo)]}\n")

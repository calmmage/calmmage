from pathlib import Path
from collections import Counter
from src.lib.lib import discover_local_projects
from loguru import logger

# Disable debug logging to keep output clean
logger.remove()
logger.add(lambda msg: print(msg), level="INFO")


def get_repo_depth(repo_path: Path) -> int:
    """Get the depth of repository in directory tree"""
    return len(repo_path.parts)


def print_repo_stats():
    repos, authors = discover_local_projects()

    # Basic stats
    print("\n=== Repository Statistics ===")
    print(f"Total repositories found: {len(repos)}")

    # Author stats
    author_patterns = ["Petr Lavrov", "petr.b.lavrov", "Reliable Magician", "calmquant"]
    my_repos = [
        repo
        for repo in repos
        if any(
            pattern in author
            for repo_authors in [authors[str(repo)]]
            for author in repo_authors
            for pattern in author_patterns
        )
    ]
    print(f"My repositories: {len(my_repos)}")

    # Depth statistics
    depths = Counter(get_repo_depth(repo) for repo in repos)
    print("\n=== Repository Depths ===")
    for depth in sorted(depths.keys()):
        print(f"Depth {depth}: {depths[depth]} repos")

    # Directory statistics
    dir_counts = Counter(str(repo.parent) for repo in repos)
    print("\n=== Top Directories by Repository Count ===")
    for dir_path, count in dir_counts.most_common(5):
        print(f"{dir_path}: {count} repos")

    # Example paths
    print("\n=== Example Repository Paths ===")
    for repo in list(repos)[:5]:
        print(f"- {repo}")


if __name__ == "__main__":
    print_repo_stats()

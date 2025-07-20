from datetime import datetime, timedelta
from pathlib import Path

from git import GitCommandError, Repo
from pydantic_settings import BaseSettings


def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


# todo: update as below
def get_last_commit_date(path: Path) -> datetime:
    repo = Repo(path)
    return datetime.fromtimestamp(repo.head.commit.committed_date)


def get_first_commit_date(path: Path) -> datetime:
    """
    Retrieves the date of the first commit in the Git repository at the given path.

    Args:
        path (Path): The filesystem path to the Git repository.

    Returns:
        datetime: The datetime of the first commit.

    Raises:
        ValueError: If the repository has no commits.
        GitCommandError: If the provided path is not a valid Git repository.
    """
    try:
        repo = Repo(path)
    except GitCommandError as e:
        raise ValueError(f"The path '{path}' is not a valid Git repository.") from e

    if repo.bare:
        raise ValueError(f"The repository at '{path}' is bare and has no commits.")

    try:
        # Attempt to iterate commits in reverse (from oldest to newest)
        first_commit = next(repo.iter_commits(reverse=True))
    except StopIteration:
        raise ValueError("No commits found in the repository.")

    return first_commit.committed_datetime


def get_commit_count(path: Path, days: int = 30) -> int:
    repo = Repo(path)
    since_date = datetime.now() - timedelta(days=days)
    return len(list(repo.iter_commits(since=since_date)))


class DateFormatSettings(BaseSettings):
    use_relative_dates: bool = True
    short_format: bool = (
        True  # Use shortened date format (e.g., "Nov 15" vs "2023-11-15")
    )

    # Only used if use_relative_dates disabled  Use relative dates for dates within a week
    use_relative_for_recent: bool = True
    recent_threshold_days: int = 7  # What counts as "recent"


def format_relative(delta: timedelta) -> str:
    """Format a timedelta into human readable format"""
    days = delta.days
    if days == 0:
        hours = delta.seconds // 3600
        if hours == 0:
            minutes = delta.seconds // 60
            return f"{minutes} minutes ago"
        return f"{hours} hours ago"
    # elif days < 7:
    #     return f"{days} days ago"
    # elif days < 31:
    #     weeks = days // 7
    #     return f"{weeks} weeks ago"
    elif days < 65:
        return f"{days} days ago"
    elif days < 365:
        months = days // 30
        # remaining_days = days % 30
        # if remaining_days > 0:
        #     return f"{months} months {remaining_days} days ago"
        return f"{months} months ago"
    else:
        years = days // 365
        remaining_months = (days % 365) // 30
        if remaining_months > 0:
            return f"{years} years {remaining_months} months ago"
        return f"{years} years ago"


def format_date(
    date: datetime, format: DateFormatSettings, now: datetime = None
) -> str:
    """Format date according to format:
    - Can use relative dates ("2 months ago")
    - Can use short format for recent dates ("Nov 15")
    - Can use relative dates only for recent changes
    """
    if now is None:
        now = datetime.now()

    delta = now - date
    days_old = delta.days

    # Use relative dates for recent changes if enabled
    if format.use_relative_for_recent and days_old <= format.recent_threshold_days:
        return format_relative(delta)

    # Use relative dates if enabled
    if format.use_relative_dates:
        return format_relative(delta)

    # Use short format for dates
    if format.short_format:
        if days_old < 365:
            return date.strftime("%d %b")  # "15 Nov"
        else:
            return date.strftime("%b %Y")  # "Oct 2023"

    # Default to full date format
    return date.strftime("%Y-%m-%d")

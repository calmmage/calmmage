import os
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel

from github.Repository import Repository
from loguru import logger
from tqdm.auto import tqdm

from tools.project_arranger.src.config import ProjectArrangerSettings
from tools.project_arranger.src.utils import (
    DateFormatSettings,
    format_date,
    get_commit_count,
    get_first_commit_date,
    get_last_commit_date,
    is_git_repo,
)


def MISSING():
    pass


# todo: use everywhere?
class Group(str, Enum):
    experiments = "experiments"
    actual = "projects"  # rename to actual? - but folder stays as projects/
    unsorted = "unsorted"
    archive = "archive"
    ignore = "ignore"


class Project(BaseModel):
    name: str
    path: Optional[Path] = None
    github_repo: Optional[Repository] = None

    class Config:
        arbitrary_types_allowed = True

    def __hash__(self):
        """Make Project hashable for use in sets and as dict keys"""
        # Use name and path (if available) as the hash key
        return hash((self.name, str(self.path) if self.path else None))

    def __eq__(self, other):
        """Define equality for Project objects"""
        if not isinstance(other, Project):
            return False
        # Projects are equal if they have the same name and path
        return self.name == other.name and self.path == other.path

    @staticmethod
    def _extract_repo_info(url: str) -> tuple[str, str]:
        """Extract GitHub repository name and organization from the project path"""
        if "github.com" not in url:
            raise ValueError(f"URL {url} is not a GitHub URL")
        # Extract org and repo from URL
        # Handles both HTTPS and SSH URLs:
        # https://github.com/org/repo.git
        # git@github.com:org/repo.git
        parts = url.split("github.com")[-1].strip("/:").replace(".git", "").split("/")
        if len(parts) == 2:
            org_name, repo_name = parts
            return repo_name, org_name
        raise ValueError(f"Failed to extract repo info from {url}")

    @cached_property
    def _repo_info(self) -> tuple[Optional[str], Optional[str]]:
        """Get GitHub repository name and organization for a local repository

        Returns:
            Tuple of (repo_name, org_name) or None if not found/available
        """
        if self.github_repo:
            return self._extract_repo_info(self.github_repo.html_url)

        try:
            from git import Repo

            repo = Repo(self.path)

            # Get the GitHub remote URL
            for remote in repo.remotes:
                url = remote.url
                if "github.com" not in url:
                    continue
                return self._extract_repo_info(url)

            raise ValueError(f"Failed to find GitHub remote URL in {self.path}")

        except Exception as e:
            logger.debug(f"Failed to get repo info for {self.path}: {e}")
            return None, None

    @property
    def github_name(self) -> Optional[str]:
        if self.github_repo:
            return self.github_repo.name
        repo_info = self._repo_info
        return repo_info[0] if repo_info else None

    @property
    def github_org(self) -> Optional[str]:
        if self.github_repo:
            return self.github_repo.owner.login
        repo_info = self._repo_info
        return repo_info[1] if repo_info else None

    # todo: use external ignore rules
    #  option 1: gitignore
    __ignored_paths = [
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "build",
        "dist",
        ".pytest_cache",
    ]

    __source_extensions = [
        ".py",
        ".md",
        # ".js",
        # ".ts",
        # ".jsx",
        # ".tsx",
        # ".java",
        ".cpp",
        # ".c",
        # ".h",
        # ".hpp",
        # ".rs",
        # ".go",
        # ".rb",
        # ".php",
        # ".html",
        # ".css",
        # ".scss",
        # ".sql",
        ".sh",
    ]

    @cached_property
    def size(self) -> int:
        """Synchronous size calculation - use async_size for better performance"""
        import asyncio

        try:
            # Try to run in existing event loop
            loop = asyncio.get_running_loop()
            # If we're already in an async context, we need to use a different approach
            # This is a fallback for sync usage
            return asyncio.run_coroutine_threadsafe(self.async_size(), loop).result(
                timeout=10
            )
        except RuntimeError:
            # No event loop running, safe to use asyncio.run
            return asyncio.run(self.async_size())

    async def async_size(self) -> int:
        """Async size calculation for better performance with many projects"""
        if self.path is None:
            logger.warning(f"No path set for project {self.name}, can't calculate size")
            return 0

        # Fast approach 1: Use git ls-files if it's a git repo
        if self.is_git_repo():
            try:
                return await self._async_git_tracked_size()
            except Exception as e:
                logger.debug(f"Git size calculation failed for {self.path}: {e}")

        # Fast approach 2: Smart glob patterns for non-git projects
        return await self._async_fallback_size_calculation()

    async def _async_git_tracked_size(self) -> int:
        """Async version of git size calculation"""
        import asyncio
        from git import Repo

        # Run git operations in thread pool to avoid blocking
        def _git_size():
            repo = Repo(self.path)
            total_size = 0

            # Get all tracked files
            tracked_files = repo.git.ls_files().splitlines()

            for file_path in tracked_files:
                file_full_path = self.path / file_path

                # Skip if file doesn't exist (deleted but not committed)
                if not file_full_path.exists():
                    continue

                # Only count source code files
                if file_full_path.suffix in self.__source_extensions:
                    total_size += file_full_path.stat().st_size

            return total_size

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _git_size)

    async def _async_fallback_size_calculation(self) -> int:
        """Async fallback size calculation"""
        import asyncio

        if self.path is None:
            return 0

        def _fallback_size():
            total_size = 0
            try:
                # Only check a few key patterns for speed
                quick_patterns = ["*.py", "*.md", "*.sh", "src/**/*.py", "lib/**/*.py"]
                for pattern in quick_patterns:
                    for file in self.path.glob(pattern):
                        if file.is_file():
                            total_size += file.stat().st_size
            except Exception as e:
                logger.debug(f"Fallback size calculation failed for {self.path}: {e}")
            return total_size

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _fallback_size)

    FORMAT_MODE: int = 2

    # todo: show main language?
    @property
    def size_formatted(self) -> str:
        """Format size with appropriate units and alignment"""
        if self.FORMAT_MODE == 1:
            if self.size >= 1_000_000:  # 1M+
                return f"{self.size/1_000_000:>8.2f}M"
            elif self.size >= 1_000:  # 1K+
                return f"{self.size/1_000:>8.2f}K"
            else:
                return f"{self.size:>8}B"
        elif self.FORMAT_MODE == 2:
            # Round to 3 significant digits and add commas
            if self.size >= 1000:
                magnitude = len(str(self.size)) - 3
                rounded = (self.size // (10**magnitude)) * (10**magnitude)
                return f"{rounded:>10,}"
            return f"{self.size:>10}"
        else:
            # Default fallback
            return f"{self.size:>10}"

    @cached_property
    def date(self) -> datetime:
        """Last meaningful change date - from git or filesystem"""
        if self.github_repo:
            return self.github_repo.pushed_at.replace(tzinfo=None)

        if self.path is None:
            # Fallback to current time if no path available
            return datetime.now()

        # idea 1: if git repo - look at last commit date
        if is_git_repo(self.path):
            try:
                return get_last_commit_date(self.path).replace(
                    tzinfo=None
                )  # Make naive
            except ValueError:
                pass
        # idea 2: if no git repo - look at file dates
        paths = list(self.path.iterdir())
        paths.append(self.path)
        max_mtime = max(
            file.stat().st_mtime for file in paths if not file.name.startswith(".")
        )
        return datetime.fromtimestamp(max_mtime)

    @cached_property
    def created_date(self) -> datetime:
        """Project creation date - from git or filesystem"""
        if self.github_repo:
            return self.github_repo.created_at.replace(tzinfo=None)

        if self.path is None:
            # Fallback to current time if no path available
            return datetime.now()

        # idea 1: if git repo - look at first commit date
        if is_git_repo(self.path):
            try:
                return get_first_commit_date(self.path).replace(
                    tzinfo=None
                )  # Make naive
            except ValueError:
                pass
        # idea 2: if no git repo - look at file dates
        paths = list(self.path.iterdir())
        paths.append(self.path)
        min_mtime = min(
            file.stat().st_mtime for file in paths if not file.name.startswith(".")
        )
        return datetime.fromtimestamp(min_mtime)

    @cached_property
    def current_group(self) -> str:
        if self.path is None:
            return Group.ignore
        group = self.path.parent.name
        try:
            return Group(group)
        except:
            logger.warning(f"Unknown group {group}")
            return Group.unsorted

    def date_formatted(self, format: DateFormatSettings = DateFormatSettings()) -> str:
        """Format date information based on project timeline:
        - if edited > 1 month ago -> print that
        - if edited recently but created long ago -> print both
        - if edited recently and created recently -> print only when edited
        """
        today = datetime.now()  # Naive datetime
        one_month_ago = today - timedelta(days=30)
        three_months_ago = today - timedelta(days=90)

        edited_date = self.date
        created_date = self.created_date

        if edited_date < one_month_ago:
            return f"Edited {format_date(edited_date, format)}"
        elif created_date < three_months_ago:
            return (
                f"Edited {format_date(edited_date, format)}, "
                f"Created {format_date(created_date, format)}"
            )
        else:
            return f"Edited {format_date(edited_date, format)}"

    def is_git_repo(self):
        if self.github_repo:
            return True
        if self.path is None:
            return False
        return is_git_repo(self.path)

    def get_recent_commit_count(self, days: int = 30) -> int:
        if self.github_repo:
            since = datetime.now(timezone.utc) - timedelta(days=days)
            return self.github_repo.get_commits(since=since).totalCount
        elif self.path and self.is_git_repo():
            return get_commit_count(self.path, days=days)
        raise ValueError("Project is not a git repo")

    def format_line(
        self,
        prefix: str = "",
        show_size: bool = False,
        show_date: bool = True,
        format: DateFormatSettings = DateFormatSettings(),
        target_width: int = 100,
        github_user: Optional[str] = None,
    ) -> str:
        """Format project information into a display line

        Args:
            prefix: Optional prefix (e.g., "+", "-" for changes)
            show_size: Whether to show project size
            show_date: Whether to show date information

        Returns:
            Formatted line string
        """
        parts = []

        # Add prefix if provided
        if prefix:
            parts.append(f"{prefix} ")

        # Add size if requested
        if show_size:
            parts.append(f"[{self.size_formatted}] ")

        # Add project name with GitHub info if available
        name_part = self.name
        flag_1 = self.github_name and self.github_name != self.name
        flag_2 = github_user and self.github_org and self.github_org != github_user
        if flag_1 and flag_2:
            name_part = f" ({self.github_org}/{self.github_name})"
        elif flag_1:
            name_part += f" ({self.github_name})"
        elif flag_2:
            name_part = f"{self.github_org}/{name_part}"
        parts.append(name_part)

        # Add date if requested
        if show_date:
            date_str = self.date_formatted(format=format)
            to_pad = target_width - len(date_str) - sum(len(p) for p in parts)

            if to_pad > 0:
                parts.append(" " * to_pad)
            parts.append(f" ({date_str})")

        return "".join(parts)


class ProjectArranger:
    def __init__(self, config_path: Path, **kwargs):
        self.settings = ProjectArrangerSettings.from_yaml(config_path, **kwargs)
        self._github_client = MISSING

    def build_projects_list(self) -> List[Project]:
        """Discover all projects in configured paths"""
        logger.info("Building projects list...")
        local_projects = self._build_projets_list_local()
        github_projects = self._build_projets_list_github()
        merged_projects = self._merge_projects_lists(local_projects, github_projects)
        logger.info(
            f"Found {len(merged_projects)} total projects ({len(local_projects)} local, {len(github_projects)} GitHub)"
        )
        return merged_projects

    def _build_projets_list_local(self) -> List[Project]:
        """Discover all projects in local paths"""
        logger.info("Discovering local projects...")
        projects = []

        for root in self.settings.root_paths:
            root = root.expanduser()
            if not root.exists():
                logger.warning(f"Path {root} does not exist")
                continue

            # logger.info(f"Scanning directory: {root}")
            paths = [
                path
                for path in root.iterdir()
                if path.is_dir() and not path.name.startswith(".")
            ]
            logger.info(f"Found {len(paths)} directories in {root}")

            for path in paths:
                projects.append(Project(name=path.name, path=path.resolve()))

        logger.info(f"Found {len(projects)} local projects total")
        return projects

    def _build_projets_list_github(self) -> List[Project]:
        """Discover all projects in GitHub"""
        if self.github_client is None:
            logger.warning("GitHub client not available - skipping GitHub projects")
            return []

        logger.info("Discovering GitHub projects...")
        projects = []
        all_orgs = set()
        try:
            logger.info("Fetching repositories from GitHub API...")
            all_repos = list(self.github_client.get_user().get_repos())
            logger.info(f"Found {len(all_repos)} total repositories on GitHub")

            logger.info("Processing repositories...")
            for repo in all_repos:
                if repo.fork:  # Skip forked repos
                    continue

                org = repo.owner.login
                all_orgs.add(org)

                # Skip if org is in skip list
                if org in self.settings.github_skip_orgs:
                    logger.debug(
                        f"Skipping repo {repo.name} from org {org} (in skip list)"
                    )
                    continue

                # Skip if org list is specified and org not in it
                if self.settings.github_orgs and org not in self.settings.github_orgs:
                    logger.debug(
                        f"Skipping repo {repo.name} from org {org} (not in include list)"
                    )
                    continue

                # Create Project instance with GitHub metadata
                projects.append(Project(name=repo.name, github_repo=repo))

            # Log org info
            logger.info(
                f"Found {len(projects)} GitHub projects from orgs: {sorted(all_orgs)}"
            )
            if self.settings.github_orgs:
                logger.info(f"Including only orgs: {sorted(self.settings.github_orgs)}")
            if self.settings.github_skip_orgs:
                logger.info(f"Skipping orgs: {sorted(self.settings.github_skip_orgs)}")

        except Exception as e:
            logger.error(f"Failed to get GitHub projects: {e}")
            return []

        return projects

    def _merge_projects_lists(
        self, local_projects: List[Project], github_projects: List[Project]
    ) -> List[Project]:
        """Merge projects lists from local and GitHub"""
        logger.info("Merging local and GitHub project lists...")

        # Create lookup by GitHub URL for local projects
        logger.info("Building local projects lookup...")
        start_time = time.time()
        local_by_github = {}
        slow_projects = []

        for p in local_projects:
            project_start = time.time()
            if p.github_name and p.github_org:
                local_by_github[(p.github_org, p.github_name)] = p
            project_time = time.time() - project_start
            if project_time > 0.05:  # Log projects that take more than 50ms
                slow_projects.append((p.name, project_time))

        elapsed = time.time() - start_time
        logger.info(f"Built lookup in {elapsed:.2f}s")
        if slow_projects:
            logger.warning(
                f"Slow projects during lookup: {slow_projects[:5]}"
            )  # Show first 5

        # Add GitHub metadata to matching local projects
        logger.info("Matching GitHub projects with local...")
        matched_count = 0
        for github_proj in github_projects:
            key = (github_proj.github_org, github_proj.github_name)
            if key in local_by_github:
                local_proj = local_by_github[key]
                local_proj.github_repo = github_proj.github_repo
                matched_count += 1

        # Add GitHub-only projects
        github_only = [
            p
            for p in github_projects
            if (p.github_org, p.github_name) not in local_by_github
        ]

        logger.info(
            f"Merged projects: {matched_count} matched, {len(github_only)} GitHub-only"
        )
        return local_projects + github_only

    def get_current_groups(
        self, projects: List[Project]
    ) -> Dict[str, Dict[str, List[Project]]]:
        """Build groups dictionary based on current filesystem structure"""
        logger.info(f"Analyzing current groups for {len(projects)} projects...")
        groups: Dict[str, Dict[str, List[Project]]] = {
            "main": defaultdict(list),
            "secondary": defaultdict(list),
        }

        # Sort into main groups based on current directory structure
        for project in projects:
            current_group = project.current_group
            groups["main"][current_group].append(project)

        # Log current distribution
        current_counts = {
            group: len(projects) for group, projects in groups["main"].items()
        }
        logger.info(f"Current distribution: {current_counts}")

        # TODO: Implement secondary groups scanning
        # Will need to:
        # 1. Scan additional folders like 'templates/', 'ai-projects/', etc.
        # 2. Add a method to detect current secondary groups for a project
        # 3. Update Project class to support multiple current groups

        # Convert defaultdicts to regular dicts for return type compliance
        return {"main": dict(groups["main"]), "secondary": dict(groups["secondary"])}

    def sort_projects(
        self, projects: List[Project]
    ) -> Dict[str, Dict[str, List[Project]]]:
        """Sort projects into target categories based on config"""
        logger.info(f"Sorting {len(projects)} projects into groups...")
        groups = {
            "main": defaultdict(list),
            "secondary": defaultdict(list),
            "main_reason": {},
        }

        # Add progress tracking for slow operations
        processed = 0
        for project in tqdm(projects):
            project_start = time.time()
            main_group, reason = self._sort_projects_into_main_groups(project)
            secondary_groups = self._sort_projects_into_secondary_groups(project)
            project_time = time.time() - project_start

            if project_time > 0.1:  # Log slow projects
                logger.warning(
                    f"Slow project sorting: {project.name} took {project_time:.2f}s"
                )

            if (
                secondary_groups
                and (main_group in [Group.unsorted, Group.ignore])
                and (reason != "manual")
            ):
                reason = "has secondary groups"
                main_group = Group.archive
            groups["main"][main_group].append(project)
            groups["main_reason"][project.name] = reason
            for group in secondary_groups:
                groups["secondary"][group].append(project)

            processed += 1

        # Log summary
        main_counts = {
            group: len(projects) for group, projects in groups["main"].items()
        }
        logger.info(f"Sorted projects: {main_counts}")
        return groups

    async def sort_projects_async(
        self, projects: List[Project]
    ) -> Dict[str, Dict[str, List[Project]]]:
        """Async version of sort_projects for better performance with large project lists"""
        import asyncio

        logger.info(f"Sorting {len(projects)} projects into groups (async)...")
        groups = {
            "main": defaultdict(list),
            "secondary": defaultdict(list),
            "main_reason": {},
        }

        # Pre-calculate sizes async for all projects that need it
        logger.info("Pre-calculating project sizes...")
        size_tasks = []
        for project in projects:
            if project.path and self._needs_size_for_sorting(project):
                size_tasks.append(project.async_size())
            else:
                size_tasks.append(asyncio.sleep(0, result=0))  # No-op task

        # Run size calculations concurrently
        await asyncio.gather(*size_tasks)
        logger.info("Size calculations complete")

        # Now sort projects (this part is still mostly CPU-bound)
        for project in tqdm(projects):
            project_start = time.time()
            main_group, reason = self._sort_projects_into_main_groups(project)
            secondary_groups = self._sort_projects_into_secondary_groups(project)
            project_time = time.time() - project_start

            if project_time > 0.1:  # Log slow projects
                logger.warning(
                    f"Slow project sorting: {project.name} took {project_time:.2f}s"
                )

            if (
                secondary_groups
                and (main_group in [Group.unsorted, Group.ignore])
                and (reason != "manual")
            ):
                reason = "has secondary groups"
                main_group = Group.archive
            groups["main"][main_group].append(project)
            groups["main_reason"][project.name] = reason
            for group in secondary_groups:
                groups["secondary"][group].append(project)

        # Log summary
        main_counts = {
            group: len(projects) for group, projects in groups["main"].items()
        }
        logger.info(f"Sorted projects: {main_counts}")
        return groups

    def _needs_size_for_sorting(self, project: Project) -> bool:
        """Check if project sorting logic needs size calculation"""
        # Check if project would go through auto-sorting that uses size
        if project.name in (
            self.settings.ignore
            + self.settings.actual
            + self.settings.archive
            + self.settings.experiments
        ):
            return False  # Manual sorting, no size needed
        return True  # Auto-sorting may need size

    def _sort_projects_into_main_groups(self, project: Project) -> tuple[str, str]:
        """Sort projects into main groups"""
        # main groups: experiments, projects, archive and ignored
        # part 1: manually
        main_group = self._sort_main_manual(project)
        if main_group is not None:
            return main_group, "manual"
        # part 2: automatically
        main_group, reason = self._sort_main_auto(project)
        return main_group, reason

    def _sort_main_manual(self, project: Project) -> Optional[str]:
        """Sort projects into main groups manually"""
        # todo: figure out what to do if local name and github name are different
        if project.name in self.settings.ignore:
            return Group.ignore
        elif project.name in self.settings.actual:
            return Group.actual
        elif project.name in self.settings.archive:
            return Group.archive
        elif project.name in self.settings.experiments:
            return Group.experiments
        return None

    def _sort_main_auto(self, project: Project) -> tuple[str, str]:
        """Sort projects into main groups automatically. If not specified manually."""
        # idea 1: look at project date
        today = datetime.now()
        this_month = today - timedelta(days=30)

        # If created this month -> experiments
        # logger.debug(f"Checking created_date for {project.name}")
        if project.created_date > this_month:
            if project.current_group == Group.actual:
                return Group.actual, "already in actual"
            return Group.experiments, "created this month"

        # logger.debug(f"Checking date for {project.name}")
        if project.date > today - timedelta(days=self.settings.auto_sort_days):
            # look at the size / activity
            logger.debug(f"Checking git repo status for {project.name}")
            if (
                project.is_git_repo()
                and project.get_recent_commit_count(self.settings.auto_sort_days)
                > self.settings.auto_sort_commits
            ):
                # look at commit activity
                # - if more than 5 commits in the last 30 days - "actual"
                return Group.actual, "5+ recent commits"  # "actual"

            elif project.size > self.settings.auto_sort_size:
                return Group.actual, "recent and big"  # "actual"
            if project.current_group == Group.actual:
                return Group.actual, "already in actual"
            return Group.experiments, "recent but yet small"
        else:
            # look at project size
            logger.debug(f"Checking size for old project {project.name}")
            if project.size > self.settings.auto_sort_size:
                return Group.archive, "old but big"  # "archive"
            return Group.ignore, "old and small"  # "ignore"

    def _sort_projects_into_secondary_groups(self, project: Project) -> List[str]:
        """Sort projects into secondary groups"""
        # secondary groups: tags and collections.
        # - templates
        # - ai projects
        # ... etc.
        manual_sort = self._sort_secondary_manual(project)
        auto_sort = self._sort_secondary_auto(project)
        return list(set(manual_sort + auto_sort))

    def _sort_secondary_manual(self, project: Project) -> List[str]:
        """Sort projects into secondary groups manually
        Returns list of tags/collections the project should be sorted into."""
        res = []
        if project.name in self.settings.cool:
            res.append("cool")
        if project.name in self.settings.libs:
            res.append("libs")
        if project.name in self.settings.templates:
            res.append("templates")
        if project.name in self.settings.unfinished:
            res.append("unfinished")
        if project.name in self.settings.memorable:
            res.append("memorable")
        return res

    def _sort_secondary_auto(self, project: Project) -> List[str]:
        """Sort projects into secondary groups automatically. If not specified manually.
        Returns list of tags/collections the project should be sorted into."""
        res = []
        if "template" in project.name.lower():
            res.append("templates")
        return res

    @property
    def github_client(self):
        # todo: make sure to give warning instead of crashing
        if self._github_client is MISSING:
            from github import Github

            token = os.getenv("GITHUB_API_TOKEN")
            if token is None:
                logger.info("GITHUB API TOKEN not found in env. Loading ~/.env")
                from dotenv import load_dotenv

                load_dotenv(Path("~/.env").expanduser())
                token = os.getenv("GITHUB_API_TOKEN")

            if token is None:
                # raise ValueError('Missing GitHub API token')
                logger.warning("Missing GitHub API token")
                self._github_client = None
            else:
                self._github_client = Github(token)
        return self._github_client

    @cached_property
    def github_username(self) -> Optional[str]:
        if self.github_client is None:
            return None
        return self.github_client.get_user().login

    def print_all_results(self, groups, print_sizes: bool = False) -> None:
        """Print all projects in their groups"""
        print("Main Project Groups:")
        for group in Group.__members__:
            proj_list = groups["main"][group]
            print(f"{group.title()} ({len(proj_list)}):")
            for proj in sorted(proj_list, key=lambda x: x.name):
                reason = groups["main_reason"].get(proj.name, "")
                print(
                    f"- {proj.format_line(show_size=print_sizes, github_user=self.github_username)} [{reason}]"
                )
            print()

        print("\n" + "=" * 50 + "\n")

        print("Secondary Project Groups:")
        for group, proj_list in sorted(groups["secondary"].items()):
            print(f"{group.title()} ({len(proj_list)}):")
            for proj in sorted(proj_list, key=lambda x: x.name):
                print(
                    f"- {proj.format_line(show_size=print_sizes, github_user=self.github_username)}"
                )
            print()

    def print_changes(self, old_groups, new_groups, print_sizes: bool = False) -> None:
        """Print only the changes between old and new groups"""
        print("Changes in Main Project Groups:")
        for group in Group.__members__.values():
            old_projects = {p.name for p in old_groups["main"].get(group, [])}
            new_projects = {p.name for p in new_groups["main"].get(group, [])}

            added = new_projects - old_projects
            removed = old_projects - new_projects

            if added or removed:
                print(f"\n{group.title()}:")
                if added:
                    print("  Added:")
                    for proj_name in sorted(added):
                        proj = next(
                            p for p in new_groups["main"][group] if p.name == proj_name
                        )
                        reason = new_groups["main_reason"].get(proj.name, "")
                        print(
                            "  "
                            + proj.format_line(
                                prefix="+",
                                show_size=print_sizes,
                                github_user=self.github_username,
                            )
                            + f" [{reason}]"
                        )
                if removed:
                    print("  Removed:")
                    for proj_name in sorted(removed):
                        old_proj = next(
                            p for p in old_groups["main"][group] if p.name == proj_name
                        )
                        print(
                            "  "
                            + old_proj.format_line(
                                prefix="-",
                                show_size=print_sizes,
                                github_user=self.github_username,
                            )
                        )

        # Compare secondary groups
        if any(old_groups["secondary"]) or any(new_groups["secondary"]):
            print("\nChanges in Secondary Project Groups:")
            for group in set(old_groups["secondary"].keys()) | set(
                new_groups["secondary"].keys()
            ):
                old_projects = {p.name for p in old_groups["secondary"].get(group, [])}
                new_projects = {p.name for p in new_groups["secondary"].get(group, [])}

                added = new_projects - old_projects
                removed = old_projects - new_projects

                if added or removed:
                    print(f"\n{group.title()}:")
                    if added:
                        print("  Added:")
                        for proj_name in sorted(added):
                            proj = next(
                                p
                                for p in new_groups["secondary"][group]
                                if p.name == proj_name
                            )
                            print(
                                "  "
                                + proj.format_line(
                                    prefix="+",
                                    show_size=print_sizes,
                                    github_user=self.github_username,
                                )
                            )
                    if removed:
                        print("  Removed:")
                        for proj_name in sorted(removed):
                            old_proj = next(
                                p
                                for p in old_groups["secondary"][group]
                                if p.name == proj_name
                            )
                            print(
                                "  "
                                + old_proj.format_line(
                                    prefix="-",
                                    show_size=print_sizes,
                                    github_user=self.github_username,
                                )
                            )

from pathlib import Path
from typing import List, Set

import yaml
from pydantic_settings import BaseSettings

from dev_env.tools.project_arranger.src.utils import DateFormatSettings


class ProjectArrangerSettings(BaseSettings):
    # group 1: general
    dry_run: bool = True
    root_paths: List[Path]

    # group 2: manual sorting
    ## main groups
    ### ignore - skip cloning / remove
    ignore: Set[str] = set()
    ### actual - dir 'projects'
    actual: Set[str] = set()
    archive: Set[str] = set()
    experiments: Set[str] = set()

    ## secondary groups
    templates: Set[str] = set()
    libs: Set[str] = set()  # shared libraries and collections for reusing
    cool: Set[str] = set()  # ideas worth revisiting
    unfinished: Set[str] = set()  # have some work done, but not completed
    memorable: Set[str] = set()  # cool artifacts that were finished

    # group 3: auto sorting
    ## main groups
    ## secondary groups
    auto_sort_days: int = 30
    auto_sort_commits: int = 5
    auto_sort_size: int = 10000

    # group 4: extras
    ignored_dirs: Set[str] = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "build",
        "dist",
        ".pytest_cache",
    }
    source_extensions: Set[str] = {
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".java",
        ".cpp",
        ".c",
        ".h",
        ".hpp",
        ".rs",
        ".go",
        ".rb",
        ".php",
        ".html",
        ".css",
        ".scss",
        ".sql",
        ".sh",
    }

    # Date formatting format
    date_format: DateFormatSettings = DateFormatSettings()

    # GitHub settings
    # will include only these orgs
    github_orgs: List[str] = []
    # will include all except these
    github_skip_orgs: List[str] = []  # List of GitHub organizations to exclude

    @classmethod
    def from_yaml(cls, yaml_path: str | Path, **kwargs):
        with open(yaml_path) as f:
            yaml_settings = yaml.safe_load(f)
        yaml_settings.update(**kwargs)
        return cls(**yaml_settings)

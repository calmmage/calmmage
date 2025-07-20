from pathlib import Path

import yaml
from pydantic_settings import BaseSettings


class ProjectSettings(BaseSettings):
    # manual part
    ignored_projects: tuple[str] = ()
    main_projects: tuple[str] = ()

    # auto part

    # extras

    ignored_dirs: tuple[str] = (
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "build",
        "dist",
        ".pytest_cache",
    )
    source_extensions: tuple[str] = (
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
    )

    @classmethod
    def from_yaml(cls, yaml_path: str | Path):
        with open(yaml_path) as f:
            yaml_settings = yaml.safe_load(f)
        return cls(**yaml_settings)


# Usage:
# settings = ProjectSettings.from_yaml('config.yaml')

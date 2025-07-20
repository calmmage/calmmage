from pathlib import Path
from typing import Dict, List

import yaml
from pydantic_settings import BaseSettings


class ProjectDiscovererConfig(BaseSettings):
    # Glob patterns for different destination types
    glob_patterns: Dict[str, List[str]] = {
        "main": ["*"],  # Direct children only
        "examples": ["*/*", "*/*/*"],  # Up to 2 levels deep
        "library": ["dev/*", "dev/*/*"],  # dev folder patterns
    }
    # Special patterns for specific destinations
    seasonal_patterns: List[str] = ["seasonal/*/*/*"]  # seasonal/season_n/group/project
    seasonal_destinations: List[str] = ["calmmage-private", "calmmage"]

    @classmethod
    def from_yaml(cls, path: Path):
        with open(path) as f:
            return cls(**yaml.safe_load(f))

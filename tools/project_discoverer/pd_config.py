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
    seasonal_patterns: List[str] = [
        # experiments/season_n/project
        "experiments/season_*/*",
        # experiments/season_n/_archive/project
        "experiments/season_*/_archive/*"
    ]
    seasonal_destinations: List[str] = ["calmmage-private", "calmmage"]

    @classmethod
    def from_yaml(cls, path: Path):
        with open(path) as f:
            return cls(**yaml.safe_load(f))

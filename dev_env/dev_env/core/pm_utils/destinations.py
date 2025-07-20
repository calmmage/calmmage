from pathlib import Path
from typing import Dict, Optional

import yaml

from dev_env.core.pm_utils.project_utils import Destination


class DestinationsRegistry:
    """Universal registry of all work destinations"""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize destinations registry with config

        Args:
            config_path: Path to destinations config.
                        If None, uses default at package/config/destinations.yaml
        """
        if config_path is None:
            config_path = Path(__file__).parent / "config" / "destinations.yaml"

        self.config_path = config_path
        self._destinations = None

    @property
    def destinations(self) -> Dict[str, Destination]:
        """Get all destinations, loading from config if needed"""
        if self._destinations is None:
            with open(self.config_path) as f:
                data = yaml.safe_load(f)

            settings = data.get("settings", {})
            projects_root = Path(settings.get("projects_root", "~/work")).expanduser()

            self._destinations = {
                name: Destination(
                    name=dest["name"],
                    path=projects_root / dest["path"],
                    type=dest["type"].lower(),
                    description=dest["description"],
                    features=dest.get("features", []),
                )
                for name, dest in data["destinations"].items()
            }

        return self._destinations

    def get(self, name: str) -> Destination:
        """Get destination by name"""
        return self.destinations[name]

    def __getitem__(self, name: str) -> Destination:
        """Get destination by name using dict-like access"""
        return self.get(name)

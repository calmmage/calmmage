from pathlib import Path
from typing import List, Optional

from loguru import logger

from src.lib.pm_utils.destinations import DestinationsRegistry
from tools.project_discoverer.pd_config import ProjectDiscovererConfig


class ProjectDiscoverer:
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize ProjectDiscoverer with config and destinations registry"""
        if config_path is None:
            config_path = Path(__file__).parent / "pd_config.yaml"
        self.config = ProjectDiscovererConfig.from_yaml(config_path)
        self.dr = DestinationsRegistry()

    def quick_search(self, query: str) -> List[Path]:
        """Search for projects in common project directories"""
        results = []

        for dest in self.dr.destinations.values():
            if not dest.path.exists():
                logger.debug(f"Skipping non-existent destination: {dest.path}")
                continue

            logger.debug(f"Searching in destination: {dest.name} ({dest.path})")
            # Get patterns based on destination type
            if dest.name in self.config.seasonal_destinations:
                search_patterns = self.config.seasonal_patterns
                logger.debug(
                    f"Using seasonal patterns for {dest.name}: {search_patterns}"
                )
            elif dest.name == "examples":
                search_patterns = self.config.glob_patterns["examples"]
                logger.debug(
                    f"Using examples patterns for {dest.name}: {search_patterns}"
                )
            else:
                # todo: check this works fine
                search_patterns = self.config.glob_patterns.get(dest.type.value, [])
                logger.debug(
                    f"Using {dest.type.value} patterns for {dest.name}: {search_patterns}"
                )

            # Search using glob patterns
            for pattern in search_patterns:
                logger.debug(f"Searching with pattern: {pattern}")
                found = [
                    p
                    for p in dest.path.glob(pattern)
                    if p.is_dir() and query.lower() in p.name.lower()
                ]
                if found:
                    logger.debug(
                        f"Found {len(found)} matches with pattern {pattern}: {found}"
                    )
                results.extend(found)

        return sorted(results)

    def get_outer_project_dirs(self, path):
        """Find all project directories that are parent of the given path"""
        res = []
        for p in [path] + list(path.parents):
            try:
                # mini-projects
                # todo: add the new 'season' folder logic
                if p.parent.name in [
                    "draft",
                    "wip",
                    "unsorted",
                    "paused",
                    "_archive",
                ] or p.parent.name.startswith("season_"):
                    logger.debug(f"Found mini-project: {p}")
                    res.append(p)


                # main destinations
                # todo: use destinations registry instead!
                if p.parent.name in ["experiments", "archive", "projects"]:
                    logger.debug(f"Found main project: {p}")
                    res.append(p)

                # todo: think if any other heuristics are needed here
            except Exception as e:
                logger.error(f"Failed to process path {p}: {e}")
        return sorted(str(p) for p in res)

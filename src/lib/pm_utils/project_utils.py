from enum import Enum
from pathlib import Path
from typing import List, Optional

from loguru import logger
from pydantic import BaseModel


class DestinationType(str, Enum):
    """Types of destinations"""

    MAIN = "main"  # experiments, projects, archive
    REPOSITORY = "repo"  # examples, calmmage, calmmage-private
    LIBRARY = "library"  # botspot, calmlib
    SPECIAL = "special"  # templates, to_remove


class Destination(BaseModel):
    """Project destination with metadata"""

    name: str
    path: Path
    type: DestinationType
    description: str
    features: List[str]  # e.g. ["New projects", "Prototypes", "Recent experiments"]

    @property
    def full_path(self) -> Path:
        return Path("~/work").expanduser() / self.path

    @classmethod
    def get_standard_destinations(cls) -> List["Destination"]:
        """Get list of standard project destinations"""
        return [
            cls(
                name="experiments",
                path="experiments",
                type=DestinationType.MAIN,
                description="New projects and prototypes",
                features=[
                    "New projects and prototypes",
                    "Recent experiments (< 30 days old)",
                    "Small projects under active development",
                ],
            ),
            cls(
                name="projects",
                path="projects",
                type=DestinationType.MAIN,
                description="Main active projects",
                features=[
                    "Main active projects",
                    "Production-ready code",
                    "Actively maintained repositories",
                ],
            ),
            # ... other destinations
        ]


class ProjectContext(BaseModel):
    """Project metadata and context"""

    name: str
    path: Optional[Path] = None
    destination: Optional[Destination] = None
    is_git_repo: bool = False
    github_org: Optional[str] = None
    github_name: Optional[str] = None


class ProjectDiscovery:
    """Utility class for discovering project context"""

    def __init__(self):
        self.destinations = Destination.get_standard_destinations()

    def get_current_project(self) -> Optional[ProjectContext]:
        """Try to detect current project based on working directory"""
        try:
            current_dir = Path.cwd()
            return ProjectContext(
                name=current_dir.name,
                path=current_dir,
                destination=self._detect_destination(current_dir),
            )
        except Exception as e:
            logger.warning(f"Failed to detect current project: {e}")
            return None

    def _detect_destination(self, path: Path) -> Optional[Destination]:
        """Detect project destination based on path"""
        try:
            abs_path = path.resolve()
            path_str = str(abs_path).lower()

            for dest in self.destinations:
                if f"/work/{dest.name}/" in path_str:
                    return dest

            return None
        except Exception as e:
            logger.warning(f"Failed to detect destination for {path}: {e}")
            return None

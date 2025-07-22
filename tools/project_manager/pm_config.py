from pathlib import Path

from pydantic_settings import BaseSettings


class ProjectManagerConfig(BaseSettings):
    """Project Manager configuration"""

    # Project creation settings
    experiments_destination: str = (
        "projects"  # Key in destinations registry. New projects now go to projects/ dir
    )
    private_mini_projects_destination: str = (
        "calmmage-private"  # For private mini-projects
    )
    public_mini_projects_destination: str = "calmmage"  # For public mini-projects

    # Feature creation settings
    features_subfolder: Path = Path("dev/draft")

    # Todo creation settings
    todo_subfolder: Path = Path("dev")
    todo_filename_template: str = "todo_%d_%b.md"  # e.g. todo_17_Nov.md

    # Editor settings
    # default_editor: str = "cursor"
    default_editor: str = "subl"

    # name convention
    always_use_hyphens: bool = (
        True  # Auto convert underscores to hyphens in project names
    )

    # Seasonal folder settings
    seasonal_folder_threshold: int = 15  # Max projects before rolling to new folder

    @classmethod
    def from_yaml(cls, path: Path) -> "ProjectManagerConfig":
        """Load config from yaml file"""
        import yaml

        with open(path) as f:
            return cls(**yaml.safe_load(f))

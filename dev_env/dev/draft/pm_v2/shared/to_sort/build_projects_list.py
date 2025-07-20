import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Set

from dotenv import load_dotenv
from github import Github
from loguru import logger
from pydantic import BaseModel
from tqdm.auto import tqdm

load_dotenv()


class Project(BaseModel):
    name: str
    path: Optional[Path] = None
    source: str  # 'github' or 'local' or 'both'
    last_modified: datetime
    is_git_repo: bool
    github_url: Optional[str] = None

    def __hash__(self):
        # Use name as primary key for deduplication
        # todo: do a complex logic including github remote
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Project):
            return False
        # todo: do a complex logic including github remote
        return self.name == other.name
        # return self.name == other.name and str(self.path) == str(other.path)

    class Config:
        frozen = True  # Makes the model immutable, which is required for hashing


class ProjectCollector:
    def __init__(self):
        self.projects: Set[Project] = set()
        self.default_paths = [
            Path.home() / "work/experiments",
            Path.home() / "work/projects",
            Path.home() / "work/archive",
        ]
        self.allowed_teams = [
            "calmmage",
            "Augmented-development",
            "engineering-friends",
            "lavrpetrov",
        ]
        self.github_client = Github(os.getenv("GITHUB_TOKEN"))

    def discover_local_projects(self) -> None:
        """Discover projects from local directories"""
        logger.info("Discovering local projects...")
        for base_path in self.default_paths:
            if not base_path.exists():
                logger.warning(f"Path {base_path} does not exist")
                continue

            for path in base_path.glob("*"):
                if path.is_dir():
                    is_git = (path / ".git").exists()
                    last_modified = datetime.fromtimestamp(path.stat().st_mtime)

                    project = Project(
                        name=path.name,
                        path=path,
                        source="local",
                        last_modified=last_modified,
                        is_git_repo=is_git,
                    )
                    self.projects.add(project)

    def discover_github_projects(self) -> None:
        """Discover projects from GitHub"""
        logger.info("Discovering GitHub projects...")
        repos = list(self.github_client.get_user().get_repos())

        for repo in tqdm(repos):
            full_repo_name = repo.full_name
            if not any(full_repo_name.startswith(team) for team in self.allowed_teams):
                logger.debug(f"Skipping {full_repo_name} - not in allowed teams")
                continue

            # Check if project already exists locally
            existing_project = next(
                (p for p in self.projects if p.name == repo.name), None
            )

            if existing_project:
                # Merge GitHub info with local project
                merged_project = Project(
                    name=repo.name,
                    path=existing_project.path,
                    source="both",
                    last_modified=repo.updated_at,
                    is_git_repo=True,
                    github_url=repo.clone_url,
                )
                self.projects.remove(existing_project)
                self.projects.add(merged_project)
            else:
                # Add new GitHub project
                project = Project(
                    name=repo.name,
                    source="github",
                    last_modified=repo.updated_at,
                    is_git_repo=True,
                    github_url=repo.clone_url,
                )
                self.projects.add(project)

    def save_projects(self, output_file: Path) -> None:
        """Save projects to JSON file"""
        projects_data = [
            {
                "name": p.name,
                "path": str(p.path) if p.path else None,
                # "path": str(p.path),
                "source": p.source,
                "last_modified": p.last_modified.isoformat(),
                "is_git_repo": p.is_git_repo,
            }
            for p in self.projects
        ]

        output_file.write_text(json.dumps(projects_data, indent=2))


def main():
    logger.info("Starting project discovery")
    collector = ProjectCollector()
    collector.discover_local_projects()

    output_path = Path(
        "../../../../../tools/project_arrangement/dev/projects_list.json"
    )
    collector.save_projects(output_path)
    logger.info(f"Projects list saved to {output_path}")


if __name__ == "__main__":
    main()

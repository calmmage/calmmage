"""Project discovery utilities for automation and management."""

from pathlib import Path
from typing import List, Optional, Set
import yaml
from loguru import logger

from .project import Project


DEFAULT_PROJECT_PATHS = [
    "~/work/projects",
    "~/work/archive"
]


def get_local_projects(
    config_path: Optional[Path] = None,
    root_paths: Optional[List[str]] = None,
    include_github: bool = False
) -> List[Project]:
    """Fast project discovery for automation scripts.
    
    Args:
        config_path: Optional path to project arranger config
        root_paths: Override default project paths
        include_github: Whether to include GitHub metadata (slower)
        
    Returns:
        List of Project objects with name and path
        
    Usage:
        projects = get_local_projects()
        for project in projects:
            uv_sync(project.path)
    """
    if root_paths is None:
        if config_path:
            root_paths = _load_root_paths_from_config(config_path)
        else:
            root_paths = DEFAULT_PROJECT_PATHS
    
    projects = []
    for root_str in root_paths:
        root = Path(root_str).expanduser()
        if not root.exists():
            logger.warning(f"Path {root} does not exist")
            continue
            
        for path in root.iterdir():
            if path.is_dir() and not path.name.startswith("."):
                projects.append(Project(name=path.name, path=path.resolve()))
    
    logger.info(f"Found {len(projects)} local projects")
    return projects


def get_projects_extended(
    config_path: Optional[Path] = None,
    include_github: bool = True,
    github_orgs: Optional[List[str]] = None,
    github_skip_orgs: Optional[List[str]] = None
) -> List[Project]:
    """Comprehensive project discovery with GitHub integration.
    
    Args:
        config_path: Path to project arranger config
        include_github: Whether to fetch GitHub metadata
        github_orgs: GitHub orgs to include (if specified, only these)
        github_skip_orgs: GitHub orgs to skip
        
    Returns:
        List of Project objects with full metadata
        
    Usage:
        projects = get_projects_extended()
        for project in projects:
            print(f"{project.name}: {project.size_formatted}")
    """
    # Get local projects first
    projects = get_local_projects(config_path=config_path)
    
    if include_github:
        # Import GitHub functionality only when needed
        try:
            from tools.project_arranger.src.main import ProjectArranger
            from tools.project_arranger.src.config import ProjectArrangerSettings
            
            # Create minimal config for GitHub discovery
            if config_path:
                settings = ProjectArrangerSettings.from_yaml(config_path)
            else:
                settings = ProjectArrangerSettings(
                    root_paths=[Path(p) for p in DEFAULT_PROJECT_PATHS],
                    github_orgs=github_orgs or [],
                    github_skip_orgs=github_skip_orgs or []
                )
            
            arranger = ProjectArranger(config_path or Path("dummy"), **settings.dict())
            github_projects = arranger._build_projets_list_github()
            projects = arranger._merge_projects_lists(projects, github_projects)
            
        except Exception as e:
            logger.warning(f"Failed to load GitHub projects: {e}")
    
    logger.info(f"Found {len(projects)} total projects")
    return projects


def find_project(name: str, config_path: Optional[Path] = None) -> Optional[Project]:
    """Find a specific project by name.
    
    Args:
        name: Project name to search for
        config_path: Optional config path for discovery
        
    Returns:
        Project object if found, None otherwise
        
    Usage:
        project = find_project("calmmage")
        if project:
            deploy_ai_rules(project.path)
    """
    projects = get_local_projects(config_path=config_path)
    for project in projects:
        if project.name == name:
            return project
    return None


def _load_root_paths_from_config(config_path: Path) -> List[str]:
    """Load root_paths from project arranger config."""
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return config.get("root_paths", DEFAULT_PROJECT_PATHS)
    except Exception as e:
        logger.warning(f"Failed to load config {config_path}: {e}")
        return DEFAULT_PROJECT_PATHS
#!/usr/bin/env python3
"""UV sync automation job - synchronize UV environments across all projects."""

import subprocess
from pathlib import Path
from loguru import logger

from src.lib.coding_projects import get_local_projects


def run_uv_sync(project_path: Path) -> bool:
    """Run uv sync in a project directory.
    
    Args:
        project_path: Path to the project
        
    Returns:
        True if successful, False otherwise
    """
    try:
        result = subprocess.run(
            ["uv", "sync"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            logger.info(f"✅ UV sync successful: {project_path.name}")
            return True
        else:
            logger.warning(f"❌ UV sync failed: {project_path.name} - {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error(f"⏱️ UV sync timeout: {project_path.name}")
        return False
    except Exception as e:
        logger.error(f"💥 UV sync error: {project_path.name} - {e}")
        return False


def has_uv_project(project_path: Path) -> bool:
    """Check if project has UV configuration files."""
    return (
        (project_path / "pyproject.toml").exists() or
        (project_path / "uv.lock").exists() or
        (project_path / ".python-version").exists()
    )


def main():
    """Synchronize UV environments across all discovered projects."""
    logger.info("🔄 Starting UV sync across all projects...")
    
    projects = get_local_projects()
    uv_projects = [p for p in projects if has_uv_project(p.path)]
    
    logger.info(f"Found {len(uv_projects)} projects with UV configuration out of {len(projects)} total")
    
    if not uv_projects:
        logger.info("No UV projects found, nothing to sync")
        return
    
    success_count = 0
    for project in uv_projects:
        logger.info(f"Syncing {project.name}...")
        if run_uv_sync(project.path):
            success_count += 1
    
    logger.info(f"✅ UV sync completed: {success_count}/{len(uv_projects)} projects successful")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Shared utilities for the calmmage project.

This module provides common utilities and constants used across the project,
including path resolution and project root detection.
"""

from pathlib import Path

# Project root directory - two levels up from this file
# src/lib/utils.py -> src/lib -> src -> project_root
repo_root = Path(__file__).parent.parent.parent

def get_repo_root() -> Path:
    """
    Get the repository root directory.
    
    Returns:
        Path: The absolute path to the repository root directory
    """
    return repo_root.resolve()

def get_scripts_dir() -> Path:
    """
    Get the scripts directory within the repository.
    
    Returns:
        Path: The absolute path to the scripts directory
    """
    return repo_root / "scripts"

def get_scheduled_tasks_dir() -> Path:
    """
    Get the scheduled tasks directory within the scripts directory.
    
    Returns:
        Path: The absolute path to the scheduled_tasks directory
    """
    return repo_root / "scripts" / "scheduled_tasks"

def get_config_dir() -> Path:
    """
    Get the config directory within the repository.
    
    Returns:
        Path: The absolute path to the config directory
    """
    return repo_root / "config"

def get_tools_dir() -> Path:
    """
    Get the tools directory within the repository.
    
    Returns:
        Path: The absolute path to the tools directory
    """
    return repo_root / "tools"

def get_experiments_dir() -> Path:
    """
    Get the experiments directory within the repository.
    
    Returns:
        Path: The absolute path to the experiments directory
    """
    return repo_root / "experiments"

def get_projects_dir() -> Path:
    """
    Get the projects directory within the repository.
    
    Returns:
        Path: The absolute path to the projects directory (calmmage is nested)
    """
    return repo_root  # The calmmage project itself is the "projects" directory

# Backward compatibility
def get_project_root() -> Path:
    """
    Alias for get_repo_root() for backward compatibility.
    
    Returns:
        Path: The absolute path to the repository root directory
    """
    return get_repo_root()
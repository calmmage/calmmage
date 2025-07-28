"""Coding projects library for project discovery and management."""

from .project import Project
from .discovery import get_local_projects, get_projects_extended, find_project

__all__ = ["Project", "get_local_projects", "get_projects_extended", "find_project"]
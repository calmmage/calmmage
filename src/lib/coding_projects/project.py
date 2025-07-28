"""Base Project class for coding project discovery and management."""

from pathlib import Path
from typing import Optional
from pydantic import BaseModel


class Project(BaseModel):
    """
    Base class for representing a coding project.
    
    This serves as the foundation for project discovery and management tools.
    Contains core project properties that are universally useful.
    
    EMPTY FOR NOW - will be populated as functionality is migrated from project_arranger.
    """
    
    name: str
    path: Optional[Path] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def __hash__(self):
        """Make Project hashable for use in sets and as dict keys"""
        return hash((self.name, str(self.path) if self.path else None))

    def __eq__(self, other):
        """Define equality for Project objects"""
        if not isinstance(other, Project):
            return False
        return self.name == other.name and self.path == other.path
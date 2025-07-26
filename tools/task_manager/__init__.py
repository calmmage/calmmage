"""Task Management Tool - A fuzzy parser for markdown task lists."""

from .fuzzy_parser import FuzzyTaskParser, TaskItem, TextLocation

__version__ = "0.1.0"
__all__ = ["FuzzyTaskParser", "TaskItem", "TextLocation"]
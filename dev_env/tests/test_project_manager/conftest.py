from datetime import datetime, timedelta
from pathlib import Path
from typing import List

import pytest
from loguru import logger
from pydantic import BaseModel

from dev_env.tools.project_manager.project_manager import ProjectManager


# Add this class to mock the config structure
class MockProjectDiscovererConfig(BaseModel):
    root_dirs: List[Path]

    @classmethod
    def from_yaml(cls, path):
        return cls(root_dirs=[Path("path/to/projects"), Path("another/path")])


@pytest.fixture
def sample_project_dir(tmp_path):
    """Create a sample project directory with dev subfolder for todos"""
    project_dir = tmp_path / "sample_project"
    # Use dev subfolder as specified in pm_config.yaml
    dev_dir = project_dir / "dev"
    dev_dir.mkdir(parents=True)
    return project_dir


@pytest.fixture
def mock_pm_config_file(tmp_path):
    """Create a mock project manager config file"""
    config_content = """
# Project Manager Configuration
# experiments_destination: "experiments"
# mini_projects_destination: "calmmage-private"
# public_mini_projects_destination: "calmmage"
# features_subfolder: "dev/draft"
# todo_subfolder: "dev"
# todo_filename_template: "todo_%d_%b.md"
# default_editor: "subl"
# # Project Manager Configuration

# # Editor settings
default_editor: "subl"

"""
    config_file = tmp_path / "pm_config.yaml"
    config_file.write_text(config_content)
    return config_file


@pytest.fixture
def pm_config(mock_pm_config_file):
    """Get ProjectManager config for testing"""
    pm = ProjectManager(config_path=mock_pm_config_file)
    return pm.config


@pytest.fixture
def sample_todos(sample_project_dir, pm_config):
    """Create sample todo files with different dates in dev folder"""
    dev_dir = sample_project_dir / pm_config.todo_subfolder

    # Create todo files for the last few days
    today = datetime.now()

    # Helper to create todo file
    def create_todo(date: datetime, content: str):
        filename = date.strftime(pm_config.todo_filename_template)
        (dev_dir / filename).write_text(content)
        logger.debug(f"Created test todo file: {filename}")

    # Create sample todos
    create_todo(today - timedelta(days=2), "- Task from 2 days ago\n- Another old task")
    create_todo(today - timedelta(days=1), "- Yesterday's task")
    create_todo(today, "- Today's task")

    return dev_dir


@pytest.fixture
def pm_with_custom_editor(monkeypatch, mock_pm_config_file):
    """Create ProjectManager instance with a mock editor command"""

    def mock_editor(self, path):
        logger.debug(f"Mock editor called with: {path}")
        return

    # Patch the open_in_editor method to prevent actual editor opening
    monkeypatch.setattr(ProjectManager, "open_in_editor", mock_editor)

    return ProjectManager(config_path=mock_pm_config_file)


# @pytest.fixture
# def mock_pd_config(tmp_path, monkeypatch):
#     """Create a mock project discoverer config file"""
#     config_content = """
# # Project Discoverer Configuration
# root_dirs:
#   - path/to/projects
#   - another/path
# """
#     config_file = tmp_path / "pd_config.yaml"
#     config_file.write_text(config_content)
#
#     # Mock the entire config class
#     monkeypatch.setattr(
#         "dev_env.tools.project_discoverer.pd_config.ProjectDiscovererConfig",
#         MockProjectDiscovererConfig,
#     )
#
#     return config_file

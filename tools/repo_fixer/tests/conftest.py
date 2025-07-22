"""Test configuration and shared fixtures."""

from pathlib import Path
from textwrap import dedent

import pytest
from loguru import logger


@pytest.fixture
def broken_repo(tmp_path: Path) -> Path:
    """Create a repository with incorrect project name setup."""
    repo_path = tmp_path / "my-cool-project"
    repo_path.mkdir(exist_ok=True)
    logger.info(f"Created test repo at: {repo_path}")

    # Create pyproject.toml with wrong name
    pyproject_content = dedent(
        """
        [tool.poetry]
        name = "project-name"  # This should be fixed
        version = "0.1.0"
        description = "Test project"

        [tool.poetry.dependencies]
        python = "^3.11"
        """
    )
    (repo_path / "pyproject.toml").write_text(pyproject_content)

    # Create source directory with wrong name
    (repo_path / "project_name").mkdir(exist_ok=True)
    (repo_path / "project_name" / "__init__.py").touch()

    return repo_path


@pytest.fixture
def correct_repo(tmp_path: Path) -> Path:
    """Create a repository with correct project name setup."""
    repo_path = tmp_path / "correct-project"
    repo_path.mkdir(exist_ok=True)
    logger.info(f"Created test repo at: {repo_path}")

    # Create pyproject.toml with correct name
    pyproject_content = dedent(
        """
        [tool.poetry]
        name = "my-cool-project"
        version = "0.1.0"
        description = "Test project"
        [tool.poetry.dependencies]
        python = "^3.11"
        [[tool.poetry.packages]]
        include = "my_cool_project"
        from = "."
        """
    )
    (repo_path / "pyproject.toml").write_text(pyproject_content)

    # Create source directory with correct name
    (repo_path / "my_cool_project").mkdir(exist_ok=True)
    (repo_path / "my_cool_project" / "__init__.py").touch()

    return repo_path

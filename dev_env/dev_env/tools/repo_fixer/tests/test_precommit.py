"""Tests for pre-commit configuration functionality."""

from pathlib import Path
from textwrap import dedent

import pytest

from dev_env.tools.repo_fixer.repo_fixer import _add_precommit_tool_if_missing


@pytest.fixture
def empty_repo(tmp_path: Path) -> Path:
    """Create an empty repository."""
    repo_path = tmp_path / "empty-repo"
    repo_path.mkdir(exist_ok=True)

    # Create minimal pyproject.toml
    pyproject_content = dedent(
        """
        [tool.poetry]
        name = "empty-repo"
        version = "0.1.0"
        description = "Test project"
        
        [tool.poetry.dependencies]
        python = "^3.11"
        """
    )
    (repo_path / "pyproject.toml").write_text(pyproject_content)
    return repo_path


@pytest.fixture
def repo_with_empty_precommit(empty_repo: Path) -> Path:
    """Create a repository with an empty .pre-commit-config.yaml."""
    (empty_repo / ".pre-commit-config.yaml").touch()
    return empty_repo


@pytest.fixture
def repo_with_precommit(empty_repo: Path) -> Path:
    """Create a repository with an existing .pre-commit-config.yaml."""
    content = dedent(
        """
        repos:
          - repo: https://github.com/psf/black
            rev: 24.2.0
            hooks:
              - id: black
                args: [ --line-length=100 ]
        """
    )
    (empty_repo / ".pre-commit-config.yaml").write_text(content)
    return empty_repo


def test_create_new_precommit(empty_repo: Path):
    """Test creating a new pre-commit config file."""
    test_content = dedent(
        """
        - repo: https://github.com/test/test
          rev: v1.0.0
          hooks:
            - id: test-hook
        """
    )

    _add_precommit_tool_if_missing(empty_repo, "test-hook", test_content)

    config_path = empty_repo / ".pre-commit-config.yaml"
    assert config_path.exists()

    content = config_path.read_text()
    assert content.startswith("repos:\n")
    assert "test-hook" in content


def test_add_to_empty_precommit(repo_with_empty_precommit: Path):
    """Test adding a tool to an empty pre-commit config."""
    test_content = dedent(
        """
        - repo: https://github.com/test/test
          rev: v1.0.0
          hooks:
            - id: test-hook
        """
    )

    _add_precommit_tool_if_missing(repo_with_empty_precommit, "test-hook", test_content)

    content = (repo_with_empty_precommit / ".pre-commit-config.yaml").read_text()
    assert content.startswith("repos:\n")
    assert "test-hook" in content


def test_add_to_existing_precommit(repo_with_precommit: Path):
    """Test adding a tool to an existing pre-commit config."""
    test_content = dedent(
        """
        - repo: https://github.com/test/test
          rev: v1.0.0
          hooks:
            - id: test-hook
        """
    )

    _add_precommit_tool_if_missing(repo_with_precommit, "test-hook", test_content)

    content = (repo_with_precommit / ".pre-commit-config.yaml").read_text()
    assert content.startswith("repos:\n")
    assert "black" in content  # Original content preserved
    assert "test-hook" in content  # New content added


def test_skip_existing_tool(repo_with_precommit: Path):
    """Test that adding an existing tool is skipped."""
    test_content = dedent(
        """
        - repo: https://github.com/psf/black
          rev: different-version
          hooks:
            - id: black
        """
    )

    original_content = (repo_with_precommit / ".pre-commit-config.yaml").read_text()
    _add_precommit_tool_if_missing(repo_with_precommit, "black", test_content)

    new_content = (repo_with_precommit / ".pre-commit-config.yaml").read_text()
    assert new_content == original_content  # Content unchanged

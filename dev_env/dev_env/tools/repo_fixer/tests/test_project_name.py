"""Tests for project name discovery and fixing functionality."""

from pathlib import Path

from dev_env.tools.repo_fixer.repo_fixer import (
    _get_source_dir_name,
    check_and_fix_poetry_project_name,
)


def test_project_name_discovery(broken_repo: Path):
    """Test that project name is correctly discovered from repo path."""
    source_dir = _get_source_dir_name(broken_repo)
    assert source_dir == "my_cool_project"

    # Check that source directory exists
    assert (broken_repo / source_dir).exists()

    # Check that pyproject.toml was updated
    with open(broken_repo / "pyproject.toml") as f:
        content = f.read()
        assert 'name = "my-cool-project"' in content


def test_project_name_fix(broken_repo: Path):
    """Test that project name is correctly fixed in pyproject.toml."""
    check_and_fix_poetry_project_name(broken_repo, "my-cool-project")

    # Verify pyproject.toml was updated
    with open(broken_repo / "pyproject.toml") as f:
        content = f.read()
        assert 'name = "my-cool-project"' in content
        assert 'name = "project-name"' not in content


def test_source_dir_rename(broken_repo: Path):
    """Test that source directory is correctly renamed."""
    source_dir = _get_source_dir_name(broken_repo)

    # Check old directory is gone
    assert not (broken_repo / "project_name").exists()

    # Check new directory exists with correct name
    assert (broken_repo / "my_cool_project").exists()
    assert (broken_repo / "my_cool_project" / "__init__.py").exists()


def test_correct_repo_unchanged(correct_repo: Path):
    """Test that correctly named repo is not modified."""
    original_content = (correct_repo / "pyproject.toml").read_text()

    source_dir = _get_source_dir_name(correct_repo)
    assert source_dir == "my_cool_project"

    # Verify nothing was changed
    assert (correct_repo / "pyproject.toml").read_text() == original_content
    assert (correct_repo / "my_cool_project").exists()

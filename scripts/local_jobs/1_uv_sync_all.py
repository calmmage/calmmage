#!/usr/bin/env python3
"""UV sync automation job - synchronize UV environments across all projects."""

import subprocess
import sys
import toml
from pathlib import Path

from src.lib.coding_projects import get_local_projects


def run_uv_sync(project_path: Path) -> bool:
    """Run uv sync with all groups in a project directory.
    
    Args:
        project_path: Path to the project
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Try syncing with all available groups first
        groups = get_dependency_groups(project_path)
        
        if groups:
            # Build command with all groups
            cmd = ["uv", "sync", "--upgrade"]
            for group in groups:
                cmd.extend(["--group", group])
        else:
            # Fallback to basic sync
            cmd = ["uv", "sync", "--upgrade"]
        
        print(f"  Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            print(f"  ✅ UV sync successful: {project_path.name}")
            return True
        else:
            print(f"  ❌ UV sync failed: {project_path.name}")
            print(f"     Error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"  ⏱️ UV sync timeout: {project_path.name}")
        return False
    except Exception as e:
        print(f"  💥 UV sync error: {project_path.name} - {e}")
        return False


def get_dependency_groups(project_path: Path) -> list[str]:
    """Extract dependency groups from pyproject.toml."""
    pyproject_path = project_path / "pyproject.toml"
    if not pyproject_path.exists():
        return []
    
    try:
        with open(pyproject_path) as f:
            data = toml.load(f)
        
        # Look for dependency groups in UV format
        dependency_groups = data.get("dependency-groups", {})
        return list(dependency_groups.keys())
        
    except Exception:
        return []


def has_uv_project(project_path: Path) -> bool:
    """Check if project is a UV project (not Poetry)."""
    pyproject_path = project_path / "pyproject.toml"
    uv_lock_path = project_path / "uv.lock"
    
    # Must have pyproject.toml
    if not pyproject_path.exists():
        return False
    
    # If has uv.lock, definitely UV project
    if uv_lock_path.exists():
        return True
    
    # Check if it's NOT a Poetry project
    try:
        with open(pyproject_path) as f:
            data = toml.load(f)
        
        # Poetry projects have [tool.poetry] section
        if "tool" in data and "poetry" in data["tool"]:
            return False
            
        # UV projects typically have [dependency-groups] or [project]
        if "dependency-groups" in data or "project" in data:
            return True
            
    except Exception:
        pass
    
    return False


def main():
    """Synchronize UV environments across all discovered projects."""
    try:
        projects = get_local_projects()
        uv_projects = [p for p in projects if has_uv_project(p.path)]
        
        print(f"Found {len(uv_projects)} UV projects out of {len(projects)} total projects")
        
        if not uv_projects:
            print("🎯 FINAL STATUS: success")
            print("📝 FINAL NOTES: No UV projects found")
            return 0
        
        success_count = 0
        archive_path = Path.home() / "work/archive"
        for project in uv_projects:
            if archive_path in project.path.parents:
                continue
            print(f"Syncing {project.name}...")
            if run_uv_sync(project.path):
                success_count += 1
        
        if success_count == len(uv_projects):
            print("🎯 FINAL STATUS: success")
        elif success_count == 0:
            print("🎯 FINAL STATUS: fail")
        else:
            print("🎯 FINAL STATUS: requires_attention")
        
        print(f"📝 FINAL NOTES: {len(uv_projects)} UV projects, {success_count} successful")
        return 0
        
    except Exception as e:
        print(f"🎯 FINAL STATUS: fail")
        print("📝 FINAL NOTES: Check discovery/UV install")
        return 1


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""Git sync automation job - synchronize git repositories across all projects."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

from src.lib.coding_projects import get_local_projects


def run_git_command(project_path: Path, command: list[str]) -> tuple[bool, str, str]:
    """Run a git command in a project directory.
    
    Args:
        project_path: Path to the project
        command: Git command as list (e.g., ['git', 'status', '--porcelain'])
        
    Returns:
        tuple of (success: bool, stdout: str, stderr: str)
    """
    try:
        result = subprocess.run(
            command,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60  # 1 minute timeout
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "Git command timed out"
    except Exception as e:
        return False, "", f"Git command failed: {e}"


def has_local_changes(project_path: Path) -> bool:
    """Check if project has uncommitted local changes."""
    success, stdout, _ = run_git_command(project_path, ["git", "status", "--porcelain"])
    return success and bool(stdout.strip())


def has_remote_changes(project_path: Path) -> tuple[bool, bool]:
    """Check if remote has changes to pull.
    
    Returns:
        tuple of (fetch_success: bool, has_changes: bool)
    """
    # First fetch to update remote refs
    fetch_success, _, _ = run_git_command(project_path, ["git", "fetch"])
    if not fetch_success:
        return False, False
    
    # Check if remote is ahead of local
    success, stdout, _ = run_git_command(project_path, ["git", "rev-list", "HEAD..origin/main", "--count"])
    if not success:
        # Try 'master' if 'main' doesn't exist
        success, stdout, _ = run_git_command(project_path, ["git", "rev-list", "HEAD..origin/master", "--count"])
    
    if success and stdout.isdigit():
        return True, int(stdout) > 0
    return True, False  # Assume no changes if we can't determine


def create_backup_branch(project_path: Path) -> tuple[bool, str]:
    """Create a backup branch with timestamp.
    
    Returns:
        tuple of (success: bool, branch_name: str)
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    base_name = f"daily-snapshots/{date_str}"
    
    # Check if base name exists
    success, _, _ = run_git_command(project_path, ["git", "rev-parse", "--verify", base_name])
    if not success:
        # Base name doesn't exist, use it
        branch_name = base_name
    else:
        # Find available name with suffix
        for i in range(1, 100):  # Limit to 100 attempts
            branch_name = f"{base_name}-{i}"
            success, _, _ = run_git_command(project_path, ["git", "rev-parse", "--verify", branch_name])
            if not success:
                break
        else:
            return False, ""  # Couldn't find available name
    
    # Create the backup branch
    success, _, stderr = run_git_command(project_path, ["git", "branch", branch_name])
    return success, branch_name if success else stderr


def sync_git_repository(project_path: Path) -> tuple[str, str, str]:
    """Sync a single git repository.
    
    Returns:
        tuple of (status, action_taken, details)
        status: 'success', 'no_change', 'requires_attention', 'fail'
    """
    project_name = project_path.name
    
    # Check if it's a git repository
    if not (project_path / ".git").exists():
        return "no_change", "skipped", "Not a git repository"
    
    print(f"  Syncing {project_name}...")
    
    # Factor 1: Check for local changes
    local_changes = has_local_changes(project_path)
    print(f"    Local changes: {'YES' if local_changes else 'NO'}")
    
    # Factor 2: Check for remote changes
    fetch_success, remote_changes = has_remote_changes(project_path)
    if not fetch_success:
        return "fail", "fetch_failed", "Could not fetch from remote"
    
    print(f"    Remote changes: {'YES' if remote_changes else 'NO'}")
    
    # Decision matrix implementation
    if not local_changes and not remote_changes:
        # ✅ CLEAN: No local changes, no remote changes
        return "success", "up_to_date", "Repository is up-to-date"
    
    elif not local_changes and remote_changes:
        # 🟢 SIMPLE PULL: No local changes, has remote changes
        # Create backup branch before pulling
        backup_success, backup_branch = create_backup_branch(project_path)
        if not backup_success:
            return "fail", "backup_failed", f"Could not create backup branch: {backup_branch}"
        
        print(f"    Created backup branch: {backup_branch}")
        
        # Pull changes
        pull_success, _, pull_error = run_git_command(project_path, ["git", "pull"])
        if not pull_success:
            return "fail", "pull_failed", f"Git pull failed: {pull_error}"
        
        return "success", "pulled", f"Pulled remote changes (backup: {backup_branch})"
    
    elif local_changes and not remote_changes:
        # 💾 LOCAL ONLY: Has local changes, no remote changes
        return "no_change", "local_only", "Local changes present, no remote updates"
    
    else:
        # 🔥 COMPLEX: Both local AND remote changes
        return "requires_attention", "complex_case", "Both local and remote changes - manual intervention required"


def is_git_repository(project_path: Path) -> bool:
    """Check if project is a git repository."""
    return (project_path / ".git").exists()


def main():
    """Synchronize git repositories across all discovered projects."""
    print("🎯 FINAL STATUS: Starting git sync across all projects")
    
    try:
        projects = get_local_projects()
        git_projects = [p for p in projects if is_git_repository(p.path)]
        
        print(f"Found {len(git_projects)} git repositories out of {len(projects)} total projects")
        
        if not git_projects:
            print("🎯 FINAL STATUS: success - No git repositories found")
            print("📝 FINAL NOTES: Scanned all projects, none are git repositories")
            return 0
        
        # Track statistics
        stats = {
            "success": 0,
            "no_change": 0, 
            "requires_attention": 0,
            "fail": 0
        }
        actions = {
            "up_to_date": 0,
            "pulled": 0,
            "local_only": 0,
            "complex_case": 0,
            "skipped": 0
        }
        
        for project in git_projects:
            status, action, details = sync_git_repository(project.path)
            stats[status] += 1
            actions[action] += 1
            
            # Log the result
            status_emoji = {
                "success": "✅",
                "no_change": "⚪", 
                "requires_attention": "⚠️",
                "fail": "❌"
            }
            print(f"  {status_emoji.get(status, '?')} {project.name}: {details}")
        
        # Determine final status
        if stats["fail"] > 0:
            final_status = "fail"
            status_desc = f"{stats['fail']} repositories failed"
        elif stats["requires_attention"] > 0:
            final_status = "requires_attention"
            status_desc = f"{stats['requires_attention']} repositories need manual intervention"
        elif stats["success"] > 0:
            final_status = "success" 
            status_desc = f"{stats['success']} repositories processed successfully"
        else:
            final_status = "no_change"
            status_desc = "All repositories up-to-date"
        
        print(f"🎯 FINAL STATUS: {final_status} - {status_desc}")
        
        # Detailed statistics in FINAL NOTES
        notes_parts = [f"Processed {len(git_projects)} git repositories"]
        if actions["pulled"] > 0:
            notes_parts.append(f"{actions['pulled']} pulled updates")
        if actions["local_only"] > 0:
            notes_parts.append(f"{actions['local_only']} with local changes")
        if actions["complex_case"] > 0:
            notes_parts.append(f"{actions['complex_case']} need manual merge")
        if stats["fail"] > 0:
            notes_parts.append(f"{stats['fail']} failed")
        
        print(f"📝 FINAL NOTES: {', '.join(notes_parts)}")
        return 0
        
    except Exception as e:
        print(f"🎯 FINAL STATUS: fail - Git sync failed: {e}")
        print("📝 FINAL NOTES: Check git installation and project discovery")
        return 1


if __name__ == "__main__":
    sys.exit(main())
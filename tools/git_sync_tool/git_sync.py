"""Git sync core functionality."""

import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import typer


@dataclass
class GitSyncResult:
    """Result of git sync operation."""
    project_name: str
    project_path: Path
    status: str  # 'success', 'no_change', 'requires_attention', 'fail'
    action: str  # 'up_to_date', 'pulled', 'local_only', 'complex_case', 'skipped'
    details: str
    backup_branch: Optional[str] = None


class GitSyncManager:
    """Manager for git synchronization operations."""
    
    def __init__(
        self,
        dry_run: bool = False,
        skip_backup: bool = False,
        backup_prefix: str = "daily-snapshots",
        timeout: int = 60,
        force_complex: bool = False,
        verbose: bool = True
    ):
        self.dry_run = dry_run
        self.skip_backup = skip_backup
        self.backup_prefix = backup_prefix
        self.timeout = timeout
        self.force_complex = force_complex
        self.verbose = verbose
    
    def run_git_command(self, project_path: Path, command: List[str]) -> Tuple[bool, str, str]:
        """Run a git command in a project directory.
        
        Args:
            project_path: Path to the project
            command: Git command as list (e.g., ['git', 'status', '--porcelain'])
            
        Returns:
            tuple of (success: bool, stdout: str, stderr: str)
        """
        if self.dry_run and command[1] in ['pull', 'branch', 'stash']:
            # For dry run, simulate success for write operations
            return True, f"[DRY RUN] Would execute: {' '.join(command)}", ""
        
        try:
            result = subprocess.run(
                command,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, "", f"Git command timed out after {self.timeout}s"
        except Exception as e:
            return False, "", f"Git command failed: {e}"
    
    def has_local_changes(self, project_path: Path) -> bool:
        """Check if project has uncommitted local changes."""
        success, stdout, _ = self.run_git_command(project_path, ["git", "status", "--porcelain"])
        return success and bool(stdout.strip())
    
    def has_remote_changes(self, project_path: Path) -> Tuple[bool, bool]:
        """Check if remote has changes to pull.
        
        Returns:
            tuple of (fetch_success: bool, has_changes: bool)
        """
        # First fetch to update remote refs
        if not self.dry_run:
            fetch_success, _, _ = self.run_git_command(project_path, ["git", "fetch"])
            if not fetch_success:
                return False, False
        else:
            fetch_success = True
        
        # Check if remote is ahead of local
        success, stdout, _ = self.run_git_command(project_path, ["git", "rev-list", "HEAD..origin/main", "--count"])
        if not success:
            # Try 'master' if 'main' doesn't exist
            success, stdout, _ = self.run_git_command(project_path, ["git", "rev-list", "HEAD..origin/master", "--count"])
        
        if success and stdout.isdigit():
            return True, int(stdout) > 0
        return True, False  # Assume no changes if we can't determine
    
    def create_backup_branch(self, project_path: Path) -> Tuple[bool, str]:
        """Create a backup branch with timestamp.
        
        Returns:
            tuple of (success: bool, branch_name: str)
        """
        if self.skip_backup:
            return True, "backup-skipped"
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        base_name = f"{self.backup_prefix}/{date_str}"
        
        # Check if base name exists
        success, _, _ = self.run_git_command(project_path, ["git", "rev-parse", "--verify", base_name])
        if not success:
            # Base name doesn't exist, use it
            branch_name = base_name
        else:
            # Find available name with suffix
            for i in range(1, 100):  # Limit to 100 attempts
                branch_name = f"{base_name}-{i}"
                success, _, _ = self.run_git_command(project_path, ["git", "rev-parse", "--verify", branch_name])
                if not success:
                    break
            else:
                return False, "Could not find available backup branch name"
        
        # Create the backup branch
        success, _, stderr = self.run_git_command(project_path, ["git", "branch", branch_name])
        return success, branch_name if success else stderr
    
    def sync_git_repository(self, project_path: Path) -> GitSyncResult:
        """Sync a single git repository.
        
        Returns:
            GitSyncResult with status and details
        """
        project_name = project_path.name
        
        # Check if it's a git repository
        if not self.is_git_repository(project_path):
            return GitSyncResult(
                project_name=project_name,
                project_path=project_path,
                status="no_change",
                action="skipped", 
                details="Not a git repository"
            )
        
        if self.verbose:
            if not self.dry_run:
                typer.echo(f"  Syncing {project_name}...")
            else:
                typer.echo(f"  [DRY RUN] Would sync {project_name}...")
        
        # Factor 1: Check for local changes
        local_changes = self.has_local_changes(project_path)
        if self.verbose:
            typer.echo(f"    Local changes: {'YES' if local_changes else 'NO'}")
        
        # Factor 2: Check for remote changes
        fetch_success, remote_changes = self.has_remote_changes(project_path)
        if not fetch_success:
            return GitSyncResult(
                project_name=project_name,
                project_path=project_path,
                status="fail",
                action="fetch_failed",
                details="Could not fetch from remote"
            )
        
        if self.verbose:
            typer.echo(f"    Remote changes: {'YES' if remote_changes else 'NO'}")
        
        # Decision matrix implementation
        if not local_changes and not remote_changes:
            # ✅ CLEAN: No local changes, no remote changes
            return GitSyncResult(
                project_name=project_name,
                project_path=project_path,
                status="success",
                action="up_to_date",
                details="Repository is up-to-date"
            )
        
        elif not local_changes and remote_changes:
            # 🟢 SIMPLE PULL: No local changes, has remote changes
            backup_branch = None
            
            if not self.skip_backup:
                # Create backup branch before pulling
                backup_success, backup_result = self.create_backup_branch(project_path)
                if not backup_success:
                    return GitSyncResult(
                        project_name=project_name,
                        project_path=project_path,
                        status="fail",
                        action="backup_failed",
                        details=f"Could not create backup branch: {backup_result}"
                    )
                backup_branch = backup_result
                if self.verbose:
                    typer.echo(f"    Created backup branch: {backup_branch}")
            
            # Pull changes
            pull_success, _, pull_error = self.run_git_command(project_path, ["git", "pull"])
            if not pull_success:
                return GitSyncResult(
                    project_name=project_name,
                    project_path=project_path,
                    status="fail",
                    action="pull_failed", 
                    details=f"Git pull failed: {pull_error}",
                    backup_branch=backup_branch
                )
            
            details = "Pulled remote changes"
            if backup_branch and backup_branch != "backup-skipped":
                details += f" (backup: {backup_branch})"
            
            return GitSyncResult(
                project_name=project_name,
                project_path=project_path,
                status="success",
                action="pulled",
                details=details,
                backup_branch=backup_branch
            )
        
        elif local_changes and not remote_changes:
            # 💾 LOCAL ONLY: Has local changes, no remote changes
            return GitSyncResult(
                project_name=project_name,
                project_path=project_path,
                status="no_change",
                action="local_only",
                details="Local changes present, no remote updates"
            )
        
        else:
            # 🔥 COMPLEX: Both local AND remote changes
            if self.force_complex:
                # TODO: Implement complex stash-based flow
                return GitSyncResult(
                    project_name=project_name,
                    project_path=project_path,
                    status="requires_attention",
                    action="complex_case",
                    details="Complex merge flow not yet implemented"
                )
            else:
                return GitSyncResult(
                    project_name=project_name,
                    project_path=project_path,
                    status="requires_attention",
                    action="complex_case",
                    details="Both local and remote changes - manual intervention required"
                )
    
    def sync_all_repositories(self, project_paths: List[Path]) -> List[GitSyncResult]:
        """Sync multiple git repositories.
        
        Args:
            project_paths: List of paths to sync
            
        Returns:
            List of GitSyncResult objects
        """
        results = []
        
        # Filter out archived projects (post-filtration)
        active_paths = []
        archived_count = 0
        
        for project_path in project_paths:
            if "/archive/" in str(project_path) or str(project_path).endswith("/archive"):
                archived_count += 1
                continue
            active_paths.append(project_path)
        
        if archived_count > 0 and self.verbose:
            typer.echo(f"Skipping {archived_count} archived repositories")
        
        for project_path in active_paths:
            result = self.sync_git_repository(project_path)
            results.append(result)
            
            # Log the result - always show requires_attention and fail, only show others if verbose
            status_emoji = {
                "success": "✅",
                "no_change": "⚪",
                "requires_attention": "⚠️",
                "fail": "❌"
            }
            
            should_show = (self.verbose or 
                          result.status in ["requires_attention", "fail"] or
                          result.action == "pulled")  # Always show successful pulls
            
            if should_show:
                typer.echo(f"  {status_emoji.get(result.status, '?')} {result.project_name}: {result.details}")
        
        return results
    
    def print_summary(self, results: List[GitSyncResult]) -> None:
        """Print summary of sync results."""
        # Track statistics
        stats = {"success": 0, "no_change": 0, "requires_attention": 0, "fail": 0}
        actions = {"up_to_date": 0, "pulled": 0, "local_only": 0, "complex_case": 0, "skipped": 0}
        
        for result in results:
            stats[result.status] += 1
            actions[result.action] += 1
        
        # Print summary
        typer.echo("\n" + "="*60)
        typer.echo("GIT SYNC SUMMARY")
        typer.echo("="*60)
        
        for status, count in stats.items():
            if count > 0:
                status_emoji = {"success": "✅", "no_change": "⚪", "requires_attention": "⚠️", "fail": "❌"}
                typer.echo(f"{status_emoji.get(status, '?')} {status.replace('_', ' ').title()}: {count}")
        
        typer.echo(f"\nTotal repositories processed: {len(results)}")
        
        if actions["pulled"] > 0:
            typer.echo(f"Repositories updated: {actions['pulled']}")
        if actions["complex_case"] > 0:
            typer.echo(f"⚠️  Repositories needing manual intervention: {actions['complex_case']}")
        if stats["fail"] > 0:
            typer.echo(f"❌ Failed repositories: {stats['fail']}")
    
    def is_git_repository(self, project_path: Path) -> bool:
        """Check if project is a git repository."""
        return (project_path / ".git").exists()
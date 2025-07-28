#!/usr/bin/env python3
"""Git sync tool - synchronize git repositories with remote origins."""

import typer
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated

from tools.git_sync_tool.git_sync import GitSyncManager
from src.lib.coding_projects import get_local_projects

app = typer.Typer(help="Git sync tool - synchronize repositories with remotes")


@app.command("sync-all")
def sync_all_repositories(
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Show what would be done without executing")] = False,
    skip_backup: Annotated[bool, typer.Option("--skip-backup", help="Skip creating backup branches")] = False,
    backup_prefix: Annotated[str, typer.Option("--backup-prefix", help="Custom backup branch prefix")] = "daily-snapshots",
    timeout: Annotated[int, typer.Option("--timeout", help="Git command timeout in seconds")] = 60,
    force_complex: Annotated[bool, typer.Option("--force-complex", help="Attempt complex merge flow (experimental)")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Show detailed output for all repositories")] = False,
):
    """Synchronize all git repositories with their remotes."""
    
    manager = GitSyncManager(
        dry_run=dry_run,
        skip_backup=skip_backup, 
        backup_prefix=backup_prefix,
        timeout=timeout,
        force_complex=force_complex,
        verbose=verbose
    )
    
    projects = get_local_projects()
    git_projects = [p for p in projects if manager.is_git_repository(p.path)]
    
    if dry_run:
        typer.echo("🔍 DRY RUN MODE - No changes will be made")
    
    typer.echo(f"Found {len(git_projects)} git repositories out of {len(projects)} total projects")
    
    if not git_projects:
        typer.echo("No git repositories found")
        return
    
    results = manager.sync_all_repositories([p.path for p in git_projects])
    
    # Print summary
    manager.print_summary(results)


@app.command("sync")  
def sync_single_repository(
    path: Annotated[Path, typer.Argument(help="Path to git repository")],
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Show what would be done without executing")] = False,
    skip_backup: Annotated[bool, typer.Option("--skip-backup", help="Skip creating backup branches")] = False,
    backup_prefix: Annotated[str, typer.Option("--backup-prefix", help="Custom backup branch prefix")] = "daily-snapshots",
    timeout: Annotated[int, typer.Option("--timeout", help="Git command timeout in seconds")] = 60,
):
    """Synchronize a single git repository with its remote."""
    
    if not path.exists():
        typer.echo(f"Error: Path {path} does not exist", err=True)
        raise typer.Exit(1)
    
    manager = GitSyncManager(
        dry_run=dry_run,
        skip_backup=skip_backup,
        backup_prefix=backup_prefix, 
        timeout=timeout
    )
    
    if not manager.is_git_repository(path):
        typer.echo(f"Error: {path} is not a git repository", err=True)
        raise typer.Exit(1)
    
    if dry_run:
        typer.echo("🔍 DRY RUN MODE - No changes will be made")
    
    result = manager.sync_git_repository(path)
    
    # Print result
    status_emoji = {
        "success": "✅",
        "no_change": "⚪",
        "requires_attention": "⚠️", 
        "fail": "❌"
    }
    
    typer.echo(f"{status_emoji.get(result.status, '?')} {path.name}: {result.details}")


if __name__ == "__main__":
    app()
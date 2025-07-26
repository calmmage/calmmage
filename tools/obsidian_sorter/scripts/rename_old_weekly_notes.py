#!/usr/bin/env python3
"""Rename old weekly notes to include year prefix to avoid search collisions."""

import re  
from pathlib import Path
from typing import List

from rich.console import Console
from rich.table import Table

console = Console()

def find_old_weekly_notes(vault_path: Path) -> List[tuple]:
    """Find weekly notes that should be renamed with year prefix."""
    weekly_folder = vault_path / "weekly_workspaces"
    rename_candidates = []
    
    if not weekly_folder.exists():
        return rename_candidates
    
    # Pattern: "Week N - DD MMM YYYY.md"
    weekly_pattern = r"^Week (\d+) - (\d{1,2} [A-Za-z]{3} (\d{4}))\.md$"
    
    # Scan all weekly files (including in archive folders)
    for weekly_file in weekly_folder.rglob("*.md"):
        match = re.match(weekly_pattern, weekly_file.name)
        if match:
            week_num = match.group(1)
            full_date = match.group(2)
            year = match.group(3)
            
            # Only rename files from previous years (not current year 2025)
            if int(year) < 2025:
                new_name = f"Week {year}-{week_num} - {full_date}.md"
                rename_candidates.append((weekly_file, new_name))
    
    return rename_candidates


def rename_weekly_files(rename_candidates: List[tuple], dry_run: bool = True) -> None:
    """Rename the weekly files with year prefix."""
    if dry_run:
        console.print("[yellow]DRY RUN MODE - No files will be renamed[/yellow]")
    
    success_count = 0
    for old_path, new_name in rename_candidates:
        new_path = old_path.parent / new_name
        
        try:
            if not dry_run:
                old_path.rename(new_path)
            
            console.print(f"[green]✓[/green] {old_path.name} → {new_name}")
            success_count += 1
            
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to rename {old_path.name}: {e}")
    
    if not dry_run:
        console.print(f"\n[bold green]✅ Renamed {success_count} weekly notes[/bold green]")
    else:
        console.print(f"\n[bold blue]📋 Would rename {success_count} weekly notes[/bold blue]")


def main():
    vault_path = Path("/Users/petrlavrov/work/projects/taskzilla-cm/main/root")
    
    console.print("[bold blue]🔄 WEEKLY NOTES COLLISION FIX[/bold blue]")
    console.print(f"Scanning: {vault_path / 'weekly_workspaces'}")
    
    # Find old weekly notes 
    rename_candidates = find_old_weekly_notes(vault_path)
    
    if not rename_candidates:
        console.print("[green]✅ No old weekly notes found to rename![/green]")
        return
    
    # Show what will be renamed
    table = Table(title="Weekly Notes to Rename")
    table.add_column("Current Name", style="red")
    table.add_column("New Name", style="green")
    table.add_column("Location", style="dim")
    
    for old_path, new_name in rename_candidates:
        relative_location = old_path.parent.relative_to(vault_path)
        table.add_row(old_path.name, new_name, str(relative_location))
    
    console.print(table)
    
    # Confirm and execute
    import typer
    if typer.confirm(f"\nRename {len(rename_candidates)} weekly notes to avoid search collisions?"):
        rename_weekly_files(rename_candidates, dry_run=False)
    else:
        console.print("Operation cancelled.")


if __name__ == "__main__":
    main()
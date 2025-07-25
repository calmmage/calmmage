#!/usr/bin/env python3
"""Simple daily notes analyzer - step by step approach."""

import re
import shutil
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import typer
from rich.console import Console
from rich.table import Table

from tools.obsidian_sorter.config import ObsidianSorterConfig

console = Console()

app = typer.Typer()


def is_daily_standard(filename: str) -> bool:
    """Check DD MMM YYYY format."""
    return bool(re.match(r'^\d{1,2} [A-Za-z]{3} \d{4}\.md$', filename))


def is_daily_alternative(filename: str) -> str:
    """Check alternative formats, return type or None."""
    patterns = {
        'dashes_dmy': r'^\d{1,2}-[A-Za-z]{3}-\d{4}\.md$',
        'underscores_dmy': r'^\d{1,2}_[A-Za-z]{3}_\d{4}\.md$',
        'spaces_long': r'^\d{1,2} [A-Za-z]{4,} \d{4}\.md$',
    }
    
    for fmt, pattern in patterns.items():
        if re.match(pattern, filename, re.IGNORECASE):
            return fmt
    return None


def get_planned_actions(config: ObsidianSorterConfig) -> List[Dict]:
    """Get all planned file actions."""
    actions = []
    daily_folder = config.obsidian_root / "daily"
    non_daily_target = config.obsidian_root / config.non_daily_target
    
    # Scan all files
    all_files = list(config.obsidian_root.rglob("*.md"))
    
    for file in all_files:
        is_daily = is_daily_standard(file.name) or is_daily_alternative(file.name)
        current_location = file.parent
        
        # Determine action
        if is_daily and current_location != daily_folder:
            # Daily note not in daily folder - move to daily
            actions.append({
                "file": file,
                "action": "move_to_daily",
                "from": current_location,
                "to": daily_folder
            })
        elif not is_daily and current_location == daily_folder:
            # Non-daily note in daily folder - move out
            actions.append({
                "file": file,
                "action": "move_from_daily", 
                "from": current_location,
                "to": non_daily_target
            })
    
    return actions


def create_daily_note_link(config: ObsidianSorterConfig, file_path: Path) -> bool:
    """Add link to daily note based on file's edit date."""
    try:
        # Get file modification time
        mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
        
        # Generate daily note filename (DD MMM YYYY format)
        daily_name = mod_time.strftime("%d %b %Y") + ".md"
        daily_path = config.obsidian_root / "daily" / daily_name
        
        # Create daily note if it doesn't exist
        if not daily_path.exists():
            daily_path.parent.mkdir(parents=True, exist_ok=True)
            daily_path.write_text(f"# {mod_time.strftime('%d %b %Y')}\n\n## Auto Links\n\n- [[{file_path.stem}]]\n")
            return True
        
        # Add link to existing daily note
        content = daily_path.read_text()
        link = f"- [[{file_path.stem}]]"
        
        if "## Auto Links" in content:
            # Add to existing Auto Links section
            if link not in content:
                content = content.replace("## Auto Links", f"## Auto Links\n\n{link}")
        else:
            # Create Auto Links section
            content += f"\n\n## Auto Links\n\n{link}\n"
        
        daily_path.write_text(content)
        return True
        
    except Exception as e:
        console.print(f"[red]Error linking {file_path.name}: {e}[/red]")
        return False


def execute_actions(actions: List[Dict], config: ObsidianSorterConfig, dry_run: bool = True) -> None:
    """Execute the planned actions."""
    if dry_run:
        console.print("[yellow]DRY RUN MODE - No files will be moved[/yellow]")
        return
    
    success_count = 0
    for action in actions:
        file = action["file"]
        target_dir = action["to"]
        
        try:
            # Create auto-link before moving (to preserve edit date)
            if action["action"] == "move_from_daily":
                create_daily_note_link(config, file)
            
            # Create target directory
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Move file
            new_path = target_dir / file.name
            if new_path.exists():
                console.print(f"[yellow]Skipping {file.name} - target exists[/yellow]")
                continue
                
            shutil.move(str(file), str(new_path))
            success_count += 1
            
        except Exception as e:
            console.print(f"[red]Error moving {file.name}: {e}[/red]")
    
    console.print(f"[green]Successfully moved {success_count} files[/green]")


@app.command()
def cleanup_daily(
    config_path: Path = typer.Option("config.yaml", help="Config file"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show planned actions without executing"
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Execute without confirmation"),
):
    """Clean up daily folder - move daily notes IN, non-daily OUT."""
    
    # Load config
    try:
        config = ObsidianSorterConfig.parse_file(config_path)
    except:
        config = ObsidianSorterConfig()
    
    console.print("[bold blue]🗂️  CLEANUP DAILY FOLDER[/bold blue]")
    
    # Show current analysis
    all_files = list(config.obsidian_root.rglob("*.md"))
    daily_standard = [f for f in all_files if is_daily_standard(f.name)]
    
    alternatives = []
    for file in all_files:
        alt_type = is_daily_alternative(file.name)
        if alt_type:
            alternatives.append((file, alt_type))
    
    console.print(f"📁 Vault: {config.obsidian_root}")
    console.print(f"📄 Total: {len(all_files)}")
    console.print(f"📅 Daily: {len(daily_standard) + len(alternatives)}")
    console.print(f"✅ Standard: {len(daily_standard)}")
    
    if alternatives:
        console.print("\n🔄 Non-standard to rename:")
        for file, fmt in alternatives:
            rel_path = file.relative_to(config.obsidian_root)
            console.print(f"  {file.name} (in {rel_path.parent})")
    
    # Get planned actions
    actions = get_planned_actions(config)
    
    if not actions:
        console.print("\n[green]No files need organizing![/green]")
        return
    
    # Show planned actions in table
    console.print()  # Add spacing
    table = Table(title="Planned Actions")
    table.add_column("File Name", style="cyan")
    table.add_column("Action", style="yellow") 
    table.add_column("From", style="red")
    table.add_column("To", style="green")
    
    for action in actions:
        file = action["file"]
        action_text = "→ daily/" if action["action"] == "move_to_daily" else "← from daily/"
        from_path = action["from"].relative_to(config.obsidian_root)
        to_path = action["to"].relative_to(config.obsidian_root)
        
        table.add_row(file.name, action_text, str(from_path), str(to_path))
    
    console.print(table)
    console.print(f"\nTotal actions: {len(actions)}")
    
    # Handle execution based on flags
    if dry_run:
        console.print("\n[yellow]DRY RUN MODE - No files will be moved[/yellow]")
        return
    
    # Default behavior: ASK for confirmation
    if not yes:
        if not typer.confirm("\nProceed with these changes?"):
            console.print("Operation cancelled.")
            return
    
    # Execute actions
    execute_actions(actions, config, dry_run=False)


@app.command()
def auto_link(
    config_path: Path = typer.Option("config.yaml", help="Config file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show planned actions without executing"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Execute without confirmation")
):
    """Auto-link files to daily notes based on edit dates."""
    
    # Load config
    try:
        config = ObsidianSorterConfig.parse_file(config_path)
    except:
        config = ObsidianSorterConfig()
    
    console.print("[bold blue]🔗 AUTO-LINK TO DAILY NOTES[/bold blue]")
    console.print("📝 TODO: Implement auto-linking logic")
    console.print("   - Scan files for edit dates")
    console.print("   - Find/create corresponding daily notes")
    console.print("   - Add [[filename]] links to '## Auto Links' section")
    
    if dry_run:
        console.print("\n[yellow]DRY RUN MODE - No links will be created[/yellow]")
        return
    
    if not yes:
        if not typer.confirm("\nProceed with auto-linking? (Currently does nothing)"):
            console.print("Operation cancelled.")
            return
    
    console.print("[green]Auto-linking placeholder completed![/green]")


@app.command()
def run_all(
    config_path: Path = typer.Option("config.yaml", help="Config file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show planned actions without executing"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Execute without confirmation")
):
    """Run all daily note operations: cleanup + auto-linking."""
    
    console.print("[bold green]🚀 RUNNING ALL DAILY NOTE OPERATIONS[/bold green]")
    console.print()
    
    # Run cleanup daily first
    console.print("[bold]Step 1: Cleanup Daily Folder[/bold]")
    cleanup_daily(config_path, dry_run, yes)
    
    console.print("\n" + "="*50)
    console.print()
    
    # Run auto-linking second
    console.print("[bold]Step 2: Auto-Link Files[/bold]")
    auto_link(config_path, dry_run, yes)
    
    console.print("\n[bold green]✅ All operations completed![/bold green]")


if __name__ == "__main__":
    app()
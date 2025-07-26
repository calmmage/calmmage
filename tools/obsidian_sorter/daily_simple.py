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


def create_daily_note_link(
    config: ObsidianSorterConfig, file_path: Path, target_date: str = None
) -> bool:
    """Add link to daily note based on specified date or file's edit date."""
    try:
        if target_date:
            # Use provided target date (from filename or user choice)
            daily_name = target_date + ".md"
        else:
            # Fall back to file modification time
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            daily_name = mod_time.strftime("%d %b %Y") + ".md"
        
        daily_path = config.obsidian_root / "daily" / daily_name
        
        # Create daily note if it doesn't exist
        if not daily_path.exists():
            daily_path.parent.mkdir(parents=True, exist_ok=True)
            # Extract date for header from filename
            header_date = daily_name.replace(".md", "")
            daily_path.write_text(f"# {header_date}\n\n## Auto Links\n\n- [[{file_path.stem}]]\n")
            return True
        
        # Add link to existing daily note
        content = daily_path.read_text()
        link = f"- [[{file_path.stem}]]"
        
        # Skip if link already exists
        if link in content:
            return True
            
        if "## Auto Links" in content:
            # Find the Auto Links section and add after it
            lines = content.split('\n')
            auto_links_idx = None
            for i, line in enumerate(lines):
                if line.strip() == "## Auto Links":
                    auto_links_idx = i
                    break
            
            if auto_links_idx is not None:
                # Insert after Auto Links header, preserving existing links
                insert_idx = auto_links_idx + 1
                # Skip empty lines after header
                while insert_idx < len(lines) and lines[insert_idx].strip() == "":
                    insert_idx += 1
                lines.insert(insert_idx, link)
                content = '\n'.join(lines)
        else:
            # Create Auto Links section at the end
            if not content.endswith('\n'):
                content += '\n'
            content += f"\n## Auto Links\n\n{link}\n"
        
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
                create_daily_note_link(config, file, target_date=None)
            
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


def extract_date_from_filename(filename: str) -> str:
    """Extract date from filename patterns."""
    # Common patterns: "Meeting - 25 Jul 2025", "2025-07-25 Notes", etc.
    date_patterns = [
        r'(\d{1,2} [A-Za-z]{3} \d{4})',  # 25 Jul 2025
        r'(\d{4}-\d{1,2}-\d{1,2})',     # 2025-07-25
        r'(\d{1,2}-[A-Za-z]{3}-\d{4})', # 25-Jul-2025
        r'(\d{1,2}/\d{1,2}/\d{4})',     # 25/07/2025
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def get_auto_link_candidates(config: ObsidianSorterConfig) -> List[Dict]:
    """Get files that need auto-linking (all non-daily files)."""
    candidates = []
    all_files = list(config.obsidian_root.rglob("*.md"))
    
    for file in all_files:
        # Skip daily files
        if is_daily_standard(file.name) or is_daily_alternative(file.name):
            continue
            
        # Get file dates
        stat = file.stat()
        edit_date = datetime.fromtimestamp(stat.st_mtime)
        creation_date = datetime.fromtimestamp(stat.st_ctime)
        
        # Calculate date difference
        date_diff = abs((edit_date - creation_date).days)
        
        # Extract date from filename
        filename_date = extract_date_from_filename(file.name)
        
        candidates.append({
            "file": file,
            "edit_date": edit_date,
            "creation_date": creation_date,
            "date_diff": date_diff,
            "filename_date": filename_date,
            "suggested_date": filename_date or edit_date.strftime("%d %b %Y")
        })
    
    return candidates


@app.command()
def auto_link(
    config_path: Path = typer.Option("config.yaml", help="Config file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show planned actions without executing"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Execute without confirmation"),
    skip_date_conflicts: bool = typer.Option(False, "--skip-date-conflicts", help="Auto-decline files with large date differences")
):
    """Auto-link files to daily notes based on edit/creation dates and filename patterns."""
    
    # Load config
    try:
        config = ObsidianSorterConfig.parse_file(config_path)
    except:
        config = ObsidianSorterConfig()
    
    console.print("[bold blue]🔗 AUTO-LINK TO DAILY NOTES[/bold blue]")
    
    # Get candidates
    candidates = get_auto_link_candidates(config)
    
    if not candidates:
        console.print("[green]No files need auto-linking![/green]")
        return
    
    # Categorize by date difference
    auto_proceed = []    # 0-3 days
    batch_confirm = []   # 3-20 days  
    individual_confirm = []  # >20 days
    
    for candidate in candidates:
        diff = candidate["date_diff"]
        if diff <= 3:
            auto_proceed.append(candidate)
        elif diff <= 20:
            batch_confirm.append(candidate)
        else:
            individual_confirm.append(candidate)
    
    # Show analysis
    console.print(f"📄 Total files to process: {len(candidates)}")
    console.print(f"✅ Auto-proceed (≤3 days diff): {len(auto_proceed)}")
    console.print(f"⚠️  Batch confirm (3-20 days diff): {len(batch_confirm)}")
    console.print(f"🔍 Individual confirm (>20 days diff): {len(individual_confirm)}")
    
    # Show sample files in table
    if candidates:
        table = Table(title="Auto-Link Candidates (Sample)")
        table.add_column("File", style="cyan")
        table.add_column("Date Source", style="yellow")
        table.add_column("Target Date", style="green")
        table.add_column("Date Diff", style="red")
        
        # Show first 5 from each category
        sample_files = auto_proceed[:2] + batch_confirm[:2] + individual_confirm[:1]
        for candidate in sample_files:
            source = "filename" if candidate["filename_date"] else "edit_date"
            diff_text = f"{candidate['date_diff']}d"
            
            table.add_row(
                candidate["file"].name,
                source,
                candidate["suggested_date"],
                diff_text
            )
        
        console.print(table)
    
    if dry_run:
        console.print("\n[yellow]DRY RUN MODE - No links will be created[/yellow]")
        return
    
    # Handle confirmations based on user requirements
    files_to_process = []
    
    # Auto-proceed files (0-3 days)
    files_to_process.extend(auto_proceed)
    
    # Batch confirmation (3-20 days)
    if batch_confirm and not skip_date_conflicts:
        if not yes:
            console.print(f"\n⚠️  {len(batch_confirm)} files have 3-20 day differences between edit/creation dates.")
            if typer.confirm("Process these files with batch confirmation?"):
                files_to_process.extend(batch_confirm)
        else:
            files_to_process.extend(batch_confirm)
    
    # Individual confirmation (>20 days) - TODO: implement individual asking
    if individual_confirm and not skip_date_conflicts:
        console.print(f"\n🔍 {len(individual_confirm)} files have >20 day differences.")
        console.print("TODO: Implement individual file confirmation")
    
    if not files_to_process:
        console.print("[yellow]No files selected for processing.[/yellow]")
        return
    
    # Final confirmation
    if not yes and not skip_date_conflicts:
        if not typer.confirm(f"\nProceed with auto-linking {len(files_to_process)} files?"):
            console.print("Operation cancelled.")
            return
    
    # Execute auto-linking
    success_count = 0
    failed_count = 0
    
    console.print(f"\n[bold blue]🔗 Processing {len(files_to_process)} files...[/bold blue]")
    
    for candidate in files_to_process:
        file_path = candidate["file"]
        target_date = candidate["suggested_date"]
        
        try:
            if create_daily_note_link(config, file_path, target_date):
                success_count += 1
                console.print(f"[green]✓[/green] Linked {file_path.name} → {target_date}")
            else:
                failed_count += 1
                console.print(f"[red]✗[/red] Failed to link {file_path.name}")
                
        except Exception as e:
            failed_count += 1
            console.print(f"[red]✗[/red] Error linking {file_path.name}: {e}")
    
    # Summary
    console.print(f"\n[bold green]✅ Auto-linking completed![/bold green]")
    console.print(f"[green]Successfully linked: {success_count} files[/green]")
    if failed_count > 0:
        console.print(f"[red]Failed: {failed_count} files[/red]")


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
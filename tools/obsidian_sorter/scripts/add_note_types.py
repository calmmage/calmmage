#!/usr/bin/env python3
"""Add type fields to daily and weekly notes that are missing them."""

import yaml
from pathlib import Path
from typing import Dict

from rich.console import Console
from rich.table import Table

from tools.obsidian_sorter.daily_simple import is_daily_standard, is_weekly_standard

console = Console()

def add_type_to_note(file_path: Path, note_type: str, dry_run: bool = True) -> bool:
    """Add type field to a note file."""
    try:
        content = file_path.read_text()
        
        if content.startswith("---"):
            # Has existing frontmatter
            end_marker = content.find("---", 3)
            if end_marker > 0:
                yaml_content = content[3:end_marker].strip()
                rest_content = content[end_marker + 3:]
                
                # Parse and update YAML
                metadata = yaml.safe_load(yaml_content) or {}
                if "type" in metadata:
                    # Already has type field
                    return True
                
                metadata["type"] = note_type
                
                # Reconstruct content
                new_yaml = yaml.dump(metadata, default_flow_style=False).strip()
                new_content = f"---\n{new_yaml}\n---{rest_content}"
            else:
                # Malformed frontmatter, create new
                frontmatter = f"---\ntype: {note_type}\n---\n"
                new_content = frontmatter + content
        else:
            # No frontmatter, create new
            frontmatter = f"---\ntype: {note_type}\n---\n"
            new_content = frontmatter + content
        
        if not dry_run:
            file_path.write_text(new_content)
        
        return True
        
    except Exception as e:
        console.print(f"[red]Error updating {file_path.name}: {e}[/red]")
        return False


def analyze_notes(vault_path: Path) -> Dict:
    """Analyze daily and weekly notes for missing type fields."""
    results = {
        "daily_needs_type": [],
        "weekly_needs_type": [],
        "daily_has_type": 0,
        "weekly_has_type": 0,
        "errors": []
    }
    
    all_files = list(vault_path.rglob("*.md"))
    
    for md_file in all_files:
        try:
            is_daily = is_daily_standard(md_file.name)
            is_weekly = is_weekly_standard(md_file.name)
            
            if not (is_daily or is_weekly):
                continue
            
            # Check if file has type field
            content = md_file.read_text()
            has_type = False
            
            if content.startswith("---"):
                end_marker = content.find("---", 3)
                if end_marker > 0:
                    yaml_content = content[3:end_marker].strip()
                    metadata = yaml.safe_load(yaml_content)
                    if isinstance(metadata, dict) and "type" in metadata:
                        has_type = True
            
            if is_daily:
                if has_type:
                    results["daily_has_type"] += 1
                else:
                    results["daily_needs_type"].append(md_file)
            elif is_weekly:
                if has_type:
                    results["weekly_has_type"] += 1
                else:
                    results["weekly_needs_type"].append(md_file)
                    
        except Exception as e:
            results["errors"].append({
                "file": md_file,
                "error": str(e)
            })
    
    return results


def main():
    vault_path = Path("/Users/petrlavrov/work/projects/taskzilla-cm/main/root")
    
    console.print("[bold blue]📝 NOTE TYPE FIELD INSERTION[/bold blue]")
    console.print(f"Analyzing notes in: {vault_path}")
    
    # Analyze notes
    results = analyze_notes(vault_path)
    
    if results["errors"]:
        console.print(f"[red]⚠️  {len(results['errors'])} files had errors[/red]")
    
    # Show current status
    console.print(f"\n📄 Daily notes with type field: {results['daily_has_type']}")
    console.print(f"📄 Daily notes missing type field: {len(results['daily_needs_type'])}")
    console.print(f"📅 Weekly notes with type field: {results['weekly_has_type']}")
    console.print(f"📅 Weekly notes missing type field: {len(results['weekly_needs_type'])}")
    
    total_to_update = len(results['daily_needs_type']) + len(results['weekly_needs_type'])
    
    if total_to_update == 0:
        console.print("\n[green]✅ All daily and weekly notes already have type fields![/green]")
        return
    
    # Show sample files
    if results['daily_needs_type'] or results['weekly_needs_type']:
        table = Table(title="Notes Missing Type Fields (Sample)")
        table.add_column("Note", style="cyan")
        table.add_column("Type to Add", style="green")
        table.add_column("Location", style="dim")
        
        # Show first 5 from each category
        sample_daily = results['daily_needs_type'][:5]
        sample_weekly = results['weekly_needs_type'][:5]
        
        for note in sample_daily:
            rel_path = note.relative_to(vault_path)
            table.add_row(note.name, "daily", str(rel_path.parent))
        
        for note in sample_weekly:
            rel_path = note.relative_to(vault_path)
            table.add_row(note.name, "weekly_note", str(rel_path.parent))
        
        remaining = total_to_update - len(sample_daily) - len(sample_weekly)
        if remaining > 0:
            table.add_row("...", "...", f"... and {remaining} more")
            
        console.print(table)
    
    # Ask for confirmation and execute
    import typer
    if typer.confirm(f"\nAdd type fields to {total_to_update} notes?", default=True):
        success_count = 0
        
        # Process daily notes
        for note in results['daily_needs_type']:
            if add_type_to_note(note, "daily", dry_run=False):
                console.print(f"[green]✓[/green] Added type: daily to {note.name}")
                success_count += 1
        
        # Process weekly notes
        for note in results['weekly_needs_type']:
            if add_type_to_note(note, "weekly_note", dry_run=False):
                console.print(f"[green]✓[/green] Added type: weekly_note to {note.name}")
                success_count += 1
        
        console.print(f"\n[bold green]✅ Updated {success_count} notes with type fields[/bold green]")
    else:
        console.print("Operation cancelled.")


if __name__ == "__main__":
    main()
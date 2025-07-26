#!/usr/bin/env python3
"""Fix case inconsistencies in YAML frontmatter type fields."""

import yaml
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.table import Table

console = Console()

def find_case_inconsistencies(vault_path: Path) -> Dict[str, List[Path]]:
    """Find files with case-inconsistent type values."""
    inconsistent_files = {}
    
    for md_file in vault_path.rglob("*.md"):
        try:
            content = md_file.read_text()
            if content.startswith("---"):
                end_marker = content.find("---", 3)
                if end_marker > 0:
                    yaml_content = content[3:end_marker].strip()
                    metadata = yaml.safe_load(yaml_content)
                    if isinstance(metadata, dict) and "type" in metadata:
                        type_value = metadata["type"]
                        # Check if it has uppercase letters (should be lowercase)
                        if isinstance(type_value, str) and type_value != type_value.lower():
                            if type_value not in inconsistent_files:
                                inconsistent_files[type_value] = []
                            inconsistent_files[type_value].append(md_file)
        except Exception:
            continue
    
    return inconsistent_files


def fix_case_inconsistency(file_path: Path, old_value: str, new_value: str) -> bool:
    """Fix case inconsistency in a single file."""
    try:
        content = file_path.read_text()
        if content.startswith("---"):
            end_marker = content.find("---", 3)
            if end_marker > 0:
                yaml_content = content[3:end_marker].strip()
                rest_content = content[end_marker + 3:]
                
                # Replace the type value
                new_yaml_content = yaml_content.replace(f"type: {old_value}", f"type: {new_value}")
                
                # Write back
                new_content = f"---\n{new_yaml_content}\n---{rest_content}"
                file_path.write_text(new_content)
                return True
    except Exception as e:
        console.print(f"[red]Error fixing {file_path.name}: {e}[/red]")
    
    return False


def main():
    vault_path = Path("/Users/petrlavrov/work/projects/taskzilla-cm/main/root")
    
    console.print("[bold blue]🔧 FIXING CASE INCONSISTENCIES[/bold blue]")
    console.print(f"Scanning vault: {vault_path}")
    
    # Find inconsistencies
    inconsistent_files = find_case_inconsistencies(vault_path)
    
    if not inconsistent_files:
        console.print("[green]✅ No case inconsistencies found![/green]")
        return
    
    # Show what we found
    table = Table(title="Case Inconsistencies Found")
    table.add_column("Current Value", style="red")
    table.add_column("Should Be", style="green")
    table.add_column("Files Count", style="yellow")
    
    for old_value, files in inconsistent_files.items():
        new_value = old_value.lower()
        table.add_row(f"type: {old_value}", f"type: {new_value}", str(len(files)))
    
    console.print(table)
    
    # Fix them
    console.print("\n[bold]Fixing inconsistencies...[/bold]")
    total_fixed = 0
    
    for old_value, files in inconsistent_files.items():
        new_value = old_value.lower()
        
        for file_path in files:
            if fix_case_inconsistency(file_path, old_value, new_value):
                console.print(f"[green]✓[/green] Fixed {file_path.name}: {old_value} → {new_value}")
                total_fixed += 1
            else:
                console.print(f"[red]✗[/red] Failed to fix {file_path.name}")
    
    console.print(f"\n[bold green]✅ Fixed {total_fixed} files[/bold green]")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Generic node type cleanup - organize all configured node types."""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
import typer
from rich.console import Console
from rich.table import Table

from tools.obsidian_sorter.config import ObsidianSorterConfig

console = Console()
app = typer.Typer()


def detect_file_node_type(file_path: Path, config: ObsidianSorterConfig) -> Optional[str]:
    """Detect node type for a file using filename patterns and frontmatter."""
    
    # First try filename pattern detection
    filename_type = config.detect_node_type_by_filename(file_path.name)
    if filename_type:
        return filename_type
    
    # Then try frontmatter detection
    try:
        content = file_path.read_text()
        if content.startswith("---"):
            end_marker = content.find("---", 3)
            if end_marker > 0:
                yaml_content = content[3:end_marker].strip()
                metadata = yaml.safe_load(yaml_content)
                if isinstance(metadata, dict) and "type" in metadata:
                    type_value = metadata["type"]
                    frontmatter_type = config.detect_node_type_by_frontmatter(type_value)
                    if frontmatter_type:
                        return frontmatter_type
    except Exception:
        pass
    
    return None


def get_generic_cleanup_actions(config: ObsidianSorterConfig) -> tuple[List[Dict], Dict[str, int]]:
    """Get all planned actions for generic node type cleanup."""
    actions = []
    stats = {"correctly_placed": 0, "needs_move": 0, "untyped": 0, "total_scanned": 0}
    inbox_path = config.obsidian_root / config.inbox_path
    
    # Scan all files in vault
    all_files = list(config.obsidian_root.rglob("*.md"))
    stats["total_scanned"] = len(all_files)
    stats["templates_skipped"] = 0
    stats["daily_weekly_skipped"] = 0
    
    for file in all_files:
        # Skip files already being processed by specific cleanups
        # (daily/weekly cleanup handles these separately)
        if file.parent.name in ["daily", "weekly_workspaces"]:
            stats["daily_weekly_skipped"] += 1
            continue
            
        # Skip template files - they should never be moved
        templates_path = config.obsidian_root / config.templates_path if config.templates_path else None
        if templates_path and (file.parent == templates_path or templates_path in file.parents):
            stats["templates_skipped"] += 1
            continue
        
            
        # Detect what type this file should be
        detected_type = detect_file_node_type(file, config)
        
        if detected_type:
            # File has a detected type
            target_path = config.get_node_type_path(detected_type)
            current_location = file.parent
            
            # Check if file needs to move
            if current_location != target_path:
                stats["needs_move"] += 1
                actions.append({
                    "file": file,
                    "action": "move_to_typed_folder",
                    "node_type": detected_type,
                    "from": current_location,
                    "to": target_path
                })
            else:
                stats["correctly_placed"] += 1
        else:
            # File has no detected type
            current_location = file.parent
            current_rel_path = str(current_location.relative_to(config.obsidian_root))
            
            # Check if current location is a configured node type folder (core folders to preserve)
            is_in_core_typed_folder = False
            for node_type in config.node_types.values():
                if current_rel_path == node_type.folder or current_rel_path.startswith(node_type.folder + "/"):
                    is_in_core_typed_folder = True
                    break
            
            if current_location == inbox_path:
                # File is untyped and already in inbox - correct
                stats["correctly_placed"] += 1
            elif is_in_core_typed_folder:
                # File is untyped but in a core typed folder - leave it there
                stats["correctly_placed"] += 1
            else:
                # File is untyped and in a non-core folder
                # Move the entire folder to inbox (preserving folder structure)
                folder_name = current_location.name
                target_folder_in_inbox = inbox_path / folder_name
                
                stats["untyped"] += 1
                actions.append({
                    "file": file,
                    "action": "move_folder_to_inbox",
                    "node_type": "untyped",
                    "from": current_location,
                    "to": target_folder_in_inbox,
                    "folder_name": folder_name
                })
    
    return actions, stats


@app.command()
def cleanup_all_types(
    config_path: Path = typer.Option("config.yaml", help="Config file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show planned actions without executing"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Execute without confirmation"),
):
    """Clean up all configured node types - organize files by type."""
    
    # Load config
    try:
        config = ObsidianSorterConfig.parse_file(config_path)
    except:
        config = ObsidianSorterConfig()
    
    console.print("[bold blue]🗂️  CLEANUP ALL NODE TYPES[/bold blue]")
    console.print(f"📁 Vault: {config.obsidian_root}")
    console.print(f"📝 templates path: {config.obsidian_root / config.templates_path if config.templates_path else 'None'}")
    
    # Show configured node types
    console.print(f"\n📋 Configured node types: {len(config.node_types)}")
    
    type_table = Table(title="Configured Node Types")
    type_table.add_column("Type", style="cyan")
    type_table.add_column("Target Folder", style="green")
    type_table.add_column("Detection", style="yellow")
    
    for type_name, node_type in config.node_types.items():
        detection_methods = []
        if node_type.pattern:
            detection_methods.append("filename")
        if node_type.frontmatter_type:
            detection_methods.append("frontmatter")
        
        detection_text = ", ".join(detection_methods) if detection_methods else "none"
        type_table.add_row(type_name, node_type.folder, detection_text)
    
    console.print(type_table)
    
    # Get planned actions
    actions, stats = get_generic_cleanup_actions(config)
    
    # Show statistics
    console.print("\n📊 Vault Analysis:")
    console.print(f"   Total files scanned: {stats['total_scanned']}")
    console.print(f"   Templates skipped: {stats['templates_skipped']}")
    console.print(f"   Daily/weekly skipped: {stats['daily_weekly_skipped']}")
    console.print(f"   Already in correct locations: {stats['correctly_placed']}")
    console.print(f"   Need to be moved: {stats['needs_move']}")
    console.print(f"   Untyped files (→ Inbox): {stats['untyped']}")
    
    if not actions:
        console.print("\n[green]✅ All files are already in correct locations![/green]")
        return
    
    # Show planned actions
    console.print(f"\n📄 Files needing organization: {len(actions)}")
    
    action_table = Table(title="Planned Actions")
    action_table.add_column("File", style="cyan")
    action_table.add_column("Action", style="yellow")
    action_table.add_column("Type", style="green") 
    action_table.add_column("From", style="red")
    action_table.add_column("To", style="green")
    
    # Show sample actions
    for action in actions[:10]:  # Show first 10
        file = action["file"]
        
        if action["action"] == "move_to_typed_folder":
            action_text = f"→ {action['node_type']} folder"
        elif action["action"] == "move_folder_to_inbox":
            action_text = f"→ inbox/{action['folder_name']} (folder move)"
        else:
            action_text = "→ inbox (untyped)"
        
        from_path = action["from"].relative_to(config.obsidian_root)
        to_path = action["to"].relative_to(config.obsidian_root)
        
        action_table.add_row(
            file.name,
            action_text,
            action["node_type"],
            str(from_path),
            str(to_path)
        )
    
    if len(actions) > 10:
        action_table.add_row("...", "...", "...", "...", f"... and {len(actions) - 10} more")
    
    console.print(action_table)
    
    if dry_run:
        console.print("\n[yellow]DRY RUN MODE - No files will be moved[/yellow]")
        return
    
    # Confirmation
    if not yes:
        if not typer.confirm(f"\nProceed with organizing {len(actions)} files?"):
            console.print("Operation cancelled.")
            return
    
    # Execute actions
    success_count = 0
    failed_count = 0
    moved_folders = set()  # Track folders we've already moved
    
    for action in actions:
        file_path = action["file"]
        target_dir = action["to"]
        
        try:
            if action["action"] == "move_folder_to_inbox":
                # Handle folder move
                source_folder = action["from"]
                folder_name = action["folder_name"]
                
                # Skip if we've already moved this folder
                if source_folder in moved_folders:
                    continue
                    
                # Move entire folder to inbox
                inbox_target = target_dir
                if inbox_target.exists():
                    console.print(f"[yellow]Skipping folder {folder_name} - target exists in inbox[/yellow]")
                    continue
                
                import shutil
                shutil.move(str(source_folder), str(inbox_target))
                moved_folders.add(source_folder)
                success_count += 1
                
                console.print(f"[green]✓[/green] Moved folder {folder_name} → inbox/{folder_name}")
                
            else:
                # Handle individual file move
                target_dir.mkdir(parents=True, exist_ok=True)
                
                new_path = target_dir / file_path.name
                if new_path.exists():
                    console.print(f"[yellow]Skipping {file_path.name} - target exists[/yellow]")
                    continue
                
                import shutil
                shutil.move(str(file_path), str(new_path))
                success_count += 1
                
                action_desc = f"→ {action['node_type']}" if action["action"] == "move_to_typed_folder" else "→ inbox"
                console.print(f"[green]✓[/green] Moved {file_path.name} {action_desc}")
            
        except Exception as e:
            failed_count += 1
            console.print(f"[red]✗[/red] Failed to move {file_path.name}: {e}")
    
    # Summary
    console.print("\n[bold green]✅ Generic cleanup completed![/bold green]")
    console.print(f"[green]Successfully moved: {success_count} files[/green]") 
    if failed_count > 0:
        console.print(f"[red]Failed: {failed_count} files[/red]")


if __name__ == "__main__":
    app()
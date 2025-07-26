#!/usr/bin/env python3
"""Obsidian Note Sorter CLI."""

import sys
from pathlib import Path
from typing import Optional
import yaml
import typer
from rich.console import Console
from rich.table import Table

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from .config import ObsidianSorterConfig, SortingRule
from .sorter import ObsidianSorter
from .detectors import auto_detect_note_types

app = typer.Typer(help="Obsidian Note Auto-Sorter")
console = Console()


def load_config(config_path: Optional[Path] = None) -> ObsidianSorterConfig:
    """Load configuration from file or create default."""
    if config_path and config_path.exists():
        with open(config_path) as f:
            config_data = yaml.safe_load(f)
        return ObsidianSorterConfig(**config_data)
    else:
        # Return default configuration
        return ObsidianSorterConfig()


def save_config(config: ObsidianSorterConfig, config_path: Path) -> None:
    """Save configuration to file."""
    config_data = config.model_dump()
    # Convert Path objects to strings for YAML serialization
    def convert_paths(obj):
        if isinstance(obj, dict):
            return {k: convert_paths(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_paths(item) for item in obj]
        elif isinstance(obj, Path):
            return str(obj)
        return obj
    
    config_data = convert_paths(config_data)
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)


@app.command()
def sort(
    config_file: Optional[Path] = typer.Option(None, "--config", "-c", help="Configuration file path"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Preview changes without moving files"),
    obsidian_root: Optional[Path] = typer.Option(None, "--root", "-r", help="Obsidian vault root path"),
) -> None:
    """Sort notes from inbox to appropriate folders."""
    
    # Load configuration
    config = load_config(config_file)
    
    # Override with command line options
    if obsidian_root:
        config.obsidian_root = obsidian_root
    if dry_run:
        config.dry_run = dry_run
    
    # Validate paths
    if not config.obsidian_root.exists():
        console.print(f"[red]❌ Obsidian root does not exist: {config.obsidian_root}[/red]")
        raise typer.Exit(1)
    
    if not config.full_inbox_path.exists():
        console.print(f"[red]❌ Inbox folder does not exist: {config.full_inbox_path}[/red]")
        raise typer.Exit(1)
    
    # Check if we have any rules
    if not config.rules:
        console.print("[yellow]⚠️  No sorting rules configured. Use 'config' command to set up rules.[/yellow]")
        return
    
    console.print(f"📁 Obsidian root: {config.obsidian_root}")
    console.print(f"📨 Inbox: {config.full_inbox_path}")
    console.print(f"📏 Rules: {len(config.rules)}")
    
    if dry_run:
        console.print("[yellow]🔍 DRY RUN MODE - No files will be moved[/yellow]")
    
    # Create sorter and run
    sorter = ObsidianSorter(config)
    results = sorter.sort_all()
    
    # Print results
    sorter.print_results()
    
    # Generate job runner output
    status, notes = sorter.generate_status_output()
    print(f"\n🎯 FINAL STATUS: {status}")
    print(f"📝 FINAL NOTES: {notes}")
    
    # Add rule breakdown details if successful
    if results and any(r.success for r in results):
        rule_counts = {}
        for result in results:
            if result.success and result.rule_name:
                rule_counts[result.rule_name] = rule_counts.get(result.rule_name, 0) + 1
        
        if rule_counts:
            rule_summary = ", ".join([f"{count} via '{rule}'" for rule, count in rule_counts.items()])
            print(f"📊 Rule breakdown: {rule_summary}")


@app.command()
def config(
    config_file: Optional[Path] = typer.Option(None, "--config", "-c", help="Configuration file path"),
    list_rules: bool = typer.Option(False, "--list", "-l", help="List current rules"),
    add_rule: bool = typer.Option(False, "--add", "-a", help="Add new rule interactively"),
    auto_detect: bool = typer.Option(False, "--auto-detect", help="Auto-detect note types and create rules"),
) -> None:
    """Manage sorting configuration."""
    
    config_path = config_file or Path("config.yaml")
    config = load_config(config_path if config_path.exists() else None)
    
    if list_rules:
        if not config.rules:
            console.print("[yellow]No rules configured[/yellow]")
            return
        
        table = Table(title="Sorting Rules")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="green")  
        table.add_column("Pattern", style="yellow")
        table.add_column("Target Folder", style="blue")
        table.add_column("Priority", justify="center")
        
        for rule in sorted(config.rules, key=lambda r: r.priority, reverse=True):
            table.add_row(
                rule.name,
                rule.detector_type,
                rule.pattern,
                str(rule.target_folder),
                str(rule.priority)
            )
        
        console.print(table)
        return
    
    if auto_detect:
        console.print("🔍 Auto-detecting note types...")
        note_types = auto_detect_note_types(config)
        
        if not note_types:
            console.print("[yellow]No note types detected[/yellow]")
            return
        
        console.print(f"Found note types: {', '.join(note_types)}")
        
        # Create basic rules for detected types
        for note_type in note_types:
            rule = SortingRule(
                name=f"Auto: {note_type}",
                detector_type="tag",
                pattern=note_type.lower(),
                target_folder=Path(note_type),
                priority=0
            )
            config.rules.append(rule)
        
        save_config(config, config_path)
        console.print(f"[green]✅ Created {len(note_types)} auto-detected rules[/green]")
        return
    
    if add_rule:
        console.print("📝 Creating new sorting rule...")
        
        name = typer.prompt("Rule name")
        detector_type = typer.prompt(
            "Detector type", 
            type=typer.Choice(['tag', 'template', 'content', 'filename'])
        )
        pattern = typer.prompt("Pattern to match")
        target_folder = typer.prompt("Target folder")
        priority = typer.prompt("Priority", default=0, type=int)
        
        rule = SortingRule(
            name=name,
            detector_type=detector_type,
            pattern=pattern,
            target_folder=Path(target_folder),
            priority=priority
        )
        
        config.rules.append(rule)
        save_config(config, config_path)
        console.print(f"[green]✅ Added rule '{name}'[/green]")
        return
    
    # Show current configuration
    console.print(f"📁 Obsidian root: {config.obsidian_root}")
    console.print(f"📨 Inbox: {config.full_inbox_path}")
    console.print(f"📏 Rules: {len(config.rules)}")
    console.print(f"🔧 Config file: {config_path}")


@app.command()
def test(
    note_path: Path = typer.Argument(help="Path to note file to test"),
    config_file: Optional[Path] = typer.Option(None, "--config", "-c", help="Configuration file path"),
) -> None:
    """Test sorting rules against a specific note."""
    
    if not note_path.exists():
        console.print(f"[red]❌ Note file does not exist: {note_path}[/red]")
        raise typer.Exit(1)
    
    config = load_config(config_file)
    sorter = ObsidianSorter(config)
    
    # Analyze the note
    content, frontmatter, _ = sorter.analyze_note(note_path)
    rule = sorter.find_matching_rule(note_path, content, frontmatter)
    
    console.print(f"📄 Testing note: {note_path.name}")
    console.print(f"📊 Frontmatter keys: {list(frontmatter.keys())}")
    
    if rule:
        target_path = config.get_target_path(rule) / note_path.name
        console.print(f"[green]✅ Matches rule: {rule.name}[/green]")
        console.print(f"📁 Would move to: {target_path}")
    else:
        console.print("[yellow]⚠️  No matching rule found[/yellow]")


if __name__ == "__main__":
    app()
#!/usr/bin/env python3
"""Note Types Discovery Script - Analyze entity types from 3 sources.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List
from collections import defaultdict, Counter

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def discover_template_types(vault_path: Path) -> Dict[str, str]:
    """Source 1: Extract entity types from template files."""
    templates_path = vault_path / "templates"
    template_types = {}
    
    if not templates_path.exists():
        console.print("[red]Templates folder not found[/red]")
        return template_types
    
    for template_file in templates_path.glob("*.md"):
        # Extract type from filename pattern
        filename = template_file.stem
        if filename.endswith("_template"):
            type_name = filename.replace("_template", "")
            template_types[filename] = type_name
        
        # Also check YAML frontmatter in template
        try:
            content = template_file.read_text()
            if content.startswith("---"):
                end_marker = content.find("---", 3)
                if end_marker > 0:
                    yaml_content = content[3:end_marker].strip()
                    metadata = yaml.safe_load(yaml_content)
                    if isinstance(metadata, dict) and "type" in metadata:
                        template_types[filename] = metadata["type"]
        except Exception as e:
            console.print(f"[yellow]Warning: Could not parse {template_file.name}: {e}[/yellow]")
    
    return template_types


def discover_yaml_types(vault_path: Path) -> Dict[str, int]:
    """Source 2: Find all 'type:' field values in YAML frontmatter."""
    type_counts = Counter()
    files_processed = 0
    
    for md_file in vault_path.rglob("*.md"):
        files_processed += 1
        try:
            content = md_file.read_text()
            if content.startswith("---"):
                end_marker = content.find("---", 3)
                if end_marker > 0:
                    yaml_content = content[3:end_marker].strip()
                    metadata = yaml.safe_load(yaml_content)
                    if isinstance(metadata, dict) and "type" in metadata:
                        type_value = metadata["type"]
                        type_counts[type_value] += 1
        except Exception:
            # Skip files with parsing issues
            continue
    
    console.print(f"[dim]Processed {files_processed} markdown files[/dim]")
    return dict(type_counts)


def discover_config_types() -> Dict[str, Dict]:
    """Source 3: Load entity types from YAML config (placeholder)."""
    # For now, return empty - this would be loaded from a config file
    # that the user would define with entity characteristics
    return {
        "daily": {
            "pattern": r"^\d{1,2} [A-Za-z]{3} \d{4}\.md$",
            "folder": "daily/",
            "auto_add_type": True
        },
        "weekly": {
            "pattern": r"^Week \d+ - \d{1,2} [A-Za-z]{3} \d{4}\.md$", 
            "folder": "weekly_workspaces/",
            "auto_add_type": True
        }
    }


def detect_file_types(vault_path: Path, config_types: Dict) -> Dict[str, List[Path]]:
    """Detect which files match which entity types."""
    detected_files = defaultdict(list)
    
    for md_file in vault_path.rglob("*.md"):
        filename = md_file.name
        
        # Check against config patterns
        for type_name, type_config in config_types.items():
            if "pattern" in type_config:
                pattern = type_config["pattern"]
                if re.match(pattern, filename):
                    detected_files[type_name].append(md_file)
                    break
    
    return dict(detected_files)


def main():
    vault_path = Path("/Users/petrlavrov/work/projects/taskzilla-cm/main/root")
    
    console.print(Panel.fit(
        "[bold blue]🔍 NOTE TYPES DISCOVERY[/bold blue]\n"
        f"Analyzing vault: {vault_path}",
        border_style="blue"
    ))
    
    # Source 1: Template analysis
    console.print("\n[bold]📁 Source 1: Template Types[/bold]")
    template_types = discover_template_types(vault_path)
    
    if template_types:
        table = Table(title="Template-Based Entity Types")
        table.add_column("Template File", style="cyan")
        table.add_column("Entity Type", style="green")
        
        for template_name, entity_type in template_types.items():
            table.add_row(template_name, entity_type)
        
        console.print(table)
    else:
        console.print("[red]No template types found[/red]")
    
    # Source 2: YAML frontmatter analysis
    console.print("\n[bold]🏷️  Source 2: YAML Frontmatter Types[/bold]")
    yaml_types = discover_yaml_types(vault_path)
    
    if yaml_types:
        table = Table(title="Existing YAML 'type:' Values")
        table.add_column("Type Value", style="cyan")
        table.add_column("Count", style="yellow")
        
        for type_value, count in sorted(yaml_types.items(), key=lambda x: x[1], reverse=True):
            table.add_row(type_value, str(count))
        
        console.print(table)
    else:
        console.print("[red]No YAML type fields found[/red]")
    
    # Source 3: Config definitions
    console.print("\n[bold]⚙️  Source 3: Config Entity Types[/bold]")
    config_types = discover_config_types()
    
    if config_types:
        table = Table(title="Config-Defined Entity Types")
        table.add_column("Entity Type", style="cyan")
        table.add_column("Pattern", style="green")
        table.add_column("Folder", style="yellow")
        
        for type_name, type_config in config_types.items():
            pattern = type_config.get("pattern", "N/A")
            folder = type_config.get("folder", "N/A")
            table.add_row(type_name, pattern, folder)
        
        console.print(table)
    
    # File detection analysis
    console.print("\n[bold]🎯 File Type Detection[/bold]")
    detected_files = detect_file_types(vault_path, config_types)
    
    if detected_files:
        table = Table(title="Files Detected by Type")
        table.add_column("Entity Type", style="cyan")
        table.add_column("Count", style="yellow")
        table.add_column("Sample Files", style="green")
        
        for type_name, files in detected_files.items():
            sample_files = [f.name for f in files[:3]]
            sample_text = ", ".join(sample_files)
            if len(files) > 3:
                sample_text += f" (+{len(files)-3} more)"
            
            table.add_row(type_name, str(len(files)), sample_text)
        
        console.print(table)
    
    # Summary
    console.print("\n[bold green]📊 DISCOVERY SUMMARY[/bold green]")
    console.print(f"Template types found: {len(template_types)}")
    console.print(f"YAML type values found: {len(yaml_types)}")
    console.print(f"Config types defined: {len(config_types)}")
    console.print(f"File types detected: {len(detected_files)}")


if __name__ == "__main__":
    main()
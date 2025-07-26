#!/usr/bin/env python3
"""Add type fields to templates that are missing them, using filename for type."""

import yaml
from pathlib import Path
from typing import Dict

from rich.console import Console
from rich.table import Table

console = Console()

def analyze_templates(vault_path: Path) -> Dict:
    """Analyze templates and identify which need type fields."""
    templates_path = vault_path / "templates"
    if not templates_path.exists():
        console.print(f"[red]Templates folder not found: {templates_path}[/red]")
        return {}
    
    results = {
        "has_type": [],
        "needs_type": [],
        "errors": []
    }
    
    for template_file in templates_path.glob("*.md"):
        filename = template_file.stem
        
        # Extract expected type from filename
        if filename.endswith("_template"):
            expected_type = filename.replace("_template", "")
        else:
            expected_type = filename
        
        try:
            content = template_file.read_text()
            
            # Check if file has YAML frontmatter
            if content.startswith("---"):
                end_marker = content.find("---", 3)
                if end_marker > 0:
                    yaml_content = content[3:end_marker].strip()
                    metadata = yaml.safe_load(yaml_content)
                    
                    if isinstance(metadata, dict) and "type" in metadata:
                        current_type = metadata["type"]
                        results["has_type"].append({
                            "file": template_file,
                            "current_type": current_type,
                            "expected_type": expected_type,
                            "needs_update": current_type != expected_type
                        })
                    else:
                        results["needs_type"].append({
                            "file": template_file,
                            "expected_type": expected_type,
                            "has_frontmatter": True,
                            "content": content
                        })
                else:
                    results["needs_type"].append({
                        "file": template_file,
                        "expected_type": expected_type,
                        "has_frontmatter": False,
                        "content": content
                    })
            else:
                results["needs_type"].append({
                    "file": template_file,
                    "expected_type": expected_type,
                    "has_frontmatter": False,
                    "content": content
                })
                
        except Exception as e:
            results["errors"].append({
                "file": template_file,
                "error": str(e)
            })
    
    return results


def add_type_to_template(template_info: Dict, dry_run: bool = True) -> bool:
    """Add type field to a template file."""
    file_path = template_info["file"]
    expected_type = template_info["expected_type"]
    content = template_info["content"]
    
    try:
        if template_info["has_frontmatter"]:
            # Add type to existing frontmatter
            end_marker = content.find("---", 3)
            yaml_content = content[3:end_marker].strip()
            rest_content = content[end_marker + 3:]
            
            # Parse and update YAML
            metadata = yaml.safe_load(yaml_content) or {}
            metadata["type"] = expected_type
            
            # Reconstruct content
            new_yaml = yaml.dump(metadata, default_flow_style=False).strip()
            new_content = f"---\n{new_yaml}\n---{rest_content}"
        else:
            # Create new frontmatter
            frontmatter = f"---\ntype: {expected_type}\n---\n"
            new_content = frontmatter + content
        
        if not dry_run:
            file_path.write_text(new_content)
        
        return True
        
    except Exception as e:
        console.print(f"[red]Error updating {file_path.name}: {e}[/red]")
        return False


def main():
    vault_path = Path("/Users/petrlavrov/work/projects/taskzilla-cm/main/root")
    
    console.print("[bold blue]📝 TEMPLATE TYPE INSERTION[/bold blue]")
    console.print(f"Analyzing templates in: {vault_path / 'templates'}")
    
    # Analyze templates
    results = analyze_templates(vault_path)
    
    if results["errors"]:
        console.print(f"[red]⚠️  {len(results['errors'])} files had errors[/red]")
        for error_info in results["errors"]:
            console.print(f"  {error_info['file'].name}: {error_info['error']}")
    
    # Show current status
    if results["has_type"]:
        table = Table(title="Templates with Type Fields")
        table.add_column("Template", style="cyan")
        table.add_column("Current Type", style="yellow")
        table.add_column("Expected Type", style="green")
        table.add_column("Status", style="blue")
        
        for info in results["has_type"]:
            status = "✓ Correct" if not info["needs_update"] else "⚠️  Update needed"
            table.add_row(
                info["file"].name,
                info["current_type"],
                info["expected_type"],
                status
            )
        
        console.print(table)
    
    # Show templates needing type fields
    if results["needs_type"]:
        table = Table(title="Templates Missing Type Fields")
        table.add_column("Template", style="cyan")
        table.add_column("Will Add Type", style="green")
        table.add_column("Has Frontmatter", style="yellow")
        
        for info in results["needs_type"]:
            frontmatter_status = "Yes" if info["has_frontmatter"] else "No (will create)"
            table.add_row(
                info["file"].name,
                info["expected_type"],
                frontmatter_status
            )
        
        console.print(table)
        
        # Ask for confirmation and execute
        if results["needs_type"]:
            import typer
            if typer.confirm(f"\nAdd type fields to {len(results['needs_type'])} templates?"):
                success_count = 0
                for template_info in results["needs_type"]:
                    if add_type_to_template(template_info, dry_run=False):
                        console.print(f"[green]✓[/green] Added type: {template_info['expected_type']} to {template_info['file'].name}")
                        success_count += 1
                
                console.print(f"\n[bold green]✅ Updated {success_count} templates[/bold green]")
            else:
                console.print("Operation cancelled.")
    
    if not results["needs_type"] and not any(info["needs_update"] for info in results["has_type"]):
        console.print("[green]✅ All templates already have correct type fields![/green]")


if __name__ == "__main__":
    main()
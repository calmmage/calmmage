#!/usr/bin/env python3
"""AI Instructions Tool CLI - Deploy AI instructions to current project."""

from pathlib import Path
from typing import List, Optional
import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from src.lib.utils import get_resources_dir

app = typer.Typer(help="AI Instructions Tool - Deploy AI instructions to current project")
console = Console()

# Available AI tools and their file mappings
AI_TOOLS = {
    "claude": {
        "filename": "CLAUDE.md",
        "template": "CLAUDE.md"
    },
    "cursor": {
        "filename": ".cursorrules", 
        "template": ".cursorrules"
    },
    "gemini": {
        "filename": "GEMINI.md",
        "template": "GEMINI.md"
    }
}

def get_templates_dir() -> Path:
    """Get the AI tools templates directory."""
    return get_resources_dir() / "llm_prompts" / "ai_tools"

def get_tech_stack_dir() -> Path:
    """Get the tech stack templates directory."""
    return get_resources_dir() / "llm_prompts" / "tech_stack"

def read_template_file(template_path: Path) -> str:
    """Read template file contents."""
    if not template_path.exists():
        console.print(f"[red]Template not found: {template_path}[/red]")
        raise typer.Exit(1)
    
    return template_path.read_text()

def read_tech_stack_files() -> str:
    """Read and combine all tech stack files."""
    tech_stack_dir = get_tech_stack_dir()
    tech_stack_content = "\n\n"
    
    for tech_file in sorted(tech_stack_dir.glob("*.md")):
        content = tech_file.read_text().strip()
        if content:
            tech_stack_content += f"{content}\n\n"
    
    return tech_stack_content

def build_final_content(ai_tool_template: str, include_tech_stack: bool = True) -> str:
    """Build final content by combining AI tool template with tech stack."""
    final_content = ai_tool_template
    
    if include_tech_stack:
        tech_stack_content = read_tech_stack_files()
        final_content += tech_stack_content
    
    return final_content

def deploy_instruction_file(ai_tool: str, target_path: Path, content: str) -> None:
    """Deploy instruction file to target location."""
    try:
        target_path.write_text(content)
        console.print(f"[green]✅ Deployed {ai_tool} instructions to {target_path}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Failed to deploy {ai_tool}: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def deploy(
    tools: Optional[List[str]] = typer.Option(None, "--tool", "-t", help="AI tools to deploy (claude, cursor, gemini)"),
    current_dir: bool = typer.Option(False, "--current", "-c", help="Deploy to current directory"),
    include_tech_stack: bool = typer.Option(True, "--tech-stack/--no-tech-stack", help="Include tech stack information"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", help="Interactive mode for tool selection")
) -> None:
    """Deploy AI instructions to current project directory."""
    
    templates_dir = get_templates_dir()
    if not templates_dir.exists():
        console.print(f"[red]Templates directory not found: {templates_dir}[/red]")
        raise typer.Exit(1)
    
    # Determine target directory
    if current_dir:
        target_dir = Path.cwd()
    else:
        target_dir = Path.cwd()
    
    console.print(f"📁 Target directory: {target_dir}")
    
    # Interactive tool selection if not specified
    if not tools and interactive:
        console.print("\n🤖 Available AI tools:")
        table = Table(show_header=True)
        table.add_column("Tool", style="cyan")
        table.add_column("File", style="yellow")
        table.add_column("Status", style="green")
        
        for tool, config in AI_TOOLS.items():
            target_file = target_dir / config["filename"]
            status = "exists" if target_file.exists() else "new"
            table.add_row(tool, config["filename"], status)
        
        console.print(table)
        
        selected_tools = []
        for tool in AI_TOOLS.keys():
            if Confirm.ask(f"Deploy {tool}?"):
                selected_tools.append(tool)
        
        tools = selected_tools
    
    # Use all tools if none specified
    if not tools:
        tools = list(AI_TOOLS.keys())
    
    if not tools:
        console.print("[yellow]No tools selected. Exiting.[/yellow]")
        return
    
    # Deploy each selected tool
    console.print(f"\n🚀 Deploying tools: {', '.join(tools)}")
    
    for tool in tools:
        if tool not in AI_TOOLS:
            console.print(f"[red]Unknown tool: {tool}[/red]")
            continue
        
        config = AI_TOOLS[tool]
        template_path = templates_dir / config["template"]
        target_path = target_dir / config["filename"]
        
        # Check if file exists
        if target_path.exists():
            if not Confirm.ask(f"File {target_path.name} exists. Overwrite?"):
                console.print(f"[yellow]Skipped {tool}[/yellow]")
                continue
        
        # Read template and build content
        template_content = read_template_file(template_path)
        final_content = build_final_content(template_content, include_tech_stack)
        
        # Deploy
        deploy_instruction_file(tool, target_path, final_content)
    
    console.print("\n[green]✨ Deployment complete![/green]")

@app.command()
def list_templates() -> None:
    """List available templates and tech stack files."""
    templates_dir = get_templates_dir()
    tech_stack_dir = get_tech_stack_dir()
    
    console.print("📋 Available AI tool templates:")
    table = Table(show_header=True)
    table.add_column("Tool", style="cyan")
    table.add_column("Template File", style="yellow")
    table.add_column("Output File", style="green")
    
    for tool, config in AI_TOOLS.items():
        template_path = templates_dir / config["template"]
        exists = "✅" if template_path.exists() else "❌"
        table.add_row(f"{exists} {tool}", config["template"], config["filename"])
    
    console.print(table)
    
    console.print("\n📚 Tech stack files:")
    for tech_file in sorted(tech_stack_dir.glob("*.md")):
        console.print(f"  • {tech_file.name}")

if __name__ == "__main__":
    app()
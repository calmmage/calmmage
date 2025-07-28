#!/usr/bin/env python3
"""AI Instructions Tool CLI - Deploy AI instructions to current project."""

from pathlib import Path
from typing import List, Optional
from enum import Enum
import subprocess
import typer
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table
from loguru import logger

from src.lib.utils import get_resources_dir

app = typer.Typer(help="AI Instructions Tool - Deploy AI instructions to current project")
console = Console()

class InstructionMode(str, Enum):
    SLIM = "slim"        # Minimal necessary instructions
    OPTIMAL = "optimal"  # Important ones (default)
    FULL = "full"        # All sections

class CustomRulesPosition(str, Enum):
    START = "start"      # Before base template
    MIDDLE = "middle"    # After base template, before tech stack  
    END = "end"          # After everything else

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

def get_current_aliases() -> str:
    """Get current shell aliases using myalias command."""
    try:
        result = subprocess.run(['myalias'], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            logger.warning(f"myalias command failed with return code {result.returncode}, stderr: {result.stderr}")
            return "# myalias command failed - aliases not available"
    except subprocess.SubprocessError as e:
        logger.warning(f"subprocess error running myalias: {e}")
        return "# myalias subprocess error - aliases not available"
    except Exception as e:
        logger.warning(f"unexpected error fetching aliases: {e}")
        return "# unexpected error - aliases not available"

def read_custom_rules(target_dir: Path) -> str:
    """Read custom LLM rules if they exist."""
    custom_rules_file = target_dir / "LLM_RULES.md"
    if custom_rules_file.exists():
        content = custom_rules_file.read_text().strip()
        if content:
            return f"{content}\n\n"
    return ""

def read_tech_stack_files(mode: InstructionMode) -> str:
    """Read and combine tech stack files based on instruction mode."""
    tech_stack_dir = get_tech_stack_dir()
    tech_stack_content = "\n\n"
    
    # Define which sections to include for each mode
    section_importance = {
        "calmmage_ecosystem.md": InstructionMode.OPTIMAL,  # Always include in optimal+
        "python_libraries.md": InstructionMode.FULL,      # Only in full mode
        "cloud_services.md": InstructionMode.FULL,        # Only in full mode
    }
    
    # Add static tech stack files based on mode
    for tech_file in sorted(tech_stack_dir.glob("*.md")):
        required_mode = section_importance.get(tech_file.name, InstructionMode.FULL)
        
        # Include section if current mode is at or above required level
        include_section = (
            mode == InstructionMode.FULL or
            (mode == InstructionMode.OPTIMAL and required_mode != InstructionMode.FULL) or
            (mode == InstructionMode.SLIM and required_mode == InstructionMode.SLIM)
        )
        
        if include_section:
            content = tech_file.read_text().strip()
            if content:
                tech_stack_content += f"{content}\n\n"
    
    # Add current aliases (include in optimal and full modes)
    if mode in [InstructionMode.OPTIMAL, InstructionMode.FULL]:
        aliases_output = get_current_aliases()
        if aliases_output:
            tech_stack_content += (
                f"# Current Shell Aliases\n\n```bash\n{aliases_output}\n```\n\n"
                "**Note**: Many tools also have Makefiles in their directories with usage examples"
                f" - check for `Makefile` when using typer CLI tools.\n\n"
            )
    
    return tech_stack_content

def build_final_content(
    ai_tool_template: str, 
    target_dir: Path,
    include_tech_stack: bool = True,
    mode: InstructionMode = InstructionMode.OPTIMAL,
    custom_position: CustomRulesPosition = CustomRulesPosition.START
) -> str:
    """Build final content by combining AI tool template with tech stack and custom rules."""
    
    # Read custom rules
    custom_rules = read_custom_rules(target_dir)
    
    # Read tech stack based on mode
    tech_stack_content = ""
    if include_tech_stack:
        tech_stack_content = read_tech_stack_files(mode)
    
    # Build final content based on custom rules position
    if custom_position == CustomRulesPosition.START:
        return custom_rules + ai_tool_template + tech_stack_content
    elif custom_position == CustomRulesPosition.MIDDLE:
        return ai_tool_template + custom_rules + tech_stack_content
    else:  # END
        return ai_tool_template + tech_stack_content + custom_rules

def update_gitignore(target_dir: Path) -> None:
    """Add AI instruction files to .gitignore if it exists."""
    gitignore_path = target_dir / ".gitignore"
    ai_files = ["CLAUDE.md", "GEMINI.md", ".cursorrules"]
    
    if not gitignore_path.exists():
        logger.info("No .gitignore file found, skipping gitignore update")
        return
    
    # Read existing gitignore
    existing_content = gitignore_path.read_text()
    lines_to_add = []
    
    for ai_file in ai_files:
        if ai_file not in existing_content:
            lines_to_add.append(ai_file)
    
    if lines_to_add:
        # Add AI files section to gitignore
        new_content = existing_content.rstrip() + "\n\n# AI instruction files (generated)\n"
        for line in lines_to_add:
            new_content += f"{line}\n"
        
        gitignore_path.write_text(new_content)
        logger.info(f"Added {len(lines_to_add)} AI files to .gitignore")
    else:
        logger.debug("All AI files already in .gitignore")

def deploy_instruction_file(ai_tool: str, target_path: Path, content: str) -> None:
    """Deploy instruction file to target location."""
    try:
        target_path.write_text(content)
        console.print(f"[green]✅ Deployed {ai_tool} instructions to {target_path}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Failed to deploy {ai_tool}: {e}[/red]")
        raise typer.Exit(1)

def deploy_ai_instructions(
    target_dir: Path,
    tools: Optional[List[str]] = None,
    include_tech_stack: bool = True,
    mode: InstructionMode = InstructionMode.OPTIMAL,
    custom_position: CustomRulesPosition = CustomRulesPosition.START,
    force_overwrite: bool = False,
    silent: bool = False,
) -> None:
    """Deploy AI instructions to a target directory.

    Args:
        target_dir: Directory to deploy instructions to
        tools: List of AI tools to deploy (None = all tools)
        include_tech_stack: Whether to include tech stack information
        mode: Instruction mode (slim, optimal, full)
        custom_position: Where to place custom rules
        force_overwrite: Overwrite existing files without asking
        silent: Suppress console output
    """
    templates_dir = get_templates_dir()
    if not templates_dir.exists():
        error_msg = f"Templates directory not found: {templates_dir}"
        if not silent:
            console.print(f"[red]{error_msg}[/red]")
        raise Exception(error_msg)

    # Use all tools if none specified
    if not tools:
        tools = list(AI_TOOLS.keys())

    if not tools:
        if not silent:
            console.print("[yellow]No tools selected.[/yellow]")
        return

    if not silent:
        console.print(f"🚀 Deploying tools: {', '.join(tools)}")

    # Deploy each selected tool
    for tool in tools:
        if tool not in AI_TOOLS:
            if not silent:
                console.print(f"[red]Unknown tool: {tool}[/red]")
            continue

        config = AI_TOOLS[tool]
        template_path = templates_dir / config["template"]
        target_path = target_dir / config["filename"]

        # Check if file exists and handle overwrite
        if target_path.exists() and not force_overwrite:
            if not silent and not Confirm.ask(
                f"File {target_path.name} exists. Overwrite?"
            ):
                if not silent:
                    console.print(f"[yellow]Skipped {tool}[/yellow]")
                continue

        # Read template and build content
        template_content = read_template_file(template_path)
        final_content = build_final_content(
            template_content, target_dir, include_tech_stack, mode, custom_position
        )

        # Deploy the file
        try:
            target_path.write_text(final_content)
            if not silent:
                console.print(
                    f"[green]✅ Deployed {tool} instructions to {target_path}[/green]"
                )
        except Exception as e:
            error_msg = f"Failed to deploy {tool}: {e}"
            if not silent:
                console.print(f"[red]❌ {error_msg}[/red]")
            raise Exception(error_msg)

    # Update .gitignore
    update_gitignore(target_dir)

    if not silent:
        console.print("[green]✨ Deployment complete![/green]")

@app.command()
def deploy(
    tools: Optional[List[str]] = typer.Option(None, "--tool", "-t", help="AI tools to deploy (claude, cursor, gemini)"),
    current_dir: bool = typer.Option(False, "--current", "-c", help="Deploy to current directory"),
    include_tech_stack: bool = typer.Option(True, "--tech-stack/--no-tech-stack", help="Include tech stack information"),
    mode: InstructionMode = typer.Option(InstructionMode.OPTIMAL, "--mode", "-m", help="Instruction mode: slim, optimal, or full"),
    custom_position: CustomRulesPosition = typer.Option(CustomRulesPosition.START, "--custom-position", help="Where to place custom LLM_RULES.md content"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", help="Interactive mode for tool selection")
) -> None:
    """Deploy AI instructions to current project directory."""
    
    # Determine target directory
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
    
    # Use the reusable deployment function
    deploy_ai_instructions(
        target_dir=target_dir,
        tools=tools,
        include_tech_stack=include_tech_stack,
        mode=mode,
        custom_position=custom_position,
        force_overwrite=False,  # CLI uses interactive prompts
        silent=False  # CLI shows output
    )

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

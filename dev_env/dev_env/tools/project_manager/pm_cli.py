import sys
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional

import pyperclip
import typer
from calmlib.utils import load_global_env
from loguru import logger
from rich.console import Console

from dev_env.core.pm_utils.name_generator import (
    EditorChoice,
    generate_project_name,
    open_in_editor,
    prompt_editor_choice,
)
from dev_env.tools.project_discoverer.pd_cli import show_result_menu
from dev_env.tools.project_discoverer.project_discoverer import ProjectDiscoverer
from dev_env.tools.project_manager.project_manager import ProjectManager

load_global_env()

pm = ProjectManager()
app = typer.Typer()
pd = ProjectDiscoverer()

console = Console()


def setup_logger(logger, level: str = "INFO"):
    logger.remove()  # Remove default handler
    logger.add(
        sink=sys.stderr,
        format="<level>{time:HH:mm:ss}</level> | <level>{message}</level>",
        colorize=True,
        level=level,
    )


# ------------------------------------------------------------
# region New Project
# ------------------------------------------------------------


def parse_template_name(template_name: str):
    """Parse the template name and return the correct one."""
    matches = pm.complete_template_name(template_name)
    if len(matches) == 1:
        name, _help = matches[0]
        return name
    else:
        raise typer.BadParameter(
            f"Invalid template name: {template_name}. {matches=}",
            param_hint="template",
        )


@app.command(
    name="new-project",
    help="Create a new project in github and clone to experiments destination",
)
def new_project(
    name: Annotated[
        Optional[str],
        typer.Argument(
            help="Name of the project (if contains '-bot', will use botspot-template by default)",
        ),
    ] = None,
    template: Annotated[
        Optional[str],
        typer.Option(
            "--template",
            "-t",
            help="Template name for the GitHub project. If not provided, uses botspot-template for bot projects, python-project-template otherwise.",
            autocompletion=pm.complete_template_name,
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Print what would be done without actually doing it",
        ),
    ] = False,
    editor: Annotated[
        Optional[EditorChoice],
        typer.Option(
            "--editor",
            "-e",
            help="Open project in editor after creation",
        ),
    ] = None,
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            help="Enable debug logging",
        ),
    ] = False,
):
    """Create a new project in github and clone to experiments destination"""
    setup_logger(logger, "DEBUG" if debug else "INFO")
    # Generate name if not provided
    if name is None:
        name = generate_project_name()

    if template:
        template = parse_template_name(template)

    project_dir = pm.create_project(name, template=template, dry_run=dry_run)

    if not dry_run:
        console.print(f"✨ [green]Project created at:[/] {project_dir}")
        editor = prompt_editor_choice(editor)
        if editor:
            open_in_editor(project_dir, editor)
    else:
        console.print(f"✨ [yellow]Dry run:[/] Would create project at {project_dir}")


# endregion New Project

# ------------------------------------------------------------
# region Mini Project
# ------------------------------------------------------------


def complete_mini_project_template(incomplete: str):
    """Autocomplete mini-project template names"""
    templates = ["mini-botspot-template"]  # Add more as needed
    return [t for t in templates if t.startswith(incomplete)]


@app.command(
    name="new-mini-project",
    help="Create a new mini-project in seasonal folder structure",
)
def new_mini_project(
    name: Annotated[
        Optional[str],
        typer.Argument(
            help="Name of the mini-project",
        ),
    ] = None,
    description: Annotated[
        Optional[str],
        typer.Option(
            "--description",
            "-d",
            help="Project description or idea",
        ),
    ] = None,
    template: Annotated[
        Optional[str],
        typer.Option(
            "--template",
            "-t",
            help="Template to use. If not provided, auto-detects based on name.",
            autocompletion=complete_mini_project_template,
        ),
    ] = None,
    private: Optional[bool] = None,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Print what would be done without actually doing it",
        ),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            help="Enable debug logging",
        ),
    ] = False,
    editor: Annotated[
        Optional[EditorChoice],
        typer.Option(
            "--editor",
            "-e",
            help="Open project in editor after creation",
        ),
    ] = None,
):
    """Create a new mini-project in seasonal folder structure"""
    setup_logger(logger, "DEBUG" if debug else "INFO")
    # Generate name if not provided
    if name is None:
        name = generate_project_name()

    # if user didn't specify private, ask
    if private is None:
        private = typer.confirm("Create in private repository?", default=False)

    project_dir = pm.create_mini_project(
        name,
        description,
        private,
        dry_run=dry_run,
        template=template,
    )

    if not dry_run:
        console.print(f"✨ [green]Mini-project created at:[/] {project_dir}")
        editor = prompt_editor_choice(editor)
        if editor:
            open_in_editor(project_dir, editor)
    else:
        console.print(
            f"✨ [yellow]Dry run:[/] Would create mini-project at {project_dir}"
        )


# endregion Mini Project

# ------------------------------------------------------------
# region WIP
# ------------------------------------------------------------


@app.command(
    name="move-to-examples", help="Move a file or directory to examples destination"
)
def move_to_examples(
    path: Annotated[
        Path,
        typer.Argument(
            ...,
            help="Path to the file or directory to move to examples",
        ),
    ],
):
    """Move a file or directory to examples destination"""
    result = pm.move_to_examples(path)
    console.print(f"✨ [green]Moved to examples:[/] {result}")


def get_project_dir(path: Path, mini_projects: bool = False) -> Optional[Path]:
    """
    Get the top-level project directory for the given path.

    Returns None if no project directory is found.
    """
    project_dirs = pd.get_outer_project_dirs(path)
    if mini_projects:
        return project_dirs[-1] if project_dirs else None
    else:
        return project_dirs[0] if project_dirs else None


@app.command(name="get-project", help="Get the project directory for the current path")
def get_project(
    path: Annotated[
        Optional[Path],
        typer.Argument(
            help="Path to check (defaults to current directory)",
        ),
    ] = None,
    mini_projects: Annotated[
        bool,
        typer.Option(
            "-m",
            "--mini-projects",
            help="Get the mini-project directory instead of the main project directory",
        ),
    ] = False,
):
    """Get the project directory for the given path or current directory"""
    check_path = path or Path.cwd()
    project_dir = get_project_dir(check_path, mini_projects=mini_projects)

    if project_dir:
        console.print(f"✨ [green]Project directory found:[/] {project_dir}")
    else:
        console.print("[yellow]No project directory found[/]")


@app.command(name="new-todo", help="Create a new todo file in the project")
def new_todo(
    project_name: Annotated[
        Optional[str],
        typer.Argument(
            help="Project name to search for (defaults to current directory)",
        ),
    ] = None,
    text: Annotated[
        Optional[str],
        typer.Option(
            "--text",
            "-t",
            help="Todo text to append (if not provided, will open editor)",
        ),
    ] = None,
    mini_projects: Annotated[
        bool,
        typer.Option(
            "-m",
            "--mini-projects",
            help="Look for mini-project directory instead of main project",
        ),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            help="Enable debug logging",
        ),
    ] = False,
):
    """Create a new todo file in the project directory"""
    # Get project directory
    setup_logger(logger, "DEBUG" if debug else "INFO")
    if project_name:
        # Search for project by name
        results = pd.quick_search(project_name)
        if not results:
            console.print("[red]No projects found[/]")
            raise typer.Exit(1)
        elif len(results) == 1:
            project_dir = results[0]
        else:
            # Use existing menu function
            result = show_result_menu(results)
            if result is None:
                raise typer.Exit()
            project_dir = Path(result)
    else:
        # Try current directory
        project_dir = get_project_dir(Path.cwd(), mini_projects=mini_projects)
        if not project_dir:
            # Ask user for project name and search
            project_name = typer.prompt(
                "Project not found. Enter project name to search"
            )
            results = pd.quick_search(project_name)
            if not results:
                console.print("[red]No projects found[/]")
                raise typer.Exit(1)
            elif len(results) == 1:
                project_dir = results[0]
            else:
                result = show_result_menu(results)
                if result is None:
                    raise typer.Exit()
                project_dir = Path(result)

    # Roll up old todos before creating new one
    rolled_up_path = pm.rollup_todos(project_dir)
    if rolled_up_path:
        console.print(f"📝 [blue]Rolled up old todos to:[/] {rolled_up_path}")

    # Rest of the function remains the same
    todo_dir = project_dir / pm.config.todo_subfolder
    todo_dir.mkdir(exist_ok=True, parents=True)

    todo_filename = datetime.now().strftime(pm.config.todo_filename_template)
    todo_path = todo_dir / todo_filename

    if text:
        # Append text to file
        with open(todo_path, "a") as f:
            if todo_path.exists() and todo_path.stat().st_size > 0:
                f.write("\n")
            f.write(f"- {text}\n")
        console.print(f"✨ [green]Added todo to:[/] {todo_path}")
    else:
        # Create file if doesn't exist
        if not todo_path.exists():
            todo_path.touch()
        # Open in default editor
        pm.open_in_editor(todo_path)
        console.print(f"✨ [green]Todo file opened:[/] {todo_path}")


@app.command(name="new-feature", help="Create a new feature directory in the project")
def new_feature(
    feature_name: Annotated[
        str,
        typer.Argument(
            help="Name of the feature directory to create",
        ),
    ],
    project_name: Annotated[
        Optional[str],
        typer.Argument(
            help="Project name to search for (defaults to current directory)",
        ),
    ] = None,
    mini_projects: Annotated[
        bool,
        typer.Option(
            "-m",
            "--mini-projects",
            help="Look for mini-project directory instead of main project",
        ),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            help="Enable debug logging",
        ),
    ] = False,
):
    """Create a new feature directory in the project's dev/draft folder"""
    setup_logger(logger, "DEBUG" if debug else "INFO")
    # Get project directory
    if project_name:
        # Search for project by name
        results = pd.quick_search(project_name)
        if not results:
            console.print("[red]No projects found[/]")
            raise typer.Exit(1)
        elif len(results) == 1:
            project_dir = results[0]
        else:
            result = show_result_menu(results)
            if result is None:
                raise typer.Exit()
            project_dir = Path(result)
    else:
        # Try current directory
        project_dir = get_project_dir(Path.cwd(), mini_projects=mini_projects)
        if not project_dir:
            # Ask user for project name and search
            project_name = typer.prompt(
                "Project not found. Enter project name to search"
            )
            results = pd.quick_search(project_name)
            if not results:
                console.print("[red]No projects found[/]")
                raise typer.Exit(1)
            elif len(results) == 1:
                project_dir = results[0]
            else:
                result = show_result_menu(results)
                if result is None:
                    raise typer.Exit()
                project_dir = Path(result)

    # Create feature directory
    feature_dir = project_dir / pm.config.features_subfolder / feature_name
    feature_dir.mkdir(exist_ok=True, parents=True)

    # Copy path to clipboard
    pyperclip.copy(str(feature_dir.absolute()))
    console.print(
        f"✨ [green]Feature directory created:[/] {feature_dir}. Path copied to clipboard."
    )


# endregion WIP

if __name__ == "__main__":
    app()

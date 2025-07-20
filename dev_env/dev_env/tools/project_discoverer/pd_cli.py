import sys
from pathlib import Path
from typing import Annotated, List, Optional

import typer
from loguru import logger
from rich.console import Console

from dev_env.core.pm_utils.name_generator import (
    EditorChoice,
    open_in_editor,
    prompt_editor_choice,
)
from dev_env.tools.project_discoverer.project_discoverer import ProjectDiscoverer

app = typer.Typer()
pd = ProjectDiscoverer()
console = Console()


def show_result_menu(results: List[Path]):
    """Show a menu to choose from multiple results"""
    options = [f"{i}. {path}" for i, path in enumerate(results, 1)]
    options.append("0. Exit. Search more (not implemented yet)")
    # show user menu with typer
    user_choice = typer.prompt("\n".join(options), type=int)
    if user_choice == 0:
        # exiting
        return None

    return results[user_choice - 1]


# todo: I will need to change aliases if I add more commands
@app.command(name="find", help="Find a project by name")
def find_project(
    query: Annotated[
        str,
        typer.Argument(
            ...,
            help="Name of the project to find",
        ),
    ],
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            "-d",
            help="Enable debug logging",
        ),
    ] = False,
    editor: Annotated[
        Optional[EditorChoice],
        typer.Option(
            "--editor",
            "-e",
            help="Editor to open the project in",
            case_sensitive=False,
        ),
    ] = None,
):
    """Find a project by name"""
    # Configure logging based on debug flag
    logger.remove()  # Remove all existing handlers
    if debug:
        # Debug mode: show all logs with detailed format
        logger.add(
            sys.stderr,
            level="DEBUG",
            format="<level>{level: <8}</level>"
            "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - {message}",
        )
    else:
        # Normal mode: show only INFO and above with simpler format
        logger.add(
            sys.stderr,
            level="INFO",
            format="{message}",  # Simplified format for normal use
            filter=lambda record: record["level"].name
            in ["INFO", "WARNING", "ERROR", "CRITICAL"],
        )

    logger.debug(f"Starting project search with query: {query}")
    # Quick search in common locations
    results = pd.quick_search(query)
    logger.debug(f"Found {len(results)} results")

    if len(results) == 1:
        # Single result found
        result = results[0]
    elif not results:
        logger.info("No projects found in common locations")
        logger.info("Try using 'fp_' or 'find' aliases to search with ripgrep")
        return
    else:
        result = show_result_menu(results)
        if result is None:
            return

    # Prompt for editor choice if not provided
    editor = prompt_editor_choice(editor)
    if editor:
        open_in_editor(result, editor)


if __name__ == "__main__":
    app()

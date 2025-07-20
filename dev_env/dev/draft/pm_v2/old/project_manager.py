from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from dev_env.core.constants import experiments_dir
from dev_env.core.ffs import get_seasonal_dev_dir
from dev_env.core.git_utils import clone_repo, create_repo_from_template
from dev_env.core.settings import settings
from loguru import logger

from calmlib.utils.main import is_subsequence

app = typer.Typer()


class ProjectType(Enum):
    MINI = "mini"
    FULL = "full"


def fuzzy_match_template(template: str, templates: list[str]) -> Optional[str]:
    exact_matches = [t for t in templates if t.lower() == template.lower()]
    if exact_matches:
        return exact_matches[0]

    prefix_matches = [t for t in templates if t.lower().startswith(template.lower())]
    if len(prefix_matches) == 1:
        return prefix_matches[0]

    subsequence_matches = [
        t for t in templates if is_subsequence(template.lower(), t.lower())
    ]
    if len(subsequence_matches) == 1:
        return subsequence_matches[0]

    return None


def get_template(template: str) -> str:
    templates = settings.github_templates

    matched_template = fuzzy_match_template(template, templates)
    if matched_template:
        return matched_template
    else:
        raise typer.BadParameter(f"No matching template found for '{template}'")


@app.command()
def start_new_project(
    name: str = typer.Argument(..., help="Name of the new project"),
    project_type: ProjectType = typer.Option(
        ProjectType.MINI, help="Type of project to create"
    ),
    template: Optional[str] = typer.Option(
        None, help="Template to use for full projects"
    ),
):
    """
    Start a new project based on the specified type and template (for full projects).
    """
    if project_type == ProjectType.MINI:
        result = create_mini_project(name)
    elif project_type == ProjectType.FULL:
        if template is None:
            template = settings.seasonal_dir_template_repo
        template = get_template(template)
        result = create_full_project(name, template)
    else:
        raise typer.BadParameter(f"Unknown project type: {project_type}")

    typer.echo(f"Project created successfully at: {result}")
    # typer.echo(f"Path copied to clipboard: {result}")
    import pyperclip

    pyperclip.copy(str(result))


def create_mini_project(name: str) -> Path:
    seasonal_dev_dir = get_seasonal_dev_dir()
    target_dir = seasonal_dev_dir / "dev" / "draft"
    project_dir = target_dir / name
    project_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created mini project at {project_dir}")
    return project_dir


def create_full_project(
    name: str, template: str = settings.default_github_template
) -> Path:
    new_repo = create_repo_from_template(name, template)
    project_dir = experiments_dir / name
    cloned_repo = clone_repo(new_repo, project_dir)
    if cloned_repo:
        logger.info(f"Created full project from template at {project_dir}")
        return project_dir
    else:
        logger.error(f"Failed to create full project {name}")
        raise typer.Abort()


@app.command()
def list_templates():
    """
    List available GitHub project templates.
    """
    templates = settings.github_templates
    typer.echo("GitHub templates:")

    for template in templates:
        typer.echo(f"- {template}")


@app.command()
def move_to_experiments(
    project_path: Path = typer.Argument(
        ..., help="Path to the project to move to experiments"
    ),
    project_name: Optional[str] = typer.Option(
        None, help="Name for the experiments project"
    ),
):
    """
    Move a project to the calmmage/experiments directory.
    """
    result = move_project_to_experiments(project_path, project_name)
    typer.echo(f"Project moved to experiments: {result}")


if __name__ == "__main__":
    app()

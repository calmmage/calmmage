import os
from itertools import chain
from pathlib import Path

import typer
from typing_extensions import Annotated

from calmmage.dev_env import CalmmageDevEnv
from calmmage.dev_env import DEFAULT_ROOT_DIR

# Instantiate the CalmmageDevEnv object
dev_env = CalmmageDevEnv()
app = typer.Typer(name="Calmmage Project Manager")

# todo: use local templates from the folder because it's faster
#  use ENV variable to decide if this is a friendly env where such a folder exists
projects_templates_dir = os.getenv("CALMMAGE_PROJECT_TEMPLATES_DIR")

github_templates = []
local_templates = []

if projects_templates_dir:
    projects_templates_dir = Path(projects_templates_dir)
    local_templates = projects_templates_dir.iterdir()
    for template in local_templates:
        # check if .git folder exists
        if (template / ".git").exists():
            # todo: improve descriptions?
            github_templates.append((template.name, "GitHub"))
        else:
            # todo: improve descriptions?
            github_templates.append((template.name, "Local"))

else:
    # Fetch GitHub templates for autocompletion
    try:
        for template_name in dev_env.get_github_template_names():
            github_templates.append(
                (template_name, dev_env.get_template_description(template_name))
            )
    except Exception:
        typer.echo("Failed to fetch GitHub templates.")
    for template_name in dev_env.get_local_template_names():
        local_templates.append((template_name, "Local"))


# Define a function for autocompleting template names
def complete_github_template_name(incomplete: str):
    # hack: always yield the incomplete string to avoid typer error (broken completion)
    # todo: report the issue to typer
    yield incomplete
    for template_name, help_text in github_templates:
        if template_name.startswith(incomplete):
            if help_text:
                yield template_name, help_text
            else:
                yield template_name


def complete_template_name(incomplete: str):
    yield incomplete
    for template_name, help_text in chain(local_templates, github_templates):
        if template_name.startswith(incomplete):
            if help_text:
                yield template_name, help_text
            else:
                yield template_name


@app.command(name="move2gh")
def move_project_to_github(
    project_path: Annotated[
        str,
        typer.Option(
            prompt="Project path (What project do you want to move to GitHub?)\nPath",
        ),
    ],
    template_name: Annotated[
        str,
        typer.Option(
            help="Template name for the GitHub project.",
            autocompletion=complete_github_template_name,
        ),
    ] = None,
    project_name: Annotated[
        str, typer.Option(help="Name of the project to move to GitHub.")
    ] = None,
):
    # Perform the action: Move project to GitHub using the selected template
    # project_name = project_path.split("/")[-1]  # Infer project name from path
    dev_env.move_project_to_github(
        project_path, template_name=template_name, project_name=project_name
    )
    typer.echo(
        f"Project {project_name} moved to GitHub using template {template_name}."
    )


# todo: rework this completely - to use the templates vars defined above
@app.command(name="lt")
def list_templates(
    local: bool = True,
    root_dir: str = DEFAULT_ROOT_DIR,
    app_data_dir: str = DEFAULT_ROOT_DIR,
):
    # dev_env = CalmmageDevEnv(root_dir, app_data_dir)
    # # todo: return, then typer.echo
    # templates = dev_env.list_templates(local=local)
    # for template in templates:
    #     typer.echo(template)
    typer.echo("Local templates:")
    for template_name in local_templates:
        typer.echo(template_name)
    typer.echo("GitHub templates:")
    for template_name, help_text in github_templates:
        if help_text:
            typer.echo(f"{template_name} - {help_text}")
        else:
            typer.echo(template_name)


@app.command(name="add")
def add_new_project(
    name: Annotated[
        str,
        typer.Option(
            prompt="Name (What do you want the project to do?)\nName",
        ),
    ],
    template_name: Annotated[
        str,
        typer.Option(
            autocompletion=complete_template_name,
            default="default",
        ),
    ],
    # local: bool = True,
    # root_dir: str = DEFAULT_ROOT_DIR,
    # app_data_dir: str = DEFAULT_ROOT_DIR,
):
    # todo: local: Annotated[bool, typer.Option(default=True, prompt=True)],
    # dev_env = CalmmageDevEnv(root_dir, app_data_dir)
    local = template_name in local_templates
    project_dir = dev_env.start_new_project(
        name, local=local, template_name=template_name
    )

    # todo: change the dir to new project? or just print the path?
    typer.echo(project_dir)


if __name__ == "__main__":
    app()

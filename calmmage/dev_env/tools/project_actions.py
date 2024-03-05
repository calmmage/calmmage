import typer
from typing_extensions import Annotated
from calmmage.dev_env import CalmmageDevEnv
import os
from pathlib import Path

# Instantiate the CalmmageDevEnv object
dev_env = CalmmageDevEnv()
app = typer.Typer()

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
    for template_name in dev_env.get_github_template_names():
        github_templates.append(
            (template_name, dev_env.get_template_description(template_name))
        )


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


@app.command(name="move2gh")
def move_project_to_github(
    project_path: Annotated[
        str,
        typer.Option(
            prompt="Project path (What project do you want to move to GitHub?)\nPath",
        ),
    ],
    project_name: Annotated[
        str, typer.Option(help="Name of the project to move to GitHub.")
    ] = None,
    template_name: Annotated[
        str,
        typer.Option(
            help="Template name for the GitHub project.",
            autocompletion=complete_github_template_name,
        ),
    ] = None,
):
    template_name = template_name.replace("_", "-")
    # Perform the action: Move project to GitHub using the selected template
    # project_name = project_path.split("/")[-1]  # Infer project name from path
    dev_env.move_project_to_github(
        project_path, template_name=template_name, project_name=project_name
    )
    typer.echo(
        f"Project {project_name} moved to GitHub using template {template_name}."
    )


if __name__ == "__main__":
    app()

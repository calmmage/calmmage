import os
from pathlib import Path

import typer
from typing_extensions import Annotated

from calmmage.dev_env import CalmmageDevEnv


# todo: move to calmlib
def is_subsequence(sub, main):
    sub_index = 0
    main_index = 0
    while sub_index < len(sub) and main_index < len(main):
        if sub[sub_index] == main[main_index]:
            sub_index += 1
        main_index += 1
    return sub_index == len(sub)


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
    templates = projects_templates_dir.iterdir()
    for template_dir in templates:
        # check if .git folder exists
        if (template_dir / ".git").exists():
            # todo: improve descriptions?
            github_templates.append((template_dir.name, "GitHub"))
        else:
            # todo: improve descriptions?
            local_templates.append((template_dir.name, "Local"))

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

github_templates = list(sorted(github_templates))
local_templates = list(sorted(local_templates))

# check name collisions\
collisions = set(github_templates) & set(local_templates)
if collisions:
    typer.secho(
        f"Warning: Name collision between local and GitHub templates. {collisions=}"
        "Local templates will be preferred.",
        fg=typer.colors.YELLOW,
    )


# todo: rename and move to calmlib
def _complete_template_name(incomplete: str, candidates):
    matches = []
    for template, help_text in candidates:
        if template.startswith(incomplete):
            matches.append((template, help_text))
    if len(matches) == 1:
        return matches

    for template, help_text in candidates:
        if is_subsequence(incomplete, template):
            matches.append((template, help_text))

    if len(matches) == 1:
        return matches
    # hack: always add the incomplete string to avoid typer error (broken completion)
    # todo: report the issue to typer
    matches.append((incomplete, ""))
    return matches


def complete_template_name(incomplete: str):
    candidates = local_templates + github_templates
    return _complete_template_name(incomplete, candidates)


def complete_github_template_name(incomplete: str):
    return _complete_template_name(incomplete, github_templates)


# todo: rename and move to calmlib
def parse_template_name(template_name: str, candidates=None):
    if not candidates:
        candidates = github_templates + local_templates
    matches = list(_complete_template_name(template_name, candidates))
    if len(matches) == 1:
        name, _help = matches[0]
        return name
    else:
        raise typer.BadParameter(
            f"Invalid template name: {template_name}. {matches=}",
            param_hint=f"template",
        )


@app.command(name="move2gh")
def move_project_to_github(
    project_path: Annotated[
        str,
        typer.Option(
            prompt="Project path (What project do you want to move to GitHub?)\nPath",
        ),
    ],
    template: Annotated[
        str,
        typer.Option(
            ...,
            "--template",
            "-t",
            help="Template name for the GitHub project.",
            autocompletion=complete_github_template_name,
        ),
    ] = None,
    project_name: Annotated[
        str,
        typer.Option(
            ...,
            "--project-name",
            "-n",
            "--name",
            help="Name of the project to move to GitHub.",
        ),
    ] = None,
):
    template = parse_template_name(template, github_templates)
    # Perform the action: Move project to GitHub using the selected template
    # project_name = project_path.split("/")[-1]  # Infer project name from path
    dev_env.move_project_to_github(
        project_path, template_name=template, project_name=project_name
    )
    typer.echo(f"Project {project_name} moved to GitHub using template {template}.")
    typer.echo(f"Project backup is available at {project_path}_backup")


# todo: rework this completely - to use the templates vars defined above
@app.command(name="lt")
def list_templates():
    typer.secho("Local templates:", fg=typer.colors.GREEN, bold=True)
    for template, _ in local_templates:
        typer.echo(template)

    typer.secho("\nGitHub templates:", fg=typer.colors.GREEN, bold=True)
    for template, _ in github_templates:
        # if help_text:
        #     typer.echo(f"{template} - {help_text}")
        # else:
        typer.echo(template)


@app.command(name="add")
def add_new_project(
    name: Annotated[
        str,
        typer.Option(
            prompt="Name (What do you want the project to do?)\nName",
        ),
    ],
    template: Annotated[
        str,
        typer.Option(
            autocompletion=complete_template_name,
            # default="default",
        ),
    ],
):
    template = parse_template_name(template)
    local = any([template == t[0] for t in local_templates])
    typer.echo(f"Using template {template}, {'GitHub' if not local else 'Local'}.")
    project_dir = dev_env.start_new_project(name, local=local, template_name=template)

    # todo: change the dir to new project? or just print the path?
    typer.echo(project_dir)


if __name__ == "__main__":
    app()
    # print(complete_template_name("pye"))
    # template = parse_template_name("pye")

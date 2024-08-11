import os
from pathlib import Path

import pyperclip
import typer
from typing_extensions import Annotated

from calmlib.utils.common import is_subsequence
from calmmage.dev_env import CalmmageDevEnv

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
        if not template_dir.is_dir() or template_dir.name.startswith("."):
            continue
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


@app.command(name="move2gh", help="Move project to GitHub using the selected template")
def move_project_to_github(
    project_path: Annotated[
        Path,
        typer.Argument(
            ...,
            file_okay=False,
            help="Path to the project to move to GitHub.",
            # prompt="Project path (What project do you want to move to GitHub?)\nPath",
        ),
    ],
    template: Annotated[
        str,
        typer.Option(
            "--template",
            "-t",
            help="Template name for the GitHub project.",
            autocompletion=complete_github_template_name,
        ),
    ] = "python-project-template",
    project_name: Annotated[
        str,
        typer.Option(
            ...,
            "--name",
            "-n",
            help="Name for the GitHub project.",
        ),
    ] = None,
):
    """
    Move project to GitHub using the selected template
    Pulls the new repo, then copies the project files to the new repo, overwriting any existing files.
    Saves a backup of the original project in the backups folder.

    cli alias: move2gh
    usage: move2gh <project_path> -t <template> -n <project_name>
    """
    template = parse_template_name(template, github_templates)
    if project_name is None:
        project_name = project_path.name
    dev_env.move_project_to_github(
        project_path, template_name=template, project_name=project_name
    )
    typer.echo(f"Project {project_name} moved to GitHub using template {template}.")
    backup_path = dev_env.get_latest_backup_path(project_path)
    typer.echo(f"Project backup is available at {backup_path}")
    pyperclip.copy(str(backup_path))


# exp dir path: dev_env.root_dir / "code/structured/dev/calmmage-dev/calmmage/experiments/seasonal/..."
@app.command(name="move2exp", help="Move project to calmmage/experiments dir")
def move_project_to_experiments(
    project_path: Annotated[
        Path,
        typer.Argument(
            ...,
            file_okay=False,
            help="Path to the project to move to experiments.",
            # prompt="Project path (What project do you want to move to experiments?)\nPath",
        ),
    ],
    project_name: Annotated[
        str,
        typer.Option(
            ...,
            "--name",
            "-n",
            help="Name for the experiments project.",
        ),
    ] = None,
):
    """
    Move project to experiments
    cli alias: move2exp
    usage: move2exp <project_path> -n <project_name>
    example: move2exp /path/to/project -n my_project
    """
    if project_name is None:
        project_name = project_path.name
    new_path = dev_env.move_project_to_experiments(
        project_path, project_name=project_name
    )
    typer.echo(f"Project {project_name} moved to {new_path}")
    pyperclip.copy(str(new_path))


# beta dir path: dev_env.root_dir / "code/structured/dev/calmlib-dev/calmlib/beta"
@app.command(name="move2beta", help="Move project to calmilb/beta")
def move_project_to_beta(
    project_path: Annotated[
        Path,
        typer.Argument(
            ...,
            file_okay=False,
            help="Path to the project to move to beta.",
            # prompt="Project path (What project do you want to move to beta?)\nPath",
        ),
    ],
    project_name: Annotated[
        str,
        typer.Option(
            ...,
            "--name",
            "-n",
            help="Name for the beta project.",
        ),
    ] = None,
):
    """
    Move project to calmilb/beta (assuming / converting to an importable package)
    cli alias: move2beta, mv2b
    usage: move2beta <project_path> -n <project_name>
    """
    if project_name is None:
        project_name = project_path.name
    new_path = dev_env.move_project_to_beta(project_path, project_name=project_name)
    typer.echo(f"{project_name} moved to {new_path}")
    pyperclip.copy(str(new_path))


@app.command(name="lt", help="List available github and local templates")
def list_templates():
    """
    List github and local templates
    cli alias: lt
    usage: lt
    """
    typer.secho("Local templates:", fg=typer.colors.GREEN, bold=True)
    for template, _ in local_templates:
        typer.echo(template)

    typer.secho("\nGitHub templates:", fg=typer.colors.GREEN, bold=True)
    for template, _ in github_templates:
        # if help_text:
        #     typer.echo(f"{template} - {help_text}")
        # else:
        typer.echo(template)


def move_and_symlink(source, dest):
    source = Path(source)
    dest = Path(dest)
    if dest.exists():
        raise FileExistsError(f"Destination already exists: {dest}")
    import shutil

    shutil.move(source, dest)
    source.symlink_to(dest)


@app.command(name="np", help="Add a new project")
def add_new_project(
    name: Annotated[
        str,
        typer.Argument(
            # ...,
            # "--name",
            # "-n",
            # prompt="Name (What do you want the project to do?)\nName",
            help="Name for the new project.",
        ),
    ],
    template: Annotated[
        str,
        typer.Option(
            "--template",
            "-t",
            autocompletion=complete_template_name,
            help="Template name for the new project "
            "- use 'lt' command to list available templates.",
        ),
    ] = "default",
):
    """
    Create a new project in the seasonal experiments dir using the selected template
    cli alias: np
    usage: np <name> -t <template>
    example: np my_project -t pyexp

    Check available templates with 'lt' command

    You can use any subsequence of the template name
    if it identifies a single template - for example,
    'pyexp' for python_experiment template
    """
    template = parse_template_name(template)
    local = any([template == t[0] for t in local_templates])
    typer.echo(f"Using template {template}, {'GitHub' if not local else 'Local'}.")
    project_dir = dev_env.start_new_project(name, local=local, template_name=template)

    # new paradygm: move project dir to structured_dir and create a symlink back
    dest_path = dev_env.all_projects_dir / name
    try:
        move_and_symlink(project_dir, dest_path)
        typer.echo(project_dir)
    except Exception as e:
        typer.echo(f"Failed to move and symlink the project: {e}")
        typer.echo(f"Project is available at {project_dir}")
        typer.echo(f"Please move it manually to {dest_path}")

    # todo: change the dir to new project? or just print the path?
    pyperclip.copy(str(project_dir))


if __name__ == "__main__":
    app()
    # print(complete_template_name("pye"))
    # template = parse_template_name("pye")

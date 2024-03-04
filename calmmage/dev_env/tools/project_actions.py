import typer
from calmmage.dev_env import CalmmageDevEnv
from beaupy import select
import os
from pathlib import Path

app = typer.Typer()

@app.command()
def move_project_to_github(project_path: str):
    # Instantiate the CalmmageDevEnv object
    dev_env = CalmmageDevEnv()

    # Combine GitHub and local templates for selection
    github_templates = dev_env.get_github_template_names()
    # local_templates_dir = os.path.join(os.getcwd(), "templates")
    local_templates_dir = Path("/Users/calm/work/code/structured/beta/project_templates")
    local_templates = [f for f in os.listdir(local_templates_dir) if os.path.isdir(os.path.join(local_templates_dir, f))]
    combined_templates = {"GitHub": github_templates, "Local": local_templates}

    # Flatten the list for display
    flattened_templates = [f"{source}: {template}" for source, templates in combined_templates.items() for template in templates]

    # Show selection menu with arrows
    choice = select(flattened_templates, "Choose a template:")

    # Extract choice details
    choice_source, choice_template = choice.split(": ", 1)

    # Perform the action based on the selected template
    if choice_source == "GitHub":
        # Move project to GitHub using the selected GitHub template
        dev_env.move_project_to_github(project_path, template_name=choice_template, project_name=None)
    elif choice_source == "Local":
        typer.echo("Moving project to GitHub using a local template is not supported.")
    else:
        typer.echo("Invalid template selection.")

if __name__ == "__main__":
    app()

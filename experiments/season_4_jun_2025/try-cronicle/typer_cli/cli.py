"""
A CLI for the Cronicle API.

This CLI is used to interact with the Cronicle API.

It is used to:
- Create a new job
- Update a job
- Delete a job / pause a job
"""

import typer
import os
import requests
from typing_extensions import Annotated


app = typer.Typer()

from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

CRONICLE_URL = os.environ.get("CRONICLE_URL", "http://localhost:3012")
CRONICLE_API_KEY = os.environ.get("CRONICLE_API_KEY")

plugin_id_map = {
    "python": "pmc6gxqss0t",
    "shell": "shellplug",
}

category_id_map = {
    "general": "general",
}


@app.command()
def create_job(
    name: str,
    script_path: str,
    category: Annotated[
        str, typer.Argument(..., help="The Category ID to assign the event to.")
    ] = "general",
    # choices: python, shell
    # todo: rewrite to use typer choices
    plugin: Annotated[
        str, typer.Option(help="Cronicle Plugin ID for python jobs.")
    ] = "python",
    target_group: Annotated[
        str, typer.Option(help="The server group to target.")
    ] = "all_servers",
    hours: Annotated[
        str, typer.Option(help="Comma-separated list of hours (0-23) for the schedule.")
    ] = None,
    minutes: Annotated[
        str,
        typer.Option(help="Comma-separated list of minutes (0-59) for the schedule."),
    ] = None,
):
    """
    Create a new job in Cronicle. Defaults to on-demand if no schedule is provided.
    """
    typer.echo(f"Creating job '{name}' to run script '{script_path}'")

    if not CRONICLE_API_KEY:
        typer.secho(
            "Error: CRONICLE_API_KEY environment variable must be set.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    headers = {"X-Api-Key": CRONICLE_API_KEY}

    category_id = category_id_map[category]
    plugin_id = plugin_id_map[plugin]

    payload = {
        "title": name,
        "category": category_id,
        "plugin": plugin_id,
        "target": target_group,
        "params": {"script": script_path},
        "enabled": 1,
    }

    timing = {}
    if hours:
        try:
            timing["hours"] = [int(h.strip()) for h in hours.split(",")]
        except ValueError:
            typer.secho(
                "Error: --hours must be a comma-separated list of numbers.",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)

    if minutes:
        try:
            timing["minutes"] = [int(m.strip()) for m in minutes.split(",")]
        except ValueError:
            typer.secho(
                "Error: --minutes must be a comma-separated list of numbers.",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)

    if timing:
        payload["timing"] = timing

    try:
        response = requests.post(
            f"{CRONICLE_URL}/api/app/create_event/v1", headers=headers, json=payload
        )
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        if data.get("code") == 0:
            typer.secho(
                f"Successfully created job. Event ID: {data['id']}",
                fg=typer.colors.GREEN,
            )
        else:
            typer.secho(
                f"Error creating job: {data.get('description', 'Unknown error')}",
                fg=typer.colors.RED,
            )

    except requests.exceptions.RequestException as e:
        typer.secho(f"API request failed: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

#!/usr/bin/env python3
"""
Cronicle Manager CLI - Typer-based tool for managing Cronicle jobs.

This CLI allows you to:
- Create new scheduled jobs in Cronicle
- List existing jobs
- Run jobs immediately
- Delete jobs
- Check job status
"""

import typer
import os
import json
from typing import Optional
from typing_extensions import Annotated
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from .cronicle_client import CronicleClient

app = typer.Typer(help="Cronicle Job Manager - Schedule and manage jobs via Cronicle API")
console = Console()

# Load environment variables
env_path = Path.home() / ".env"
if env_path.exists():
    load_dotenv(env_path)

CRONICLE_URL = os.environ.get("CRONICLE_URL", "http://localhost:3012")
CRONICLE_API_KEY = os.environ.get("CRONICLE_API_KEY")


def get_plugin_id() -> str:
    """Get the custom plugin ID, prompting user if not found."""
    plugin_id_file = Path(__file__).parent.parent / ".plugin_id"

    if plugin_id_file.exists():
        plugin_id = plugin_id_file.read_text().strip()
        console.log(f"Using plugin ID: {plugin_id}")
        return plugin_id

    # Plugin ID file missing - prompt user
    console.print("[yellow]⚠️  Plugin ID file not found![/yellow]")
    console.print("")
    console.print("📋 To find your plugin ID:")
    console.print("1. Open Cronicle web interface")
    console.print("2. Go to Admin > Plugins")
    console.print("3. Find your 'Generic Job Executor' plugin")
    console.print("4. Copy the Plugin ID (e.g., 'pmc6gxqss0t')")
    console.print("")
    console.print("🔧 If plugin is missing, install it using:")
    plugin_config_path = Path(__file__).parent.parent / "plugin" / "plugin_config.pixl"
    console.print(f"   cat {plugin_config_path}")
    console.print("   # Copy the JSON content to Cronicle Admin > Plugins > Add Plugin")
    console.print("")

    plugin_id = typer.prompt("Enter your plugin ID")

    # Save for future use
    plugin_id_file.write_text(plugin_id)
    console.print(f"[green]✅ Plugin ID saved to {plugin_id_file}[/green]")

    return plugin_id


def get_client() -> CronicleClient:
    """Get configured Cronicle client."""
    if not CRONICLE_API_KEY:
        console.print("[red]Error: CRONICLE_API_KEY environment variable must be set.[/red]")
        raise typer.Exit(1)
    
    return CronicleClient(CRONICLE_URL, CRONICLE_API_KEY)


@app.command("create")
def create_job(
    name: Annotated[str, typer.Argument(help="Job name/title")],
    executable: Annotated[str, typer.Argument(help="Path to executable")],
    category: Annotated[str, typer.Option(help="Job category")] = "general",
    target: Annotated[str, typer.Option(help="Target server/group")] = "all_servers",
    hours: Annotated[Optional[str], typer.Option(help="Comma-separated hours (0-23)")] = None,
    minutes: Annotated[Optional[str], typer.Option(help="Comma-separated minutes (0-59)")] = None,
    weekdays: Annotated[Optional[str], typer.Option(help="Comma-separated weekdays (1-7)")] = None,
    env_file: Annotated[Optional[str], typer.Option(help="Path to .env file")] = None,
    kwargs: Annotated[Optional[str], typer.Option(help="JSON kwargs for executable")] = None,
    enabled: Annotated[bool, typer.Option(help="Enable job immediately")] = True
):
    """Create a new scheduled job in Cronicle."""
    
    client = get_client()
    
    # Parse timing
    timing = {}
    if hours:
        try:
            timing["hours"] = [int(h.strip()) for h in hours.split(",")]
        except ValueError:
            console.print("[red]Error: --hours must be comma-separated numbers[/red]")
            raise typer.Exit(1)
    
    if minutes:
        try:
            timing["minutes"] = [int(m.strip()) for m in minutes.split(",")]
        except ValueError:
            console.print("[red]Error: --minutes must be comma-separated numbers[/red]")
            raise typer.Exit(1)
    
    if weekdays:
        try:
            timing["weekdays"] = [int(w.strip()) for w in weekdays.split(",")]
        except ValueError:
            console.print("[red]Error: --weekdays must be comma-separated numbers[/red]")
            raise typer.Exit(1)
    
    # Parse kwargs
    parsed_kwargs = None
    if kwargs:
        try:
            parsed_kwargs = json.loads(kwargs)
        except json.JSONDecodeError:
            console.print("[red]Error: --kwargs must be valid JSON[/red]")
            raise typer.Exit(1)
    
    try:
        # Get plugin ID
        plugin_id = get_plugin_id()
        
        response = client.create_event(
            title=name,
            executable=executable,
            plugin=plugin_id,
            category=category,
            target=target,
            timing=timing if timing else None,
            env_file=env_file,
            kwargs=parsed_kwargs,
            enabled=enabled
        )
        
        if response.get("code") == 0:
            console.print(f"[green]Successfully created job. Event ID: {response['id']}[/green]")
        else:
            console.print(f"[red]Error: {response.get('description', 'Unknown error')}[/red]")
            
    except Exception as e:
        console.print(f"[red]API request failed: {e}[/red]")
        raise typer.Exit(1)


@app.command("list")
def list_jobs():
    """List all scheduled jobs."""
    client = get_client()
    
    try:
        response = client.get_schedule()
        
        if response.get("code") == 0:
            events = response.get("rows", [])
            
            if not events:
                console.print("No scheduled jobs found.")
                return
            
            table = Table(title="Scheduled Jobs")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="magenta")
            table.add_column("Plugin", style="green")
            table.add_column("Target", style="yellow")
            table.add_column("Enabled", style="blue")
            
            for event in events:
                table.add_row(
                    event.get("id", ""),
                    event.get("title", ""),
                    event.get("plugin", ""),
                    event.get("target", ""),
                    "Yes" if event.get("enabled") else "No"
                )
            
            console.print(table)
        else:
            console.print(f"[red]Error: {response.get('description', 'Unknown error')}[/red]")
            
    except Exception as e:
        console.print(f"[red]API request failed: {e}[/red]")
        raise typer.Exit(1)


@app.command("run")
def run_job(
    event_id: Annotated[str, typer.Argument(help="Event ID to run")]
):
    """Run a job immediately."""
    client = get_client()
    
    try:
        response = client.run_event(event_id)
        
        if response.get("code") == 0:
            job_id = response.get("id", "")
            console.print(f"[green]Job started successfully. Job ID: {job_id}[/green]")
        else:
            console.print(f"[red]Error: {response.get('description', 'Unknown error')}[/red]")
            
    except Exception as e:
        console.print(f"[red]API request failed: {e}[/red]")
        raise typer.Exit(1)


@app.command("delete")
def delete_job(
    event_id: Annotated[str, typer.Argument(help="Event ID to delete")],
    force: Annotated[bool, typer.Option(help="Skip confirmation")] = False
):
    """Delete a scheduled job."""
    if not force:
        confirm = typer.confirm(f"Delete job {event_id}?")
        if not confirm:
            console.print("Cancelled")
            return
    
    client = get_client()
    
    try:
        response = client.delete_event(event_id)
        
        if response.get("code") == 0:
            console.print(f"[green]Successfully deleted job {event_id}[/green]")
        else:
            console.print(f"[red]Error: {response.get('description', 'Unknown error')}[/red]")
            
    except Exception as e:
        console.print(f"[red]API request failed: {e}[/red]")
        raise typer.Exit(1)


@app.command("status")
def job_status(
    job_id: Annotated[str, typer.Argument(help="Job ID to check")]
):
    """Check status of a running job."""
    client = get_client()
    
    try:
        response = client.get_job_status(job_id)
        
        if response.get("code") == 0:
            job = response.get("job", {})
            console.print(f"Job ID: {job_id}")
            console.print(f"Status: {job.get('complete', 'Running')}")
            console.print(f"Progress: {job.get('progress', 0)}%")
            if job.get("log_file"):
                console.print(f"Log file: {job.get('log_file')}")
        else:
            console.print(f"[red]Error: {response.get('description', 'Unknown error')}[/red]")
            
    except Exception as e:
        console.print(f"[red]API request failed: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
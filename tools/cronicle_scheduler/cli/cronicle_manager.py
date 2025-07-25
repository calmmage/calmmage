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
import random
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


def generate_job_name_from_path(script_path: str) -> str:
    """
    Generate a job name from script path using AI (placeholder for now).
    
    TODO: Implement AI-powered name generation based on script content/path.
    For now, converts filename to Title Case.
    """
    try:
        # For now: simple Title Case conversion from filename
        filename = Path(script_path).stem
        # Convert underscores/hyphens to spaces and title case
        name = filename.replace("_", " ").replace("-", " ").title()
        return name
    except Exception:
        return "Auto Generated Job"


def parse_schedule_keyword(schedule: str) -> dict:
    """
    Parse schedule keywords into timing parameters.
    
    TODO: Implement AI-powered natural language schedule parsing.
    For now, supports basic keywords and cron-like expressions.
    """
    schedule = schedule.lower().strip()
    
    # Basic keyword mappings
    keyword_mappings = {
        "minutely": {"minutes": list(range(60))},  # Every minute
        "hourly": {"minutes": [0]},  # Top of every hour
        "daily": {"hours": [random.randint(8, 20)], "minutes": [random.randint(0, 59)]},  # Random time 8-20
        "weekly": {"weekdays": [1], "hours": [random.randint(8, 20)], "minutes": [random.randint(0, 59)]},  # Monday
        "monthly": {"days": [1], "hours": [random.randint(8, 20)], "minutes": [random.randint(0, 59)]},  # 1st of month
        "quarterly": {"months": [1, 4, 7, 10], "days": [1], "hours": [random.randint(8, 20)]},  # Quarters
        "yearly": {"months": [1], "days": [1], "hours": [random.randint(8, 20)]}  # New Year
    }
    
    if schedule in keyword_mappings:
        return keyword_mappings[schedule]
    
    # TODO: Add AI-powered parsing for complex expressions like:
    # - "every weekday at 9am"
    # - "twice a week"
    # - "monthly on the 15th"
    # - "every other day"
    
    # For now, if not a keyword, assume it's a cron expression or return daily default
    console.print(f"[yellow]⚠️  Schedule '{schedule}' not recognized, using 'daily' default[/yellow]")
    return keyword_mappings["daily"]


@app.command("create")
def create_job(
    name: Annotated[Optional[str], typer.Argument(help="Job name/title")] = None,
    executable: Annotated[Optional[str], typer.Argument(help="Path to executable")] = None,
    schedule: Annotated[Optional[str], typer.Option(help="Schedule (daily/hourly/weekly/monthly/minutely/yearly/quarterly or cron)")] = None,
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
    
    # Interactive prompts for missing parameters
    
    # 1. Handle executable path (script path)
    if not executable:
        executable = typer.prompt("📄 Enter script path")
    
    # Convert relative path to absolute
    executable_path = Path(executable)
    if not executable_path.is_absolute():
        executable_path = Path.cwd() / executable_path
    executable = str(executable_path.resolve())
    
    # Validate script exists
    if not Path(executable).exists():
        console.print(f"[red]Error: Script not found: {executable}[/red]")
        raise typer.Exit(1)
    
    # 2. Handle job name
    if not name:
        suggested_name = generate_job_name_from_path(executable)
        name = typer.prompt(f"📝 Enter job name", default=suggested_name)
    
    # 3. Handle schedule
    if not schedule and not hours and not minutes and not weekdays:
        console.print("\n⏰ [bold]Schedule Options:[/bold]")
        console.print("   • [cyan]daily[/cyan] - Random time between 8-20")
        console.print("   • [cyan]hourly[/cyan] - Top of every hour")
        console.print("   • [cyan]weekly[/cyan] - Monday random time")
        console.print("   • [cyan]monthly[/cyan] - 1st of month")
        console.print("   • [cyan]minutely[/cyan] - Every minute")
        console.print("   • [cyan]yearly[/cyan] - New Year's Day")
        console.print("   • [cyan]quarterly[/cyan] - Start of quarters")
        console.print("")
        schedule = typer.prompt("📅 Enter schedule", default="daily")
    
    # Parse timing
    timing = {}
    
    # If schedule keyword provided, parse it
    if schedule:
        timing = parse_schedule_keyword(schedule)
        console.print(f"[green]✅ Using schedule: {schedule}[/green]")
        if "hours" in timing:
            console.print(f"   Hours: {timing['hours']}")
        if "minutes" in timing:
            console.print(f"   Minutes: {timing['minutes']}")
        if "weekdays" in timing:
            console.print(f"   Weekdays: {timing['weekdays']}")
    
    # Override with explicit timing parameters if provided (takes precedence over schedule keywords)
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
        
        # Show summary before creating
        console.print(f"\n📋 [bold]Job Summary:[/bold]")
        console.print(f"   Name: [cyan]{name}[/cyan]")
        console.print(f"   Script: [yellow]{executable}[/yellow]")
        if timing:
            console.print(f"   Schedule: [green]{timing}[/green]")
        console.print(f"   Plugin: [magenta]{plugin_id}[/magenta]")
        console.print("")
        
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
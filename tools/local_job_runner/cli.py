#!/usr/bin/env python3
"""
Local Job Runner CLI - Typer-based interface for running local jobs.

This CLI provides commands to:
- Run all jobs in a directory
- Run specific jobs
- List available jobs
- View job logs
"""

import typer
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table
import json
from datetime import datetime
from src.lib.utils import get_scheduled_tasks_dir

from tools.local_job_runner.job_runner import (
    LocalJobRunner,
    JobOutcome,
    JOB_TIMEOUT_SECONDS,
    get_python_executable,
)

app = typer.Typer(help="Local Job Runner - Execute and manage local jobs")
console = Console()

DEFAULT_JOBS_DIR = get_scheduled_tasks_dir()
DEFAULT_LOG_DIR = Path.home() / "Library" / "Logs" / "CalmmageScheduler"


@app.command("run")
def run_jobs(
    jobs_dir: Annotated[Path, typer.Option(help="Directory containing jobs")] = DEFAULT_JOBS_DIR,
    log_dir: Annotated[Optional[Path], typer.Option(help="Log directory")] = None,
    job_pattern: Annotated[Optional[str], typer.Option(help="Run only jobs matching pattern")] = None,
    include_disabled: Annotated[bool, typer.Option("--include-disabled", help="Include disabled jobs (starting with '_')")] = False,
    live: Annotated[bool, typer.Option("--live", help="Show live progress updates during execution")] = False
):
    """Run all jobs in the specified directory."""
    
    if not jobs_dir.exists():
        console.print(f"[red]Jobs directory does not exist: {jobs_dir}[/red]")
        raise typer.Exit(1)
    
    runner = LocalJobRunner(jobs_dir, log_dir)
    
    console.print("🚀 Starting job runner...")
    console.print(f"📁 Jobs directory: {jobs_dir}")
    console.print(f"📝 Log directory: {runner.log_dir}")
    console.print(f"⏰ Job timeout: {JOB_TIMEOUT_SECONDS // 60} minutes ({JOB_TIMEOUT_SECONDS} seconds)")
    console.print(f"🐍 Python executable: {get_python_executable()}")
    console.print()
    
    # Find jobs with disabled flag
    if job_pattern:
        all_jobs = runner.find_jobs(include_disabled=include_disabled)
        filtered_jobs = [job for job in all_jobs if job_pattern in job.name]
        if not filtered_jobs:
            console.print(f"[yellow]No jobs found matching pattern: {job_pattern}[/yellow]")
            return
        console.print(f"Running {len(filtered_jobs)} jobs matching '{job_pattern}'")
        # TODO: Implement pattern filtering in job_runner
    else:
        # Set the include_disabled flag for the runner
        runner._include_disabled = include_disabled
    
    # Run all jobs with live updates if requested
    runner.run_all_jobs(live_updates=live)
    
    # Save logs
    log_file = runner.save_logs()
    console.print(f"\n📄 Detailed logs saved to: {log_file}")
    
    # Print Rich table summary
    runner.print_summary()


@app.command("list")
def list_jobs(
    jobs_dir: Annotated[Path, typer.Option(help="Directory containing jobs")] = DEFAULT_JOBS_DIR,
    include_disabled: Annotated[bool, typer.Option("--include-disabled", help="Include disabled jobs (starting with '_')")] = False
):
    """List all available jobs."""
    
    if not jobs_dir.exists():
        console.print(f"[red]Jobs directory does not exist: {jobs_dir}[/red]")
        raise typer.Exit(1)
    
    runner = LocalJobRunner(jobs_dir)
    jobs = runner.find_jobs(include_disabled=include_disabled)
    
    if not jobs:
        console.print("No jobs found")
        return
    
    table = Table(title=f"Available Jobs in {jobs_dir}")
    table.add_column("Job Name", style="cyan")
    table.add_column("Status", style="white", justify="center")
    table.add_column("File Path", style="magenta")
    table.add_column("Size", style="green")
    table.add_column("Modified", style="yellow")
    
    for job_path in jobs:
        stat = job_path.stat()
        size = f"{stat.st_size} bytes"
        modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
        
        # Determine job status
        if job_path.name.startswith("_"):
            status = "[red]🔴 DISABLED[/red]"
            job_name_style = "[dim]" + job_path.stem + "[/dim]"
        else:
            status = "[green]🟢 ENABLED[/green]"
            job_name_style = job_path.stem
        
        table.add_row(
            job_name_style,
            status,
            str(job_path.relative_to(jobs_dir)),
            size,
            modified
        )
    
    console.print(table)


@app.command("logs")
def view_logs(
    log_dir: Annotated[Path, typer.Option(help="Log directory")] = DEFAULT_LOG_DIR,
    latest: Annotated[bool, typer.Option(help="Show only latest run")] = True,
    count: Annotated[int, typer.Option(help="Number of recent runs to show")] = 5
):
    """View job execution logs."""
    
    if not log_dir.exists():
        console.print(f"[red]Log directory does not exist: {log_dir}[/red]")
        raise typer.Exit(1)
    
    # Find log files
    log_files = sorted(log_dir.glob("job_run_*.json"), reverse=True)
    
    if not log_files:
        console.print("No log files found")
        return
    
    if latest:
        log_files = log_files[:1]
    else:
        log_files = log_files[:count]
    
    for log_file in log_files:
        try:
            with open(log_file) as f:
                log_data = json.load(f)
            
            console.print(f"\n📋 Run: {log_data['run_timestamp']}")
            console.print(f"📁 Jobs directory: {log_data['jobs_directory']}")
            console.print(f"🔢 Total jobs: {log_data['total_jobs']}")
            
            if log_data.get('results'):
                table = Table()
                table.add_column("Job", style="cyan")
                table.add_column("Outcome", style="magenta")
                table.add_column("Duration", style="green")
                table.add_column("Summary", style="yellow")
                
                for result in log_data['results']:
                    outcome_emoji = {
                        "ok": "✅",
                        "fail": "❌", 
                        "warning": "⚠️",
                        "done_nothing": "⚪"
                    }
                    
                    table.add_row(
                        result['job_name'],
                        f"{outcome_emoji.get(result['outcome'], '?')} {result['outcome']}",
                        f"{result['duration_seconds']:.1f}s",
                        result['summary'][:50] + "..." if len(result['summary']) > 50 else result['summary']
                    )
                
                console.print(table)
            
        except (json.JSONDecodeError, KeyError) as e:
            console.print(f"[red]Error reading log file {log_file}: {e}[/red]")


@app.command("test")
def test_job(
    job_name: Annotated[str, typer.Argument(help="Name of job to test")],
    jobs_dir: Annotated[Path, typer.Option(help="Directory containing jobs")] = DEFAULT_JOBS_DIR
):
    """Test run a specific job."""
    
    if not jobs_dir.exists():
        console.print(f"[red]Jobs directory does not exist: {jobs_dir}[/red]")
        raise typer.Exit(1)
    
    # Find the job
    job_path = None
    for potential_job in jobs_dir.rglob("*.py"):
        if potential_job.stem == job_name:
            job_path = potential_job
            break
    
    if not job_path:
        console.print(f"[red]Job '{job_name}' not found in {jobs_dir}[/red]")
        raise typer.Exit(1)
    
    console.print(f"🧪 Testing job: {job_name}")
    console.print(f"📄 Path: {job_path}")
    
    runner = LocalJobRunner(jobs_dir)
    result = runner.execute_job(job_path)
    
    # Display result
    outcome_emoji = {
        JobOutcome.OK: "✅",
        JobOutcome.FAIL: "❌",
        JobOutcome.WARNING: "⚠️", 
        JobOutcome.DONE_NOTHING: "⚪"
    }
    
    console.print(f"\n{outcome_emoji.get(result.outcome, '?')} Result: {result.outcome.value}")
    console.print(f"⏱️  Duration: {result.duration_seconds:.1f}s")
    console.print(f"🔢 Exit code: {result.exit_code}")
    console.print(f"📝 Summary: {result.summary}")
    
    if result.stdout:
        console.print(f"\n📤 STDOUT:\n{result.stdout}")
    
    if result.stderr:
        console.print(f"\n📥 STDERR:\n{result.stderr}")


if __name__ == "__main__":
    app()
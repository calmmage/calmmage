#!/usr/bin/env python3
"""
Local Job Runner - Scans and executes all jobs in a directory.

This script:
1. Scans all Python files in the jobs directory
2. Executes each job
3. Captures output and generates AI-powered summaries
4. Logs results to ~/Library/Logs/CalmmageScheduler/
5. Compiles a final summary report

Usage:
    python job_runner.py --jobs-dir /path/to/jobs
    python job_runner.py  # Uses default jobs directory
"""

import sys
import subprocess
import json
import time
import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from enum import Enum
import argparse
from dataclasses import dataclass, asdict
from src.lib.utils import get_scheduled_tasks_dir

# Job execution configuration
JOB_TIMEOUT_SECONDS = 300  # 5 minutes

def get_python_executable() -> str:
    """Get the Python executable to use for running jobs."""
    calmmage_venv = os.getenv('CALMMAGE_VENV_PATH')
    if calmmage_venv:
        python_path = Path(calmmage_venv) / "bin" / "python"
        if python_path.exists():
            return str(python_path)
        else:
            print(f"⚠️  Warning: CALMMAGE_VENV_PATH set but {python_path} not found, using current Python")
    else:
        print("⚠️  Warning: CALMMAGE_VENV_PATH not set, using current Python interpreter")
    
    return sys.executable

# For AI-powered summaries (using calmlib utilities)
try:
    from calmlib.llm import query_llm_text, query_llm_structured
    from pydantic import BaseModel
    HAS_LLM = True
except ImportError as e:
    print(f"⚠️  Warning: LLM utilities not available: {e}")
    print("   AI summaries will be disabled, using fallback text summaries")
    HAS_LLM = False
    BaseModel = None


class JobOutcome(Enum):
    """Job execution outcomes."""
    OK = "ok"
    FAIL = "fail"
    WARNING = "warning"
    DONE_NOTHING = "done_nothing"


if HAS_LLM:
    class JobAnalysis(BaseModel):
        """Structured AI analysis of job execution."""
        outcome_assessment: str  # One of: "ok", "fail", "warning", "done_nothing"
        did_meaningful_work: bool  # True if job performed actual changes/work
        summary: str  # 1-2 sentence summary of what happened
        key_indicators: List[str]  # List of key output indicators that led to this assessment
        
        class Config:
            extra = "forbid"
else:
    # Fallback when LLM not available
    JobAnalysis = None


@dataclass
class JobResult:
    """Result of a job execution."""
    job_name: str
    job_path: str
    outcome: JobOutcome
    exit_code: int
    duration_seconds: float
    stdout: str
    stderr: str
    summary: str
    timestamp: str


class LocalJobRunner:
    """Runs all jobs in a directory and tracks results."""
    
    def __init__(self, jobs_dir: Path, log_dir: Optional[Path] = None):
        self.jobs_dir = Path(jobs_dir)
        self.log_dir = log_dir or Path.home() / "Library" / "Logs" / "CalmmageScheduler"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.results: List[JobResult] = []
        
        # Initialize LLM for summaries if available
        self.llm = None
        if HAS_LLM:
            try:
                self.llm = LLMWrapper()
            except Exception as e:
                print(f"Warning: Could not initialize LLM for summaries: {e}")
    
    def find_jobs(self) -> List[Path]:
        """Find all Python files in the jobs directory."""
        if not self.jobs_dir.exists():
            print(f"Jobs directory does not exist: {self.jobs_dir}")
            return []
        
        jobs = []
        for file_path in self.jobs_dir.rglob("*.py"):
            if file_path.name.startswith("_"):  # Skip private files
                continue
            jobs.append(file_path)
        
        return sorted(jobs)
    
    async def execute_job_async(self, job_path: Path) -> JobResult:
        """Execute a single job and capture results."""
        job_name = job_path.stem
        start_time = time.time()
        timestamp = datetime.now().isoformat()
        
        print(f"Running job: {job_name}")
        
        try:
            # Use absolute path to avoid path resolution issues
            absolute_job_path = job_path.resolve()
            python_executable = get_python_executable()
            
            # Create subprocess asynchronously with timeout
            process = await asyncio.create_subprocess_exec(
                python_executable, str(absolute_job_path),
                cwd=Path.cwd(),  # Run from the main project directory
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Wait for completion with timeout
            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    process.communicate(), timeout=JOB_TIMEOUT_SECONDS
                )
                exit_code = process.returncode
                stdout = stdout_bytes.decode('utf-8')
                stderr = stderr_bytes.decode('utf-8')
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                raise subprocess.TimeoutExpired(f"Job {job_name}", JOB_TIMEOUT_SECONDS)
            
            duration = time.time() - start_time
            
            # Determine outcome based on exit code and output
            # TODO: This is basic heuristic-based detection. The AI analysis below
            # can provide more sophisticated outcome assessment by analyzing the actual
            # content and meaning of the output, not just simple pattern matching.
            if exit_code == 0:
                if not stdout.strip() and not stderr.strip():
                    outcome = JobOutcome.DONE_NOTHING
                elif "warning" in stdout.lower() or "warning" in stderr.lower():
                    outcome = JobOutcome.WARNING
                else:
                    outcome = JobOutcome.OK
            else:
                outcome = JobOutcome.FAIL
            
            # Generate AI summary if available
            summary = self._generate_summary(job_name, exit_code, stdout, stderr, outcome)
            
            return JobResult(
                job_name=job_name,
                job_path=str(job_path),
                outcome=outcome,
                exit_code=exit_code,
                duration_seconds=duration,
                stdout=stdout,
                stderr=stderr,
                summary=summary,
                timestamp=timestamp
            )
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            summary = f"Job '{job_name}' timed out after {JOB_TIMEOUT_SECONDS // 60} minutes"
            
            return JobResult(
                job_name=job_name,
                job_path=str(job_path),
                outcome=JobOutcome.FAIL,
                exit_code=-1,
                duration_seconds=duration,
                stdout="",
                stderr="Job timed out",
                summary=summary,
                timestamp=timestamp
            )
            
        except Exception as e:
            duration = time.time() - start_time
            summary = f"Job '{job_name}' failed with exception: {str(e)}"
            
            return JobResult(
                job_name=job_name,
                job_path=str(job_path),
                outcome=JobOutcome.FAIL,
                exit_code=-1,
                duration_seconds=duration,
                stdout="",
                stderr=str(e),
                summary=summary,
                timestamp=timestamp
            )
    
    def _generate_summary(self, job_name: str, exit_code: int, stdout: str, stderr: str, outcome: JobOutcome) -> str:
        """Generate AI-powered summary of job execution."""
        if not HAS_LLM:
            # Fallback to simple summary
            if outcome == JobOutcome.OK:
                return f"Job '{job_name}' completed successfully"
            elif outcome == JobOutcome.DONE_NOTHING:
                return f"Job '{job_name}' ran but produced no output"
            elif outcome == JobOutcome.WARNING:
                return f"Job '{job_name}' completed with warnings"
            else:
                return f"Job '{job_name}' failed with exit code {exit_code}"
        
        try:
            # First, try structured analysis for better outcome determination
            analysis_prompt = f"""
            Analyze this job execution output and provide structured assessment:
            
            Job Name: {job_name}
            Exit Code: {exit_code}
            Initial Outcome Assessment: {outcome.value}
            
            STDOUT:
            {stdout[:2000] if stdout else "(no output)"}
            
            STDERR:  
            {stderr[:1000] if stderr else "(no errors)"}
            
            Analyze the output and determine:
            1. What was the actual outcome (ok/fail/warning/done_nothing)?
            2. Did the job perform meaningful work or just run without changes?
            3. What are the key indicators in the output that led to this assessment?
            4. Provide a concise 1-2 sentence summary.
            
            Consider:
            - Jobs that only print greetings or basic info likely "done_nothing"
            - Jobs that generate statistics, reports, or analysis did meaningful work
            - Jobs that fail with errors should be marked as "fail"
            - Jobs with warnings but successful completion should be "warning"
            """
            
            try:
                if JobAnalysis is None:
                    raise Exception("JobAnalysis model not available")
                    
                analysis = query_llm_structured(
                    analysis_prompt,
                    JobAnalysis,
                    system_message="You are analyzing job execution outputs to categorize their success and meaningfulness.",
                    model="claude-3.5",  # Use faster model for analysis
                    max_tokens=300
                )
                
                # Update outcome if AI suggests different assessment
                if analysis.outcome_assessment != outcome.value:
                    print(f"  🤖 AI revised outcome: {outcome.value} → {analysis.outcome_assessment}")
                    # TODO: Consider updating the actual outcome in JobResult
                
                # Return AI-generated summary with meaningfulness indicator
                meaning_indicator = "🔄" if analysis.did_meaningful_work else "⚪"
                return f"{meaning_indicator} {analysis.summary}"
                
            except Exception as e:
                print(f"  ⚠️  Structured analysis failed ({e}), falling back to text generation")
                
                # Fallback to simple text generation
                simple_prompt = f"""
                Briefly summarize what this job did in 1-2 sentences:
                
                Job: {job_name}
                Exit Code: {exit_code}
                Output: {stdout[:500] if stdout else '(no output)'}
                Errors: {stderr[:300] if stderr else '(no errors)'}
                """
                
                response = query_llm_text(
                    simple_prompt,
                    system_message="Provide a concise job execution summary.",
                    max_tokens=100
                )
                return response.strip()
            
        except Exception as e:
            print(f"  ⚠️  AI summary generation failed: {e}")
            # Final fallback to simple summary
            return f"Job '{job_name}' finished with outcome: {outcome.value}"
    
    def print_live_results_table(self, total_jobs: int) -> None:
        """Print a live-updating table of completed jobs."""
        if not self.results:
            return
            
        # Import Rich for live table display
        from rich.console import Console
        from rich.table import Table
        from rich.live import Live
        
        console = Console()
        
        # Create table
        table = Table(title=f"Job Execution Progress ({len(self.results)}/{total_jobs} completed)")
        table.add_column("Job Name", style="cyan", no_wrap=True)
        table.add_column("Status", justify="center")
        table.add_column("Duration", justify="right", style="green")
        table.add_column("Summary", style="white")
        
        # Add completed jobs to table
        for result in self.results:
            # Status with emoji and color
            status_info = {
                JobOutcome.OK: ("✅ OK", "green"),
                JobOutcome.FAIL: ("❌ FAIL", "red"),
                JobOutcome.WARNING: ("⚠️  WARN", "yellow"),
                JobOutcome.DONE_NOTHING: ("⚪ NOTHING", "dim")
            }
            
            status_text, status_color = status_info.get(result.outcome, ("? UNKNOWN", "white"))
            
            # Truncate summary if too long
            summary = result.summary
            if len(summary) > 60:
                summary = summary[:57] + "..."
            
            table.add_row(
                result.job_name,
                f"[{status_color}]{status_text}[/{status_color}]",
                f"{result.duration_seconds:.1f}s",
                summary
            )
        
        # Show still-running jobs
        completed_names = {r.job_name for r in self.results}
        running_count = total_jobs - len(self.results)
        if running_count > 0:
            table.add_row(
                f"[yellow]{running_count} jobs still running...[/yellow]",
                "[yellow]🔄 RUNNING[/yellow]",
                "[yellow]...[/yellow]",
                "[yellow]In progress...[/yellow]"
            )
        
        # Clear screen and print table
        console.clear()
        console.print(table)

    async def run_all_jobs_async(self) -> None:
        """Run all jobs concurrently with live progress updates."""
        jobs = self.find_jobs()
        
        if not jobs:
            print("No jobs found to run")
            return
        
        print(f"Found {len(jobs)} jobs to run")
        print("Running jobs concurrently with live updates...")
        print(f"⏰ Job timeout: {JOB_TIMEOUT_SECONDS // 60} minutes ({JOB_TIMEOUT_SECONDS} seconds)")
        print(f"🐍 Python executable: {get_python_executable()}")
        print("(Press Ctrl+C to stop)\n")
        
        # Start all jobs concurrently
        tasks = {asyncio.create_task(self.execute_job_async(job_path)): job_path 
                for job_path in jobs}
        
        # Poll for completion with live updates
        while tasks:
            # Wait for at least one task to complete (with timeout for updates)
            done, pending = await asyncio.wait(
                tasks.keys(), 
                return_when=asyncio.FIRST_COMPLETED,
                timeout=2.0  # Update display every 2 seconds
            )
            
            # Process completed tasks
            for task in done:
                job_path = tasks[task]
                try:
                    result = await task
                except Exception as e:
                    # Create failure result for exceptions
                    job_name = job_path.stem
                    result = JobResult(
                        job_name=job_name,
                        job_path=str(job_path),
                        outcome=JobOutcome.FAIL,
                        exit_code=-1,
                        duration_seconds=0.0,
                        stdout="",
                        stderr=str(e),
                        summary=f"Job '{job_name}' failed with exception: {str(e)}",
                        timestamp=datetime.now().isoformat()
                    )
                
                self.results.append(result)
                del tasks[task]
            
            # Update display with current results
            self.print_live_results_table(len(jobs))
        
        # Final status update
        print(f"\n🎉 All {len(jobs)} jobs completed!")
        
        # Print simple final status for each job
        status_color = {
            JobOutcome.OK: "✅",
            JobOutcome.DONE_NOTHING: "⚪",
            JobOutcome.WARNING: "⚠️",
            JobOutcome.FAIL: "❌"
        }
        
        print("\nFinal Results:")
        for result in self.results:
            print(f"  {status_color.get(result.outcome, '?')} {result.job_name} "
                  f"({result.duration_seconds:.1f}s) - {result.summary}")
    
    def execute_job(self, job_path: Path) -> JobResult:
        """Synchronous wrapper for single job execution (used by CLI test command)."""
        return asyncio.run(self.execute_job_async(job_path))
    
    def run_all_jobs(self) -> None:
        """Synchronous wrapper for async job execution."""
        asyncio.run(self.run_all_jobs_async())
    
    def save_logs(self) -> Path:
        """Save detailed logs to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"job_run_{timestamp}.json"
        
        # Convert results to dict for JSON serialization
        def serialize_result(result):
            result_dict = asdict(result)
            result_dict["outcome"] = result.outcome.value  # Convert enum to string
            return result_dict
            
        log_data = {
            "run_timestamp": timestamp,
            "jobs_directory": str(self.jobs_dir),
            "total_jobs": len(self.results),
            "results": [serialize_result(result) for result in self.results]
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        return log_file
    
    def print_summary(self) -> None:
        """Print final summary report using Rich tables."""
        if not self.results:
            print("No jobs were executed")
            return

        # Import Rich - let it fail if not available
        from rich.console import Console
        from rich.table import Table
        console = Console()
        
        console.print("\n[bold blue]JOB EXECUTION SUMMARY[/bold blue]")
        
        # Create main results table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Job Name", style="cyan", no_wrap=True)
        table.add_column("Status", justify="center")
        table.add_column("Duration", justify="right", style="green")
        table.add_column("Summary", style="white")
        
        # Count outcomes and total duration
        outcome_counts = {outcome: 0 for outcome in JobOutcome}
        total_duration = 0
        
        for result in self.results:
            outcome_counts[result.outcome] += 1
            total_duration += result.duration_seconds
            
            # Status with emoji and color
            status_info = {
                JobOutcome.OK: ("✅ OK", "green"),
                JobOutcome.FAIL: ("❌ FAIL", "red"),
                JobOutcome.WARNING: ("⚠️  WARN", "yellow"),
                JobOutcome.DONE_NOTHING: ("⚪ NOTHING", "dim")
            }
            
            status_text, status_color = status_info.get(result.outcome, ("? UNKNOWN", "white"))
            
            # Truncate summary if too long
            summary = result.summary
            if len(summary) > 60:
                summary = summary[:57] + "..."
            
            table.add_row(
                result.job_name,
                f"[{status_color}]{status_text}[/{status_color}]",
                f"{result.duration_seconds:.1f}s",
                summary
            )
        
        console.print(table)
        
        # Print summary statistics
        stats_table = Table(show_header=False, box=None, padding=(0, 1))
        stats_table.add_column("Metric", style="bold")
        stats_table.add_column("Value", style="cyan")
        
        stats_table.add_row("Total Jobs:", str(len(self.results)))
        stats_table.add_row("Total Duration:", f"{total_duration:.1f}s")
        
        for outcome, count in outcome_counts.items():
            if count > 0:
                emoji = {"ok": "✅", "fail": "❌", "warning": "⚠️", "done_nothing": "⚪"}
                stats_table.add_row(f"{emoji.get(outcome.value, '?')} {outcome.value.title()}:", str(count))
        
        console.print("\n[bold]Statistics:[/bold]")
        console.print(stats_table)
        
        # Show errors for failed jobs
        failed_jobs = [r for r in self.results if r.outcome == JobOutcome.FAIL]
        if failed_jobs:
            console.print("\n[bold red]Failed Job Details:[/bold red]")
            for result in failed_jobs:
                if result.stderr:
                    error_msg = result.stderr[:200] + "..." if len(result.stderr) > 200 else result.stderr
                    console.print(f"[red]• {result.job_name}:[/red] {error_msg}")
    
    def _print_simple_summary(self) -> None:
        """Fallback summary printing without Rich."""
        print("\n" + "="*60)
        print("JOB EXECUTION SUMMARY")
        print("="*60)
        
        # Count outcomes
        outcome_counts = {outcome: 0 for outcome in JobOutcome}
        total_duration = 0
        
        for result in self.results:
            outcome_counts[result.outcome] += 1
            total_duration += result.duration_seconds
        
        print(f"Total jobs: {len(self.results)}")
        print(f"Total duration: {total_duration:.1f}s")
        print()
        
        for outcome, count in outcome_counts.items():
            if count > 0:
                emoji = {"ok": "✅", "fail": "❌", "warning": "⚠️", "done_nothing": "⚪"}
                print(f"{emoji.get(outcome.value, '?')} {outcome.value.upper()}: {count}")
        
        print("\nDetailed Results:")
        print("-" * 40)
        
        for result in self.results:
            print(f"{result.job_name}: {result.summary}")
            if result.outcome == JobOutcome.FAIL and result.stderr:
                print(f"  Error: {result.stderr[:100]}...")


def main():
    parser = argparse.ArgumentParser(description="Local Job Runner")
    parser.add_argument(
        "--jobs-dir",
        type=Path,
        help="Directory containing jobs to run",
        default=get_scheduled_tasks_dir()
    )
    parser.add_argument(
        "--log-dir",
        type=Path,
        help="Directory to store logs",
        default=None
    )
    
    args = parser.parse_args()
    
    runner = LocalJobRunner(args.jobs_dir, args.log_dir)
    
    print("Starting job runner...")
    print(f"📁 Jobs directory: {runner.jobs_dir}")
    print(f"📝 Log directory: {runner.log_dir}")
    print(f"⏰ Job timeout: {JOB_TIMEOUT_SECONDS // 60} minutes ({JOB_TIMEOUT_SECONDS} seconds)")
    print(f"🐍 Python executable: {get_python_executable()}")
    print()
    
    # Run all jobs
    runner.run_all_jobs()
    
    # Save logs
    log_file = runner.save_logs()
    print(f"\nDetailed logs saved to: {log_file}")
    
    # Print summary
    runner.print_summary()


if __name__ == "__main__":
    main()
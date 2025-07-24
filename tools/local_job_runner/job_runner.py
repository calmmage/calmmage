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
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from enum import Enum
import argparse
from dataclasses import dataclass, asdict

# For AI-powered summaries (using calmlib if available)
try:
    from calmlib.llm import LLMWrapper
    HAS_LLM = True
except ImportError:
    HAS_LLM = False


class JobOutcome(Enum):
    """Job execution outcomes."""
    OK = "ok"
    FAIL = "fail"
    WARNING = "warning"
    DONE_NOTHING = "done_nothing"


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
    
    def execute_job(self, job_path: Path) -> JobResult:
        """Execute a single job and capture results."""
        job_name = job_path.stem
        start_time = time.time()
        timestamp = datetime.now().isoformat()
        
        print(f"Running job: {job_name}")
        
        try:
            result = subprocess.run(
                [sys.executable, str(job_path)],
                cwd=job_path.parent,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            duration = time.time() - start_time
            exit_code = result.returncode
            stdout = result.stdout
            stderr = result.stderr
            
            # Determine outcome based on exit code and output
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
            summary = f"Job '{job_name}' timed out after 5 minutes"
            
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
        if not self.llm:
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
            prompt = f"""
            Analyze this job execution and provide a concise 1-2 sentence summary:
            
            Job Name: {job_name}
            Exit Code: {exit_code}
            Outcome: {outcome.value}
            
            STDOUT:
            {stdout[:1000] if stdout else "(no output)"}
            
            STDERR:
            {stderr[:1000] if stderr else "(no errors)"}
            
            Please provide a brief, informative summary of what happened.
            """
            
            response = self.llm.call(prompt, max_tokens=100)
            return response.strip()
            
        except Exception as e:
            print(f"Warning: Could not generate AI summary: {e}")
            return f"Job '{job_name}' finished with outcome: {outcome.value}"
    
    def run_all_jobs(self) -> None:
        """Run all jobs and collect results."""
        jobs = self.find_jobs()
        
        if not jobs:
            print("No jobs found to run")
            return
        
        print(f"Found {len(jobs)} jobs to run")
        
        for job_path in jobs:
            result = self.execute_job(job_path)
            self.results.append(result)
            
            # Print immediate feedback
            status_color = {
                JobOutcome.OK: "✅",
                JobOutcome.DONE_NOTHING: "⚪",
                JobOutcome.WARNING: "⚠️",
                JobOutcome.FAIL: "❌"
            }
            
            print(f"  {status_color.get(result.outcome, '?')} {result.job_name} "
                  f"({result.duration_seconds:.1f}s) - {result.summary}")
    
    def save_logs(self) -> Path:
        """Save detailed logs to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"job_run_{timestamp}.json"
        
        # Convert results to dict for JSON serialization
        log_data = {
            "run_timestamp": timestamp,
            "jobs_directory": str(self.jobs_dir),
            "total_jobs": len(self.results),
            "results": [asdict(result) for result in self.results]
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        return log_file
    
    def print_summary(self) -> None:
        """Print final summary report."""
        if not self.results:
            print("No jobs were executed")
            return
        
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
        default=Path.cwd() / "jobs"
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
    print(f"Jobs directory: {runner.jobs_dir}")
    print(f"Log directory: {runner.log_dir}")
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
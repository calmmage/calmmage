from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel


class Job(BaseModel):
    """Represents a scheduled job to be executed."""
    id: str
    name: str
    executable: str
    args: Optional[List[str]] = None
    kwargs: Optional[Dict[str, Any]] = None
    env_file: Optional[Path] = None
    schedule: str  # Cron-like expression or interval
    next_run: Optional[datetime] = None
    last_run: Optional[datetime] = None
    enabled: bool = True


class JobRunLog(BaseModel):
    """Represents a log entry for a job execution."""
    job_id: str
    timestamp: datetime
    status: str  # "success", "failed", "skipped"
    duration: Optional[float] = None  # in seconds
    error: Optional[str] = None


class DataStorageBase(ABC):
    """Abstract base class for data storage implementations."""
    
    @abstractmethod
    async def add_job(self, job: Job) -> str:
        """Add a new job to the storage.
        
        Args:
            job: The job to add
            
        Returns:
            str: The ID of the added job
        """
        pass
    
    @abstractmethod
    async def get_job(self, job_id: str) -> Optional[Job]:
        """Get a job by its ID.
        
        Args:
            job_id: The ID of the job to retrieve
            
        Returns:
            Optional[Job]: The job if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def update_job(self, job: Job) -> bool:
        """Update an existing job.
        
        Args:
            job: The job to update
            
        Returns:
            bool: True if the job was updated, False otherwise
        """
        pass
    
    @abstractmethod
    async def delete_job(self, job_id: str) -> bool:
        """Delete a job by its ID.
        
        Args:
            job_id: The ID of the job to delete
            
        Returns:
            bool: True if the job was deleted, False otherwise
        """
        pass
    
    @abstractmethod
    async def list_jobs(self, enabled_only: bool = False) -> List[Job]:
        """List all jobs.
        
        Args:
            enabled_only: If True, only return enabled jobs
            
        Returns:
            List[Job]: List of jobs
        """
        pass
    
    @abstractmethod
    async def get_due_jobs(self, now: datetime) -> List[Job]:
        """Get jobs that are due to run.
        
        Args:
            now: The current time
            
        Returns:
            List[Job]: List of jobs that are due to run
        """
        pass
    
    @abstractmethod
    async def add_job_run_log(self, log: JobRunLog) -> str:
        """Add a job run log entry.
        
        Args:
            log: The log entry to add
            
        Returns:
            str: The ID of the added log entry
        """
        pass
    
    @abstractmethod
    async def get_job_run_logs(self, job_id: str, limit: int = 10) -> List[JobRunLog]:
        """Get run logs for a specific job.
        
        Args:
            job_id: The ID of the job to get logs for
            limit: Maximum number of logs to return
            
        Returns:
            List[JobRunLog]: List of job run logs
        """
        pass

"""
Cronicle API client wrapper.
"""

import requests
import json
from typing import Dict, Any, Optional, List


class CronicleClient:
    """Client for interacting with Cronicle API."""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key
        }
    
    def create_event(self, 
                    title: str,
                    executable: str,
                    plugin: str = "generic_job_executor",
                    category: str = "general", 
                    target: str = "all_servers",
                    timing: Optional[Dict[str, List[int]]] = None,
                    env_file: Optional[str] = None,
                    kwargs: Optional[Dict[str, Any]] = None,
                    enabled: bool = True) -> Dict[str, Any]:
        """
        Create a new scheduled event in Cronicle.
        
        Args:
            title: Display name for the event
            executable: Path to the executable to run
            plugin: Plugin ID to use
            category: Category ID
            target: Target server or group
            timing: Schedule configuration (e.g., {"hours": [9], "minutes": [0]})
            env_file: Path to .env file
            kwargs: Additional arguments to pass to executable
            enabled: Whether the event is active
            
        Returns:
            API response dictionary
        """
        url = f"{self.base_url}/api/app/create_event/v1"
        
        # Build plugin parameters
        params = {"executable": executable}
        if env_file:
            params["env_file"] = env_file
        if kwargs:
            params["kwargs"] = json.dumps(kwargs)
        
        payload = {
            "title": title,
            "category": category,
            "plugin": plugin,
            "target": target,
            "params": params,
            "enabled": 1 if enabled else 0
        }
        
        if timing:
            payload["timing"] = timing
            
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def run_event(self, event_id: str) -> Dict[str, Any]:
        """Run an event immediately."""
        url = f"{self.base_url}/api/app/run_event/v1"
        payload = {"id": event_id}
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status of a specific job."""
        url = f"{self.base_url}/api/app/get_job_status/v1"
        params = {"id": job_id}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_schedule(self) -> Dict[str, Any]:
        """Get all scheduled events."""
        url = f"{self.base_url}/api/app/get_schedule/v1"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def delete_event(self, event_id: str) -> Dict[str, Any]:
        """Delete a scheduled event."""
        url = f"{self.base_url}/api/app/delete_event/v1"
        payload = {"id": event_id}
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def update_event(self, event_id: str, **kwargs) -> Dict[str, Any]:
        """Update an existing event."""
        url = f"{self.base_url}/api/app/update_event/v1"
        payload = {"id": event_id, **kwargs}
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
#!/usr/bin/env python3
"""
Hello World Job - Simple example job template.

This job demonstrates:
- Basic job structure
- Environment variable usage
- Simple output
"""

import os
import time
from datetime import datetime


def main():
    """Main job function."""
    print("🌍 Hello World Job Starting...")
    
    # Read environment variables
    job_source = os.getenv("JOB_SOURCE", "unknown")
    user_name = os.getenv("USER_NAME", "Anonymous")
    
    print(f"👋 Hello, {user_name}!")
    print(f"📍 Job source: {job_source}")
    print(f"⏰ Current time: {datetime.now().isoformat()}")
    
    # Simulate some work
    print("💼 Doing some work...")
    time.sleep(1)
    
    print("✅ Hello World Job Completed!")
    return 0


if __name__ == "__main__":
    exit(main())
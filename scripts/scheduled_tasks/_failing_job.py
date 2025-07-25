#!/usr/bin/env python3
"""
Failing Job - Demo job that always fails with an error.

This job demonstrates:
- Job failure handling
- Error logging and reporting
- Exception propagation
"""

import sys
import time
import random
from datetime import datetime


def main():
    """Main job function that always fails."""
    print("💥 Failing Job Starting...")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    # Do some "work" before failing
    print("📊 Initializing critical systems...")
    time.sleep(0.5)
    
    print("🔍 Checking prerequisites...")
    time.sleep(0.3)
    
    print("⚠️  Critical error detected!")
    
    # Choose a random failure mode for variety
    failure_modes = [
        ("FileNotFoundError", "Critical configuration file not found: /nonexistent/config.yaml"),
        ("ConnectionError", "Failed to connect to database: Connection refused"),
        ("ValueError", "Invalid configuration: expected positive integer, got -1"),
        ("PermissionError", "Access denied: insufficient permissions to write log file"),
        ("RuntimeError", "System resource exhausted: out of memory")
    ]
    
    error_type, error_msg = random.choice(failure_modes)
    
    print(f"❌ {error_type}: {error_msg}")
    print("🚨 Job failed - manual intervention required!")
    
    # Raise the actual error
    if error_type == "FileNotFoundError":
        raise FileNotFoundError(error_msg)
    elif error_type == "ConnectionError":
        raise ConnectionError(error_msg)
    elif error_type == "ValueError":
        raise ValueError(error_msg)
    elif error_type == "PermissionError":
        raise PermissionError(error_msg)
    else:
        raise RuntimeError(error_msg)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"💀 Fatal error: {e}")
        sys.exit(1)
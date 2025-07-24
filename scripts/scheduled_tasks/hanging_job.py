#!/usr/bin/env python3
"""
Hanging Job - A job that truly hangs forever to test timeout functionality.

This job will run indefinitely until killed by the job runner's timeout mechanism.
"""

import time
import sys
from datetime import datetime


def main():
    """Main function that hangs forever."""
    print("🔄 Hanging Job Starting...")
    print(f"⏰ Started at: {datetime.now().isoformat()}")
    print("💤 This job will hang indefinitely...")
    print("⏰ Timeout should kill it after 5 minutes")
    
    # Infinite loop with periodic output so we can see it's running
    counter = 0
    while True:
        counter += 1
        if counter % 10 == 0:  # Print every 10 seconds
            print(f"   Still hanging... {counter * 1} seconds elapsed")
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n⚠️  Job killed at {datetime.now().isoformat()}")
        sys.exit(130)  # Standard exit code for SIGINT
#!/usr/bin/env python3
"""Daily Obsidian cleanup - scheduled job for daily note organization."""

import sys
from pathlib import Path

from tools.obsidian_sorter.daily_simple import cleanup_daily

def main():
    """Run daily cleanup as a scheduled job."""
    print("🎯 FINAL STATUS: Starting daily cleanup")
    
    try:
        # Run cleanup with auto-yes (no interaction needed for scheduled job)
        cleanup_daily(
            config_path=Path("config.yaml"),
            dry_run=False,
            yes=True  # Auto-confirm for scheduled execution
        )
        
        print("🎯 FINAL STATUS: success - Daily cleanup completed")
        print("📝 FINAL NOTES: Organized daily notes and moved files to correct locations")
        
    except Exception as e:
        print(f"🎯 FINAL STATUS: fail - Daily cleanup failed: {e}")
        print("📝 FINAL NOTES: Check daily cleanup configuration and vault permissions")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
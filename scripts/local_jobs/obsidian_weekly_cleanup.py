#!/usr/bin/env python3
"""Weekly Obsidian cleanup - scheduled job for weekly note organization."""

import sys
from pathlib import Path

from tools.obsidian_sorter.daily_simple import cleanup_weekly

def main():
    """Run weekly cleanup as a scheduled job."""
    print("🎯 FINAL STATUS: Starting weekly cleanup")
    
    try:
        # Run cleanup with auto-yes (no interaction needed for scheduled job)
        cleanup_weekly(
            config_path=Path("config.yaml"),
            dry_run=False,
            yes=True  # Auto-confirm for scheduled execution
        )
        
        print("🎯 FINAL STATUS: success - Weekly cleanup completed")
        print("📝 FINAL NOTES: Organized weekly notes and renamed old format files to avoid search collisions")
        
    except Exception as e:
        print(f"🎯 FINAL STATUS: fail - Weekly cleanup failed: {e}")
        print("📝 FINAL NOTES: Check weekly cleanup configuration and vault permissions")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
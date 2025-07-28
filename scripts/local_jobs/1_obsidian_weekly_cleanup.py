#!/usr/bin/env python3
"""Weekly Obsidian cleanup - scheduled job for weekly note organization."""

import sys
from pathlib import Path

from tools.obsidian_sorter.daily_simple import cleanup_weekly

def main():
    """Run weekly cleanup as a scheduled job."""
    try:
        # Run cleanup and get structured result
        result = cleanup_weekly(
            config_path=Path("config.yaml"),
            dry_run=False,
            yes=True,  # Auto-confirm for scheduled execution
        )
        
        # Determine status based on actual work done
        if not result.had_work_to_do:
            print("🎯 FINAL STATUS: no_change")
        elif result.files_moved > 0:
            print("🎯 FINAL STATUS: success")
            print(f"📝 FINAL NOTES: {result.files_moved} files moved")
        else:
            print("🎯 FINAL STATUS: no_change")
        
    except Exception as e:
        print(f"❌ Error during weekly cleanup: {e}")
        print(f"🎯 FINAL STATUS: fail")
        print(f"📝 FINAL NOTES: {type(e).__name__} - check logs")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
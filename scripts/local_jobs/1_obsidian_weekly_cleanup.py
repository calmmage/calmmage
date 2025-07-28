#!/usr/bin/env python3
"""Weekly Obsidian cleanup - scheduled job for weekly note organization."""

import sys
from pathlib import Path

from tools.obsidian_sorter.daily_simple import cleanup_weekly

def main():
    """Run weekly cleanup as a scheduled job."""
    try:
        # Run cleanup with auto-yes (no interaction needed for scheduled job)
        cleanup_weekly(
            config_path=Path("config.yaml"),
            dry_run=False,
            yes=True  # Auto-confirm for scheduled execution
        )

        # Check if any work was actually done by looking at the function result
        # For now, assume success means work was done - could be enhanced with return value
        print("🎯 FINAL STATUS: success")
        
    except Exception as e:
        print(f"❌ Error during weekly cleanup: {e}")
        print(f"🎯 FINAL STATUS: fail")
        print(f"📝 FINAL NOTES: {type(e).__name__} - check logs")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
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
        result = cleanup_daily(
            config_path=Path("config.yaml"),
            dry_run=False,
            yes=True  # Auto-confirm for scheduled execution
        )
        
        # Extract statistics from result if available
        if hasattr(result, 'files_processed'):
            files_count = result.files_processed
            notes_count = getattr(result, 'notes_organized', 0)
            print("🎯 FINAL STATUS: success - Daily cleanup completed")
            print(f"📝 FINAL NOTES: Processed {files_count} files, organized {notes_count} daily notes")
        else:
            print("🎯 FINAL STATUS: success - Daily cleanup completed")
            print("📝 FINAL NOTES: Daily cleanup completed successfully, check logs for details")
        
    except Exception as e:
        print(f"🎯 FINAL STATUS: fail - Daily cleanup failed: {e}")
        print("📝 FINAL NOTES: Check daily cleanup configuration and vault permissions")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
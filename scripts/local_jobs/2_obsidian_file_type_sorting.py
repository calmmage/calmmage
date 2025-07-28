#!/usr/bin/env python3
"""Obsidian file type sorting - scheduled job for organizing files by node type."""

import sys
from pathlib import Path

from tools.obsidian_sorter.generic_note_cleanup import cleanup_all_types

def main():
    """Run file type sorting as a scheduled job."""
    try:
        # Run cleanup and get structured result
        result = cleanup_all_types(
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
        print(f"❌ Error during file type sorting: {e}")
        print(f"🎯 FINAL STATUS: fail")
        print(f"📝 FINAL NOTES: {type(e).__name__} - check logs")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
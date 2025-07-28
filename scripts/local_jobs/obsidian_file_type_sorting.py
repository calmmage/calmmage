#!/usr/bin/env python3
"""Obsidian file type sorting - scheduled job for organizing files by node type."""

import sys
from pathlib import Path

from tools.obsidian_sorter.generic_note_cleanup import cleanup_all_types

def main():
    """Run file type sorting as a scheduled job."""
    print("🎯 FINAL STATUS: Starting file type sorting cleanup")
    
    try:
        # Run cleanup with auto-yes (no interaction needed for scheduled job)
        cleanup_all_types(
            config_path=Path("config.yaml"),
            dry_run=False,
            yes=True  # Auto-confirm for scheduled execution
        )
        
        print("🎯 FINAL STATUS: success - File type sorting completed")
        print("📝 FINAL NOTES: Organized all configured node types into their designated folders")
        
    except Exception as e:
        print(f"🎯 FINAL STATUS: fail - File type sorting failed: {e}")
        print("📝 FINAL NOTES: Check file type sorting configuration and node type definitions")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
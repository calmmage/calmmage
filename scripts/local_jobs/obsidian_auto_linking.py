#!/usr/bin/env python3
"""Obsidian auto-linking - scheduled job for linking files to daily notes."""

import sys
from pathlib import Path

from tools.obsidian_sorter.daily_simple import auto_link

def main():
    """Run auto-linking as a scheduled job."""
    print("🎯 FINAL STATUS: Starting auto-linking")
    
    try:
        # Run auto-linking with auto-yes (no interaction needed for scheduled job)
        auto_link(
            config_path=Path("config.yaml"),
            dry_run=False,
            yes=True,  # Auto-confirm for scheduled execution
            skip_date_conflicts=False  # Keep full confirmation logic
        )
        
        print("🎯 FINAL STATUS: success - Auto-linking completed")
        print("📝 FINAL NOTES: Linked files to daily notes using incremental processing with cutoff dates")
        
    except Exception as e:
        print(f"🎯 FINAL STATUS: fail - Auto-linking failed: {e}")
        print("📝 FINAL NOTES: Check auto-linking configuration and vault permissions")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
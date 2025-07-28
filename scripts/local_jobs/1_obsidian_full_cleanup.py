#!/usr/bin/env python3
"""Full Obsidian cleanup - scheduled job for all operations (daily + weekly + auto-linking)."""

import sys
from pathlib import Path

from tools.obsidian_sorter.daily_simple import run_all

def main():
    """Run full cleanup as a scheduled job."""
    print("🎯 FINAL STATUS: Starting full Obsidian cleanup")
    
    try:
        # Run all operations with auto-yes (no interaction needed for scheduled job)
        run_all(
            config_path=Path("config.yaml"),
            dry_run=False,
            yes=True  # Auto-confirm for scheduled execution
        )
        
        print("🎯 FINAL STATUS: success - Full cleanup completed")
        print("📝 FINAL NOTES: Completed daily cleanup, weekly cleanup, and auto-linking in sequence")
        
    except Exception as e:
        print(f"🎯 FINAL STATUS: fail - Full cleanup failed: {e}")
        print("📝 FINAL NOTES: Check full cleanup configuration and individual component status")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
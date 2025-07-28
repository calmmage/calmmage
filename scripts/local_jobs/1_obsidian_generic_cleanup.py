#!/usr/bin/env python3
"""Generic Obsidian cleanup - scheduled job for all node type organization."""

import sys
from pathlib import Path

from tools.obsidian_sorter.generic_node_cleanup import cleanup_all_types

def main():
    """Run generic cleanup as a scheduled job."""
    print("🎯 FINAL STATUS: Starting generic node type cleanup")
    
    try:
        # Run cleanup with auto-yes (no interaction needed for scheduled job)
        cleanup_all_types(
            config_path=Path("config.yaml"),
            dry_run=False,
            yes=True  # Auto-confirm for scheduled execution
        )
        
        print("🎯 FINAL STATUS: success - Generic cleanup completed")
        print("📝 FINAL NOTES: Organized all configured node types into their designated folders")
        
    except Exception as e:
        print(f"🎯 FINAL STATUS: fail - Generic cleanup failed: {e}")
        print("📝 FINAL NOTES: Check generic cleanup configuration and node type definitions")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
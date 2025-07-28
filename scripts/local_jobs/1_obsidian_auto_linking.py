#!/usr/bin/env python3
"""Obsidian auto-linking - scheduled job for linking files to daily notes."""

import sys
from pathlib import Path

from tools.obsidian_sorter.daily_simple import auto_link

def main():
    """Run auto-linking as a scheduled job."""
    try:
        # Run auto-linking with auto-yes (no interaction needed for scheduled job)
        result = auto_link(
            config_path=Path("config.yaml"),
            dry_run=False,
            yes=True,  # Auto-confirm for scheduled execution
            skip_date_conflicts=False  # Keep full confirmation logic
        )
        
        # Extract statistics from result if available
        if hasattr(result, 'files_linked'):
            linked_count = result.files_linked
            notes_count = getattr(result, 'notes_processed', 0)
            
            # Soft warning for high activity (just for fun)
            if linked_count > 10:
                print("🎯 FINAL STATUS: requires_attention")
                print(f"📝 FINAL NOTES: {linked_count} files linked, {notes_count} notes (busy!)")
            else:
                print("🎯 FINAL STATUS: success")
                print(f"📝 FINAL NOTES: {linked_count} linked, {notes_count} notes")
        else:
            print("🎯 FINAL STATUS: success")
        
    except Exception as e:
        print(f"🎯 FINAL STATUS: fail - Auto-linking failed: {e}")
        print("📝 FINAL NOTES: Check config/permissions")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
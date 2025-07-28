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
                print("🎯 FINAL STATUS: requires_attention - Auto-linking completed with high activity")
                print(f"📝 FINAL NOTES: Linked {linked_count} files to daily notes, processed {notes_count} notes (busy day! 🚀)")
            else:
                print("🎯 FINAL STATUS: success - Auto-linking completed")
                print(f"📝 FINAL NOTES: Linked {linked_count} files to daily notes, processed {notes_count} notes")
        else:
            print("🎯 FINAL STATUS: success - Auto-linking completed")
            print("📝 FINAL NOTES: Auto-linking completed successfully, check logs for details")
        
    except Exception as e:
        print(f"🎯 FINAL STATUS: fail - Auto-linking failed: {e}")
        print("📝 FINAL NOTES: Check auto-linking configuration and vault permissions")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""Git sync automation job - synchronize git repositories across all projects."""

import sys
from pathlib import Path

from src.lib.coding_projects import get_local_projects
from tools.git_sync_tool.git_sync import GitSyncManager


def main():
    """Synchronize git repositories across all discovered projects."""
    try:
        # Initialize git sync manager with conservative settings for automation
        manager = GitSyncManager(
            dry_run=False,
            skip_backup=False,  # Always create backups for safety
            backup_prefix="daily-snapshots", 
            timeout=60,
            force_complex=False,  # Don't attempt complex merges in automation
            verbose=False  # Quiet mode for automation - only show attention-needed items
        )
        
        projects = get_local_projects()
        git_projects = [p for p in projects if manager.is_git_repository(p.path)]
        
        print(f"Found {len(git_projects)} git repositories out of {len(projects)} total projects")
        
        if not git_projects:
            print("🎯 FINAL STATUS: success")
            print("📝 FINAL NOTES: No git repos found")
            return 0
        
        # Sync all repositories
        results = manager.sync_all_repositories([p.path for p in git_projects])
        
        # Track statistics
        stats = {"success": 0, "no_change": 0, "requires_attention": 0, "fail": 0}
        actions = {"up_to_date": 0, "pulled": 0, "local_only": 0, "complex_case": 0, "skipped": 0}
        
        for result in results:
            stats[result.status] += 1
            actions[result.action] += 1
        
        # Determine final status
        if stats["fail"] > 0:
            final_status = "fail"
        elif stats["requires_attention"] > 0:
            final_status = "requires_attention"
        elif stats["success"] > 0:
            final_status = "success"
        else:
            final_status = "no_change"
        
        print(f"🎯 FINAL STATUS: {final_status}")
        
        # Detailed statistics in FINAL NOTES
        notes_parts = [f"Processed {len(git_projects)} git repositories"]
        if actions["pulled"] > 0:
            notes_parts.append(f"{actions['pulled']} pulled updates")
        if actions["local_only"] > 0:
            notes_parts.append(f"{actions['local_only']} with local changes")
        if actions["complex_case"] > 0:
            notes_parts.append(f"{actions['complex_case']} need manual merge")
        if stats["fail"] > 0:
            notes_parts.append(f"{stats['fail']} failed")
        
        print(f"📝 FINAL NOTES: {', '.join(notes_parts)}")
        return 0
        
    except Exception as e:
        print(f"🎯 FINAL STATUS: fail")
        print("📝 FINAL NOTES: Check git/discovery")
        return 1


if __name__ == "__main__":
    sys.exit(main())
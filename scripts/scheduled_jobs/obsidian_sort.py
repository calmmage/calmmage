#!/usr/bin/env python3
"""
Obsidian Auto-Sort Scheduled Job

Automatically sorts notes from Obsidian inbox to appropriate folders
based on configured rules. Uses the obsidian_sorter tool.

This job is designed to be run by local_job_runner and provides
structured output in the expected format.
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

try:
    # Import the sorter tool
    from tools.obsidian_sorter.config import ObsidianSorterConfig
    from tools.obsidian_sorter.sorter import ObsidianSorter
    
    def main():
        """Main job execution."""
        print("🗂️  Starting Obsidian auto-sort job...")
        
        # Use default configuration
        config = ObsidianSorterConfig()
        
        # Validate paths exist
        if not config.obsidian_root.exists():
            print(f"❌ Obsidian root does not exist: {config.obsidian_root}")
            print("🎯 FINAL STATUS: fail - Obsidian vault not found")
            print("📝 FINAL NOTES: Check obsidian_root path in configuration")
            return
        
        if not config.full_inbox_path.exists():
            print(f"📭 Inbox folder does not exist: {config.full_inbox_path}")
            print("🎯 FINAL STATUS: no_change - No inbox folder to process")
            print("📝 FINAL NOTES: Inbox folder not found, nothing to sort")
            return
        
        if not config.rules:
            print("⚠️  No sorting rules configured")
            print("🎯 FINAL STATUS: no_change - No rules configured")
            print("📝 FINAL NOTES: No sorting rules found in configuration")
            return
        
        print(f"📁 Obsidian vault: {config.obsidian_root}")
        print(f"📨 Inbox: {config.full_inbox_path}")
        print(f"📏 Active rules: {len(config.rules)}")
        
        # Create sorter and run
        sorter = ObsidianSorter(config)
        results = sorter.sort_all()
        
        # Print summary
        if results:
            sorter.print_results()
        
        # Generate structured output for job runner
        status, notes = sorter.generate_status_output()
        print(f"🎯 FINAL STATUS: {status}")
        print(f"📝 FINAL NOTES: {notes}")
        
        # Additional details for successful operations
        if results and any(r.success for r in results):
            successful_rules = {}
            for result in results:
                if result.success and result.rule_name:
                    successful_rules[result.rule_name] = successful_rules.get(result.rule_name, 0) + 1
            
            if successful_rules:
                rule_details = ", ".join([f"{count} via '{rule}'" for rule, count in successful_rules.items()])
                print(f"📊 Rule breakdown: {rule_details}")

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Failed to import obsidian_sorter: {e}")
    print("🎯 FINAL STATUS: fail - Missing dependencies")
    print("📝 FINAL NOTES: Could not import obsidian_sorter tool")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print("🎯 FINAL STATUS: fail - Unexpected error occurred")
    print(f"📝 FINAL NOTES: Job failed with error: {str(e)}")
    sys.exit(1)
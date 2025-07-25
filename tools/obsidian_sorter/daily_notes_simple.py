#!/usr/bin/env python3
"""
Simple Daily Notes Organizer - Step by step exploration

Just handles daily notes with format "25 July 2025" and moves them to daily/ folder.
Building this up gradually to understand what we want.
"""

from pathlib import Path
import re

# Your obsidian root
OBSIDIAN_ROOT = Path("/Users/petrlavrov/work/projects/taskzilla-cm/main/root")


def is_daily_note_standard(filename: str) -> bool:
    """Check if filename matches standard daily note format: '25 Jul 2025.md'"""
    # DD MMM YYYY format with spaces
    pattern = r'^\d{1,2} [A-Za-z]{3} \d{4}\.md$'
    return bool(re.match(pattern, filename))


def is_daily_note_alternative(filename: str) -> str:
    """Check if filename matches alternative daily note formats. Returns format type or None."""
    patterns = {
        'dashes_dmy': r'^\d{1,2}-[A-Za-z]{3}-\d{4}\.md$',  # 11-Feb-2025.md
        'dashes_mdy': r'^[A-Za-z]{3}-\d{1,2}-\d{4}\.md$',  # Feb-11-2025.md  
        'spaces_long': r'^\d{1,2} [A-Za-z]{4,} \d{4}\.md$', # 25 July 2025.md (full month)
    }
    
    for format_type, pattern in patterns.items():
        if re.match(pattern, filename):
            return format_type
    return None


def is_daily_note(filename: str) -> bool:
    """Check if filename is any type of daily note."""
    return is_daily_note_standard(filename) or is_daily_note_alternative(filename) is not None


def analyze_vault():
    """Analyze the entire vault structure for daily notes."""
    print("🗓️  Daily Notes Vault Analysis")
    print(f"📁 Obsidian root: {OBSIDIAN_ROOT}")
    
    if not OBSIDIAN_ROOT.exists():
        print("❌ Obsidian root doesn't exist")
        return
    
    # Get ALL markdown files recursively
    print("🔍 Scanning all markdown files in vault...")
    all_files = list(OBSIDIAN_ROOT.rglob("*.md"))
    print(f"📄 Found {len(all_files)} total markdown files")
    
    # Organize by location for analysis
    files_by_location = {}
    all_daily_standard = []
    all_daily_alternative = {}
    all_non_daily = []
    
    for file in all_files:
        # Determine location relative to root
        try:
            relative_path = file.relative_to(OBSIDIAN_ROOT)
            if len(relative_path.parts) == 1:
                location = "root"
            else:
                location = relative_path.parts[0]
        except ValueError:
            location = "unknown"
        
        if location not in files_by_location:
            files_by_location[location] = []
        files_by_location[location].append(file)
        
        # Categorize the file
        if is_daily_note_standard(file.name):
            all_daily_standard.append(file)
        else:
            alt_format = is_daily_note_alternative(file.name)
            if alt_format:
                if alt_format not in all_daily_alternative:
                    all_daily_alternative[alt_format] = []
                all_daily_alternative[alt_format].append(file)
            else:
                all_non_daily.append(file)
    
    # Show breakdown by location
    print("\n📂 FILES BY LOCATION:")
    for location, files in sorted(files_by_location.items()):
        daily_standard = [f for f in files if is_daily_note_standard(f.name)]
        daily_alt = {}
        non_daily = []
        
        for file in files:
            if not is_daily_note_standard(file.name):
                alt_format = is_daily_note_alternative(file.name)
                if alt_format:
                    if alt_format not in daily_alt:
                        daily_alt[alt_format] = []
                    daily_alt[alt_format].append(file)
                else:
                    non_daily.append(file)
        
        print(f"  📁 {location}: {len(files)} files")
        print(f"    ✅ Standard daily: {len(daily_standard)}")
        for fmt, fmt_files in daily_alt.items():
            print(f"    🔄 {fmt}: {len(fmt_files)}")
        print(f"    📄 Non-daily: {len(non_daily)}")
        
        # Show a few examples from each location
        if daily_standard:
            print(f"      Example standard: {daily_standard[0].name}")
        for fmt, fmt_files in daily_alt.items():
            print(f"      Example {fmt}: {fmt_files[0].name}")
    
    # Overall summary
    print("\n📊 VAULT SUMMARY:")
    print(f"  ✅ Standard daily notes (DD MMM YYYY): {len(all_daily_standard)}")
    
    total_alternatives = 0
    for fmt, files in all_daily_alternative.items():
        print(f"  🔄 Alternative format ({fmt}): {len(files)}")
        total_alternatives += len(files)
    
    print(f"  📄 Non-daily files: {len(all_non_daily)}")
    print(f"  📈 Total daily notes: {len(all_daily_standard) + total_alternatives}")
    
    # Show detailed examples of alternatives with their locations
    if all_daily_alternative:
        print("\n🔍 ALTERNATIVE FORMAT EXAMPLES:")
        for fmt, files in all_daily_alternative.items():
            for file in files:
                relative_path = file.relative_to(OBSIDIAN_ROOT)
                print(f"  {fmt}: {file.name} (in {relative_path.parent})")
    
    # Show some daily notes in wrong locations
    print("\n📍 DAILY NOTES LOCATION ANALYSIS:")
    daily_in_root = [f for f in all_daily_standard if f.parent == OBSIDIAN_ROOT]
    daily_in_inbox = [f for f in all_daily_standard if f.parent.name == "Inbox"]
    daily_in_daily = [f for f in all_daily_standard if f.parent.name == "daily"]
    daily_elsewhere = [f for f in all_daily_standard if f not in daily_in_root + daily_in_inbox + daily_in_daily]
    
    if daily_in_root:
        print(f"  📁 In root: {len(daily_in_root)} files (should be moved to daily/)")
    if daily_in_inbox:
        print(f"  📥 In Inbox: {len(daily_in_inbox)} files (should be moved to daily/)")
    if daily_in_daily:
        print(f"  ✅ In daily/: {len(daily_in_daily)} files (correct location)")
    if daily_elsewhere:
        print(f"  📂 In other folders: {len(daily_elsewhere)} files (should be moved to daily/)")
        for file in daily_elsewhere[:3]:  # Show first 3
            relative_path = file.relative_to(OBSIDIAN_ROOT)
            print(f"      {file.name} in {relative_path.parent}")
        if len(daily_elsewhere) > 3:
            print(f"      ... and {len(daily_elsewhere) - 3} more")


def main():
    analyze_vault()


if __name__ == "__main__":
    main()
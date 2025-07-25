#!/usr/bin/env python3
"""
Simple Daily Notes Organizer - Step by step exploration

Just handles daily notes with format "25 July 2025" and moves them to daily/ folder.
Building this up gradually to understand what we want.
"""

from pathlib import Path
import re
import argparse

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
        # Dash formats
        'dashes_dmy': r'^\d{1,2}-[A-Za-z]{3}-\d{4}\.md$',      # 11-Feb-2025.md
        'dashes_mdy': r'^[A-Za-z]{3}-\d{1,2}-\d{4}\.md$',      # Feb-11-2025.md  
        'dashes_ymd': r'^\d{4}-[A-Za-z]{3}-\d{1,2}\.md$',      # 2024-Jul-12.md
        'dashes_ydm': r'^\d{4}-\d{1,2}-[A-Za-z]{3}\.md$',      # 2024-12-Jul.md
        'dashes_numeric_dmy': r'^\d{1,2}-\d{1,2}-\d{4}\.md$',  # 12-04-2024.md
        'dashes_numeric_mdy': r'^\d{1,2}-\d{1,2}-\d{4}\.md$',  # 04-12-2024.md (ambiguous with above)
        'dashes_numeric_ymd': r'^\d{4}-\d{1,2}-\d{1,2}\.md$',  # 2024-04-12.md
        
        # Underscore formats  
        'underscores_dmy': r'^\d{1,2}_[A-Za-z]{3}_\d{4}\.md$',      # 12_jul_2025.md
        'underscores_mdy': r'^[A-Za-z]{3}_\d{1,2}_\d{4}\.md$',      # jul_12_2025.md
        'underscores_ymd': r'^\d{4}_[A-Za-z]{3}_\d{1,2}\.md$',      # 2024_jul_12.md
        'underscores_ydm': r'^\d{4}_\d{1,2}_[A-Za-z]{3}\.md$',      # 2024_12_jul.md
        'underscores_numeric_dmy': r'^\d{1,2}_\d{1,2}_\d{4}\.md$',  # 12_04_2024.md
        'underscores_numeric_mdy': r'^\d{1,2}_\d{1,2}_\d{4}\.md$',  # 04_12_2024.md (ambiguous)
        'underscores_numeric_ymd': r'^\d{4}_\d{1,2}_\d{1,2}\.md$',  # 2024_04_12.md
        
        # Space formats
        'spaces_long': r'^\d{1,2} [A-Za-z]{4,} \d{4}\.md$',         # 25 July 2025.md (full month)
        'spaces_dmy': r'^\d{1,2} [A-Za-z]{3} \d{4}\.md$',          # 12 Jul 2025.md (your target format)
        'spaces_mdy': r'^[A-Za-z]{3} \d{1,2} \d{4}\.md$',          # Jul 12 2025.md
        'spaces_ymd': r'^\d{4} [A-Za-z]{3} \d{1,2}\.md$',          # 2024 Jul 12.md
        'spaces_numeric_dmy': r'^\d{1,2} \d{1,2} \d{4}\.md$',      # 12 04 2024.md
        'spaces_numeric_mdy': r'^\d{1,2} \d{1,2} \d{4}\.md$',      # 04 12 2024.md (ambiguous)
        'spaces_numeric_ymd': r'^\d{4} \d{1,2} \d{1,2}\.md$',      # 2024 04 12.md
    }
    
    for format_type, pattern in patterns.items():
        if re.match(pattern, filename, re.IGNORECASE):  # Case-insensitive matching
            return format_type
    return None


def is_daily_note(filename: str) -> bool:
    """Check if filename is any type of daily note."""
    return is_daily_note_standard(filename) or is_daily_note_alternative(filename) is not None


def analyze_vault(verbose: bool = False):
    """Analyze the entire vault structure for daily notes."""
    if verbose:
        print("🗓️  Daily Notes Vault Analysis")
        print(f"📁 Obsidian root: {OBSIDIAN_ROOT}")
    
    if not OBSIDIAN_ROOT.exists():
        print("❌ Obsidian root doesn't exist")
        return
    
    # Get ALL markdown files recursively
    if verbose:
        print("🔍 Scanning all markdown files in vault...")
    all_files = list(OBSIDIAN_ROOT.rglob("*.md"))
    if verbose:
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
    
    # Calculate totals
    total_alternatives = sum(len(files) for files in all_daily_alternative.values())
    total_daily_notes = len(all_daily_standard) + total_alternatives
    
    # DEFAULT OUTPUT - what user wants to see by default
    print(f"📁 Obsidian vault: {OBSIDIAN_ROOT}")
    print(f"📄 Total notes: {len(all_files)}")
    print(f"📅 Total daily notes: {total_daily_notes}")
    print(f"✅ Standard format (DD MMM YYYY): {len(all_daily_standard)}")
    
    # List all non-standard daily note names for manual renaming
    if all_daily_alternative:
        print(f"\n🔄 Non-standard daily notes to rename:")
        for fmt, files in all_daily_alternative.items():
            for file in files:
                relative_path = file.relative_to(OBSIDIAN_ROOT)
                print(f"  {file.name} (in {relative_path.parent})")
    else:
        print(f"🎉 All daily notes are in standard format!")
    
    # VERBOSE OUTPUT - detailed analysis
    if verbose:
        print("\n" + "="*50)
        print("VERBOSE MODE - DETAILED ANALYSIS")
        print("="*50)
        
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
        
        print("\n📊 DETAILED VAULT SUMMARY:")
        for fmt, files in all_daily_alternative.items():
            print(f"  🔄 Alternative format ({fmt}): {len(files)}")
        print(f"  📄 Non-daily files: {len(all_non_daily)}")
        
        # Show daily notes in wrong locations
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
    parser = argparse.ArgumentParser(description="Daily Notes Simple Organizer")
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Show detailed analysis (default: concise summary)"
    )
    
    args = parser.parse_args()
    analyze_vault(verbose=args.verbose)


if __name__ == "__main__":
    main()
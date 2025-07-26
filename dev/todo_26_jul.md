# Todo - July 26, 2025

## Obsidian Sorter Issues to Fix

### 1. Parse check mark emoji in file name for 'done' status
- Parse check mark emoji (✅) in file names and treat that as 'done' status
- Files with ✅ in name should be handled differently (maybe skip processing or move to done folder)
- Need to decide: should ✅ files be excluded from auto-linking? from cleanup? from both?

### 2. Exclude weekly notes from auto-link analysis
- Weekly notes are creating too many daily files during auto-linking
- A single weekly note gets auto-linked into multiple daily files, creating clutter
- Add exclusion logic to skip weekly notes (files matching weekly note patterns) from auto-link candidate analysis
- Weekly notes should stay in their weekly_workspaces folder and not create daily note links

### 3. Fix archived weekly notes handling
- Archived weekly notes were moved out of their archive folders instead of being renamed in place
- Expected: Week 45 - 6 Nov 2024.md in weekly_workspaces/archive-2024/ should be renamed to Week 2024-45 - 6 Nov 2024.md
  in the same archive folder
- Actual: Files were moved from archive folders to main weekly_workspaces folder
- Issue might be with order of operations or incorrect path handling in rename logic
- Check weekly cleanup logic for proper archive folder preservation

## Additional Notes
- Jobs are running but with warnings due to missing files (files already processed)
- obsidiantools Path issue was fixed (passing Path object instead of string)
- Overall system is working but needs these refinements for better behavior
# Obsidian Auto-Sorting Tool Requirements

## Problem
Obsidian creates notes in either:
- Static `/Inbox` directory
- Same directory as current note

No way to programmatically route notes to appropriate folders based on content.

## Solution Overview
Auto-sorting tool that:
- Detects note types from templates/tags/existing fields
- Moves notes from Inbox to appropriate folders
- Configurable via config.yaml + pydantic model

## Tool Structure

### 1. Typer CLI Tool
Location: `calmmage/tools/obsidian_sorter/`
```
obsidian_sorter/
├── cli.py                    # Main typer CLI
├── sorter.py                 # Core sorting logic
├── config.py                 # Pydantic config model
├── detectors.py              # Note type detection
└── config.yaml              # Default configuration
```

### 2. Scheduled Job
Location: `calmmage/scripts/scheduled_jobs/obsidian_sort.py`
- Calls the tool's main sorting functionality
- Uses local_job_runner output format (FINAL_STATUS/FINAL_NOTES)

## Configuration

### ObsidianSorterConfig (Pydantic)
```python
class ObsidianSorterConfig(BaseModel):
    obsidian_root: Path
    inbox_path: Path
    rules: List[SortingRule]
    templates_path: Optional[Path]
    auto_detect: bool = True
```

### SortingRule
```python
class SortingRule(BaseModel):
    name: str
    detector_type: str  # "tag", "template", "content", "filename"
    pattern: str
    target_folder: Path
    priority: int = 0
```

## Detection Methods
1. **Template-based**: Match against existing templates
2. **Tag-based**: Parse frontmatter tags
3. **Content-based**: Analyze note content patterns
4. **Filename-based**: Match filename patterns

## Key Paths
- Obsidian root: `/Users/petrlavrov/work/projects/taskzilla-cm/main/root`
- Inbox: `{obsidian_root}/Inbox`
- Target folders: Auto-detected or configured

## Output Format
Uses local_job_runner format:
```bash
echo "🎯 FINAL STATUS: success - Sorted 5 notes to appropriate folders"
echo "📝 FINAL NOTES: Moved 3 daily notes, 1 project note, 1 meeting note"
```
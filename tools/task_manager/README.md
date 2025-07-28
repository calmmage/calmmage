# Task Management Tool

A fuzzy parser for markdown-style task lists that maintains backward mapping from items to their location in text.

## Features

- **Fuzzy Parsing**: Parses markdown files with flexible formatting
  - Supports `-`, `*`, and numbered list items
  - Handles checkbox syntax `[ ]` and `[x]`
  - Recognizes nested sub-items based on indentation
  - Splits sections by double newlines or `---` separators

- **Backward Mapping**: Maintains a mapping from each task item to its exact location in the source file
  - Line numbers
  - Character positions
  - File path

- **Multi-file Support**: Can parse multiple source files configured in `config.yaml`

## Usage

### Basic Parser

```bash
python3 fuzzy_parser.py
```

This will:
1. Read source files from `config.yaml`
2. Parse all task items
3. Display items with their status and location
4. Show summary statistics

### Check Implementation Status

```bash
python3 check_implementation_status.py
```

This will:
1. Parse all outstanding items
2. Check if corresponding projects exist in the codebase
3. Report implementation status for each project

## Configuration

Edit `config.yaml` to specify task source files:

```yaml
item_source_locations:
  - experiments/season_4_jun_2025/_notes/outstanding_items.md
  - experiments/season_4_jun_2025/_notes/projects/outstanding_ideas.md
```

## Task Format

The parser recognizes various markdown list formats:

```markdown
- Simple task
-[x] Completed task
- Parent task
  - Sub-task 1
  - Sub-task 2

## Section Header
- Task in new section

---

- Task after separator
```

## Future Plans

- MCP (Model Context Protocol) integration
- Interactive task editing
- Status updates that modify source files
- Task dependencies and relationships
- Search and filter capabilities
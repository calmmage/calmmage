# Custom LLM context for this project

## Current Main Workflow

**Primary workflow location:**
`/Users/petrlavrov/calmmage/experiments/season_4_jun_2025/_notes/projects/main_workflow_25th_july_2025.md`

**Instructions for Claude:**
1. Always check and follow the current main workflow document at the path above
2. If you find a more recent workflow file with "main_workflow" in the name and a more recent date in
   `experiments/season_4_jun_2025/_notes/projects/`, use that instead
3. Search pattern: Look for files matching `main_workflow_*_2025.md` and use the most recent date
4. The workflow contains the current development priorities and process guidelines

## Python Execution Requirements

**CRITICAL: Never use sys.path.append() in tools/**
- uv installs calmmage as a package - imports work directly
- Use absolute imports: `from tools.module_name.file import Class`
- Do NOT add `sys.path.append(str(Path(__file__).parent.parent.parent))`

## Shell Aliases Configuration

**Main alias locations in Nix config:**
- **Primary aliases file**: `/Users/petrlavrov/calmmage/config/nix/shell/aliases/default.nix`
    - Imports: new.nix, navigation.nix, better_tools.nix, calmmage_tools.nix
- **Custom tool aliases**: `/Users/petrlavrov/calmmage/config/nix/shell/aliases/calmmage_tools.nix`
    - Add new calmmage-specific tool aliases here
- **General aliases**: `/Users/petrlavrov/calmmage/config/nix/shell/aliases/new.nix`
    - Poetry commands, uv commands, etc.

**Adding new aliases:**
1. Edit appropriate .nix file based on category
2. Follow format: `alias_name = "command_to_run";`
3. Rebuild nix configuration to apply changes

## Additional Context

Refer to the existing developer planning system in:
- `experiments/season_4_jun_2025/_notes/projects/outstanding_ideas.md`
- `experiments/season_4_jun_2025/_notes/projects/automations/general.md`
- Project-specific dev notes in the same directory structure
# Gemini Configuration

## Note-Taking Locations

Choose an appropriate location for feature-specific notes:

- **Current directory**: `./dev/[feature_name]/` or `./notes/[feature_name]/` 
- **Calmmage seasonal notes**: `~/work/projects/calmmage/experiments/[latest_season]/_notes/projects/[project_name]/[feature_name]/`

Use descriptive feature names (e.g., `auth_system`, `api_refactor`, `user_dashboard`). Create markdown files for task tracking and project documentation in the chosen location.

## Git Worktree Workflow

When starting work on a feature, create a git worktree:
```bash
git worktree add ~/work/ai_workspaces/[meaningful-name] -b [meaningful-branch-name]
```

This creates an isolated workspace in the AI workspaces folder with a new branch for the feature.

## Three Main Scenarios

### Scenario 1: "simple"
- **Purpose**: Minimal overhead, no extra process
- **Action**: Cancel all additional instructions and workflows
- **Behavior**: Proceed without any extra clarifications, just as before
- **Context**: Plain development, zero ceremony

### Scenario 2: "new project"
- **Purpose**: Green field development in new directory
- **Prerequisites**:
    - Working in a new/empty directory
    - Empty repo or initialized template
- **Process**:
    1. Verify empty/clean environment
    2. Work with user to determine:
        - Project idea and goals
        - UI/interaction type (CLI tool, web interface, Telegram bot, utility library)
        - Sample data and usage scenarios
        - Main usage workflow
    3. Create stubs for future clarifications
    4. Ask clarifying questions about planned architecture
- **Notes**: May not need all details upfront - create placeholders for iterative refinement

### Scenario 3: "brownfield" (existing environment)
- **Purpose**: Working within existing codebase/repo on specific feature/improvement
- **Process**:
    1. **Determine working location**: Identify main project directory
    2. **Set up project notes**:
        - Find or create specialized notes folder for this specific feature/project
        - Structure: `experiments/[latest_season]/_notes/projects/[project_name]/[feature_name]/`
    3. **Task tracking setup**: Use Markdown files in the notes folder for task tracking
    4. **Documentation**:
        - Note project path, notes path, and description
        - Add entry to `outstanding_ideas.md` in appropriate section/inbox
    5. **Context gathering**: Understand existing architecture and integration points
- **Goal**: Structured approach to extending/improving existing systems

## Python Execution

Use uv for Python commands: `uv run python script.py` or `uv run typer path/to/cli.py run [command]`

Avoid sys.path.append() in tools/ - use direct imports: `from tools.module_name.file import Class`
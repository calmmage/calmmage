# Main Workflow - 25th July 2025

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
        - Structure: `experiments/season_4_jun_2025/_notes/projects/[project_name]/`
    3. **Task tracking setup**: Use Markdown files in the notes folder for task tracking
    4. **Documentation**:
        - Note project path, notes path, and description
        - Add entry to `outstanding_ideas.md` in appropriate section/inbox
    5. **Context gathering**: Understand existing architecture and integration points
- **Goal**: Structured approach to extending/improving existing systems

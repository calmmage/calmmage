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

## Note-Taking Approach

### Three Writing Modalities

**1. AI Work-Along Notes (*_(ai_workalong).md)**
- **CRITICAL RULE**: Verbose AI explanations are FORBIDDEN in all files except those with `_(ai_workalong)` suffix
- Examples: `brainstorm_features_(ai_workalong).md`, `analysis_auth_system_(ai_workalong).md`,
  `debugging_cronicle_(ai_workalong).md`
- Use for detailed reasoning, context, technical deep-dives, lengthy explanations
- Throwaway documentation for AI processing only
- **This is the ONLY location where verbose AI explanations are permitted**

**2. Literal Capture Mode (Default)**
- When user says "write something down" - use their exact words
- Structure better with subpoints and lists
- Keep original phrasing for features, ideas, descriptions
- Break single lines into structured, shorter sentences
- **NO verbose explanations or long-form text allowed**

**3. Content Generation Mode**
- Maximum simplicity and conciseness
- Small sentences, short and to-the-point
- Format: "Feature A: point 1, point 2, point 3"
- Use established names, precise language
- **STRICTLY no lengthy explanations or verbose content**

### Formatting Rules

**Default Structure:**
```
Group name (no heading)
- item 1
- item 2
  - subitem A
  - subitem B
- item 3
```

**Depth Limits:**
- Maximum 3-5 points per level
- Maximum 2 levels of nesting
- For deeper structure: create new group with name (no heading)

**Examples:**

*Literal Capture:*
```
Authentication system
- user login via email/password
- session management with JWT tokens
  - 24-hour expiration
  - refresh token support
- password reset flow
```

*Content Generation:*
```
Core Features
- Auth: JWT sessions, email login, password reset
- API: REST endpoints, rate limiting, error handling  
- Storage: PostgreSQL, Redis cache, S3 assets
```

## Python Execution Requirements

**CRITICAL: Always use uv for Python command execution**

**For running Python scripts:**
```bash
uv run python script.py
```

**For running Typer CLI tools:**
```bash
uv run typer path/to/cli.py run [command] [args]
```

**Examples:**
- `uv run python tools/obsidian_sorter/daily_notes_simple.py`
- `uv run typer tools/obsidian_sorter/cli.py run sort`
- `uv run typer tools/cronicle_scheduler/cli/cronicle_manager.py run create`

**Never use bare python or direct script execution - always prefix with `uv run`**

**CRITICAL: Never use sys.path.append() in tools/**
- uv installs calmmage as a package - imports work directly
- Use absolute imports: `from tools.module_name.file import Class`
- Do NOT add `sys.path.append(str(Path(__file__).parent.parent.parent))`

## Additional Context

Refer to the existing developer planning system in:
- `experiments/season_4_jun_2025/_notes/projects/outstanding_ideas.md`
- `experiments/season_4_jun_2025/_notes/projects/automations/general.md`
- Project-specific dev notes in the same directory structure
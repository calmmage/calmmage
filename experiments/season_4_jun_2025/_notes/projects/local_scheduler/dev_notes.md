# Job Scheduling System - Development Notes

## User Requirements (Raw Notes)

### Overview
"I kinda want to implement two separate components that are related."

### Component 1: Cronicle Integration
- **Main parts**:
    - job runner (that the plugin will call)
    - cli tool (that I will use via alias for adding new jobs to cronicle)
- **Plugin runner requirements**:
    - "I want my cronicle-plugin-runner to be able to accept additional .env file"
    - "custom py (or other - for example typer or any arbitrary binary - executable"
    - "kwargs - but work with defaults just fine"
    - "those will be parameters of the plugin and the cli tool"

### Component 2: Standalone Job Runner
- **Purpose**: "call directly via alias in the console"
- **Integration**: "call daily from cronicle with an automated job - but this doesn't need any special integration -
  cronicle should be able to call any arbitrary python file on my disk"
- **Job types**: "something that is ok to run multiple times a day arbitrarily"
    - "cleanup obsidian / downloads folder"
    - "auto-commit all git repos"
    - "refresh my calmmage uv env"
    - "Sort_projects tool etc."
- **Configuration**: "I don't want complicated config or anything - it actually should just take ALL FILES in jobs/ dir
  and just run them. Similar to how airflow does this. VERY SIMPLE SETUP FOR NOW."
- **Output handling**: "And in the end compile a summary of each job result"
    - "Outcome enum - ok / fail / warning / done nothing + text note - ai-generated based on output"
    - "Maybe save the jobs run log somewhere as well (where do people usually put logs in their apps on mac?)"

### Structure Requirements
- **scripts dir**: "I want to use 'scripts' dir in calmmage for standalone jobs"
- **cronicle api**: "cronicle api to store my own cronicle plugin jobs (added by cli tool via api)"
- **descriptive names**: "for tools and scripts dirs I want descriptive names with clear meaning"
- **sample jobs**: "I imagine we would add a few sample jobs to the resources/ dir"
- **job structure**: "I imagine them each being in a separate folder and containing stuff like .env of yaml config
  beside them - so that it illustrates that they work fine with those"
- **runner location**: "runner should be in tools not in scripts"

### Technical Requirements
- **CLI framework**: "please note that I'd like the cli to be implemented with typer"
- **API research**: "do you have access to context7 mcp? I want you to look up up-to-date cronicle api docs and typer
  docs"
- **existing examples**: "I have already been able to successfully test the cronicle api - look up in the
  /Users/petrlavrov/work/projects/calmmage/experiments/season_4_jun_2025/try-cronicle - examples here"

### Documentation Requirements
- **dev notes**: "please capture all my notes in as raw form as possible - just add formatting - in some dev_notes.md
  file"
- **makefile**: "please capture main usage scenarios / examples / commands in a special Makefile (for now I want just
  basic typer usage - just make sure it's working well and covers main features.)"

### Log Storage on Mac
- Standard locations for application logs on macOS:
    - `~/Library/Logs/[AppName]/` - User-specific logs
    - `/var/log/` - System-wide logs (requires admin)
    - `~/.local/share/[appname]/logs/` - XDG Base Directory spec
    - Project directory: `./logs/` - Simple approach for development

## Technical Research Summary

### Cronicle API Key Findings
- Uses REST API with JSON format
- Authentication via `X-API-Key` header
- Key endpoints: `create_event`, `run_event`, `get_job_status`
- Job parameters: title, plugin, target, timing, params
- Existing working CLI example in try-cronicle/typer_cli/cli.py

### Typer Best Practices (2025)
- Use `Annotated` syntax for type hints
- Structure with `typer.Typer()` for multi-command apps
- Support configuration via files and environment variables
- Leverage Pydantic for settings management
- Use `add_typer()` for command grouping

## Architecture Overview

### Final Structure Plan
```
calmmage/
├── tools/
│   ├── cronicle_scheduler/        # Component 1
│   │   ├── plugin/
│   │   │   ├── job_executor.py    # Generic job runner
│   │   │   └── plugin_config.pixl # Plugin definition
│   │   └── cli/
│   │       ├── cronicle_manager.py # Add/manage jobs via API
│   │       └── cronicle_client.py  # API wrapper
│   └── local_job_runner/          # Component 2
│       ├── job_runner.py          # Local job executor
│       ├── config.yaml            # Job definitions
│       └── cli.py                 # Local job management
├── scripts/
│   └── scheduled_tasks/           # Actual job scripts
│       ├── daily_backup.py
│       ├── cleanup_temp.py
│       └── data_processing.py
└── resources/
    └── job_templates/             # Sample jobs with configs
        ├── hello_world_job/
        │   ├── job.py
        │   ├── .env
        │   └── config.yaml
        ├── mongodb_test_job/
        │   ├── job.py
        │   └── .env
        └── env_access_job/
            ├── job.py
            └── .env
```

### Usage Scenarios
1. **Direct execution**: `run-local-job daily_backup`
2. **Scheduled via Cronicle**: Cronicle calls `tools/local_job_runner/job_runner.py`
3. **Add to Cronicle**: `add-cronicle-job scripts/scheduled_tasks/backup.py`
4. **Run all local jobs**: `run-all-local-jobs` (scans jobs/ directory)

## Implementation Notes

### Component 1: Cronicle Integration
- Plugin accepts: .env file path, executable path, kwargs
- CLI tool uses existing API patterns from try-cronicle examples
- Support for multiple plugin types (python, shell, typer, arbitrary binaries)

### Component 2: Local Job Runner
- Scans all files in jobs/ directory automatically
- No complex configuration required
- Generates AI-powered summaries of job outputs
- Stores logs in `~/Library/Logs/CalmmageScheduler/`
- Outcome tracking: ok/fail/warning/done_nothing + descriptive text

### Integration Points
- Cronicle can call local job runner as regular Python file
- No special integration needed between components
- Both use Typer for consistent CLI experience
- Shared logging and configuration patterns
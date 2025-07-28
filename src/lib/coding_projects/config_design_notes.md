# Coding Projects Configuration Design

## User Requirements and Issues

**Direct user quote:**
> "so, explain to me how currently the configuration of the utils works? I had pa config yaml for project arranger, listing stuff like destinations etc. How do I pass such info with our new utils? where do i put the yaml config? is it picked up automatically or do I have to pass the path every time? what if the util config needs to be a part of broader app config for some tool? (because there's also other settings)?"

**Direct user quote:**
> "Will each other project using the utils have to explicitly pass all the arguments as well? The point of having src/lib utils in calmmage/ repo is that those utils are environment-aware of calmmage and don't require all the explicitness, because they know the ecosystem's assumptions (and particularly are configurable to the current ecosystem's state / folder structure by a one-time setup. From what you designed, that one-time setup will be a modification of default values in the code... which is actually maybe fine - at least for now. But maybe i'd apreaciate some more explicitness.. actually, i think we can get by like this for now."

## Current Configuration Approach

Currently implemented: **Explicit configuration passing**

```python
# Option 1: Use defaults (hardcoded paths)
projects = get_local_projects()

# Option 2: Use project_arranger config
projects = get_local_projects(config_path=Path("tools/project_arranger/pa_config.yaml"))

# Option 3: Override paths directly  
projects = get_local_projects(root_paths=["~/custom/path1", "~/custom/path2"])
```

**Current defaults:**
```python
DEFAULT_PROJECT_PATHS = [
    "~/work/projects",
    "~/work/archive"
]
```

## Configuration Options Offered

### Option A: Convention-based Discovery
```python
# Automatically looks for: ./config.yaml, ~/.coding_projects.yaml, etc.
projects = get_local_projects()  # auto-discovers config
```

**Pros:** Zero-config for simple cases
**Cons:** Magic behavior, harder to debug

### Option B: Embedded Config Pattern
```python
# Your app config includes coding_projects section
app_config = {
    "coding_projects": {"root_paths": [...], "github_orgs": [...]},
    "other_tool_settings": {...}
}
projects = get_local_projects(config=app_config["coding_projects"])
```

**Pros:** Integrates with broader app configs
**Cons:** Requires config structure standardization

### Option C: Keep Explicit (Current Implementation)
```python
# You always specify where config comes from
projects = get_local_projects(config_path=my_app.config.projects_config_path)
```

**Pros:** Clear, explicit, no magic
**Cons:** Verbose for automation scripts

## Modified Project Arranger Integration

### Current project_arranger workflow:
```python
# tools/project_arranger/src/main.py
class ProjectArranger:
    def __init__(self, config_path: Path, **kwargs):
        self.settings = ProjectArrangerSettings.from_yaml(config_path, **kwargs)
    
    def _build_projets_list_local(self) -> List[Project]:
        # Manual discovery logic with settings.root_paths
```

### Modified workflow using coding_projects utils:
```python
# tools/project_arranger/src/main.py
from src.lib.coding_projects import get_projects_extended

class ProjectArranger:
    def __init__(self, config_path: Path, **kwargs):
        self.settings = ProjectArrangerSettings.from_yaml(config_path, **kwargs)
        self.config_path = config_path
    
    def build_projects_list(self) -> List[Project]:
        # Use shared utilities instead of custom discovery
        return get_projects_extended(
            config_path=self.config_path,
            include_github=True,
            github_orgs=self.settings.github_orgs,
            github_skip_orgs=self.settings.github_skip_orgs
        )
```

## Ecosystem-Aware Design Analysis

**User insight:** "The point of having src/lib utils in calmmage/ repo is that those utils are environment-aware of calmmage and don't require all the explicitness"

### Current Approach: Hardcoded Defaults
- Pros: Zero-config for typical calmmage ecosystem usage
- Cons: Requires code changes for different environments
- Reality: "maybe fine - at least for now"

### Ecosystem-Aware Enhancement Options:

1. **Environment Detection**
```python
def _detect_project_paths():
    """Auto-detect based on calmmage ecosystem conventions"""
    base = Path.home() / "work"
    paths = []
    for candidate in ["projects", "archive", "ai_workspaces"]:
        if (base / candidate).exists():
            paths.append(f"~/work/{candidate}")
    return paths
```

2. **Calmmage Config Convention**
```python
def _load_calmmage_config():
    """Look for calmmage ecosystem config in standard locations"""
    candidates = [
        Path.home() / ".calmmage" / "config.yaml",
        Path.cwd() / "calmmage_config.yaml",
        # Check for project_arranger configs in known locations
    ]
```

3. **One-time Setup Tool**
```python
# uv run python -m src.lib.coding_projects setup
def setup_ecosystem_config():
    """Interactive setup for calmmage ecosystem"""
    # Detect existing folders, ask user to confirm
    # Save config to standard location
```

## Implementation Strategy

**Current state:** Using hardcoded defaults with explicit config override
**Next steps:** 
1. Keep current approach for immediate needs
2. Consider ecosystem-aware enhancements later if needed
3. Monitor how automation tools (UV sync, AI instructions, Git updater) feel with current approach

## Integration Pattern for New Tools

For the three automation tools in `scripts/local_jobs/`:

```python
# scripts/local_jobs/uv_sync_all.py
from src.lib.coding_projects import get_local_projects

def main():
    projects = get_local_projects()  # Uses ecosystem defaults
    for project in projects:
        if (project.path / "pyproject.toml").exists():
            run_uv_sync(project.path)
```

**This achieves the goal:** Simple, environment-aware, minimal configuration for automation scripts.
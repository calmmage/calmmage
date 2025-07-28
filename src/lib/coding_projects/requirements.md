# Shared Coding Projects Library - Requirements

## Project Discovery Unification

### Current Tool Landscape
- **project_arranger**: Configured folder locations → treats subfolders as projects (fast, targeted)
- **project_discoverer**: Whole-disk glob search for git repos, pyproject.toml, etc. (comprehensive, slower)
- **project_manager**: Project creation and management
- **count_repos**: Repository statistics and analysis (uses `discover_local_projects` from drafts)
- **repo_fixer**: Repository utilities

### Existing Discovery Implementations
- **config/dev/draft/pm_v2/shared/repo_discovery.py**: `discover_local_projects()` with caching
- **project_arranger**: Folder-based discovery with GitHub integration
- **project_discoverer**: Comprehensive search with patterns
- **count_repos**: Statistics-focused discovery (imports non-existent `src.lib.lib`)

### Unified Discovery Strategy
- **Default mode**: Fast configured-location approach (like project_arranger)
- **Extended mode** (with flag): Augment with whole-system search (like project_discoverer)
- **Caching**: Required for whole-system approach due to performance
- **Configuration**: Default list of project locations, extensible

## Automation Tools to Build

### Tool 1: UV Environment Updater
- **Purpose**: Go over all discovered projects and run `uv sync`
- **Target**: Update/synchronize UV environments across all repositories
- **Location**: `scripts/local_jobs/` (local automation scripts folder)

### Tool 2: AI Instructions Regenerator  
- **Purpose**: Go over all projects and regenerate AI instruction files
- **Files**: `CLAUDE.md`, `GEMINI.md`, `.cursorrules`
- **Location**: `scripts/local_jobs/` 
- **Integration**: Uses the AI instructions tool we just built

### Tool 3: Git Repository Updater
- **Purpose**: Commit and push staged/unstaged changes across projects
- **Actions**: 
  - Commit current staged changes
  - Stage unstaged changes and commit
  - Push to GitHub/remote repositories
- **Goal**: Bulk GitHub repository updates
- **Location**: `scripts/local_jobs/`

## CLI Interface

### New Unified CLI
- **Challenge**: "project_manager" name already taken
- **Alternatives**: `repo_manager`, `code_manager`, `workspace_manager`, `coding_projects`
- **Purpose**: Showcase shared coding projects utilities
- **Commands**:
  - Project discovery/listing
  - UV environment management
  - AI instructions deployment  
  - Git repository management
  - (Future: additional project utilities)

### Command Structure Ideas
```bash
# Project discovery
<cli> list [--extended]  # List projects (default: configured locations, --extended: whole system)
<cli> discover [query]   # Search for projects matching query

# Automation tools  
<cli> sync-uv [--dry-run]     # Update UV environments
<cli> sync-ai [--mode=optimal] # Regenerate AI instructions  
<cli> sync-git [--dry-run]    # Commit and push repositories

# Project management
<cli> info <project>     # Project information
<cli> open <project>     # Open project (IDE, terminal, etc.)
```

## Implementation Notes

### Shared Base Classes
- ✅ `src/lib/coding_projects/Project` - Base project class (started)
- 🔄 Migrate discovery logic from existing tools
- 🔄 Shared utilities for git operations, size calculation, etc.

### Configuration System
- Unified config format across tools
- Default project locations
- Extensible for different discovery strategies
- Caching configuration for performance

### Integration Points
- Leverage existing tools: `project_arranger`, `project_discoverer`
- Build on AI instructions tool
- Integrate with existing alias system
- Work with current automation framework (`scripts/local_jobs/`)

## Future Considerations
- Project type detection (Python, web, CLI tool, etc.)
- Project health monitoring
- Dependency management across projects  
- Integration with development workflows
- Project archival and cleanup utilities
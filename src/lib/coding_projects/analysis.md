# Project Class Migration Analysis

## ✅ Generalizable (should move to base Project class):

### Core Properties
- `name: str` - ✅ Already moved
- `path: Optional[Path]` - ✅ Already moved  
- `__hash__()` and `__eq__()` methods - ✅ Already moved

### Git Operations
- `is_git_repo()` - Basic git detection
- `get_recent_commit_count()` - Commit counting
- `_extract_repo_info()` - GitHub URL parsing (useful for any git tool)
- Git date utilities: `get_last_commit_date()`, `get_first_commit_date()`

### Size Calculation
- `size` property with async support
- `_async_git_tracked_size()` - Size calculation via git ls-files
- `_async_fallback_size_calculation()` - Fallback size calculation
- File extension filtering (could be configurable)

### Date Properties
- `date` property - Last meaningful change date
- `created_date` property - Project creation date
- Basic date logic (git vs filesystem)

### Path Utilities
- Ignore patterns for size calculation (configurable)
- Source file extension detection (configurable)

## ❌ Project Arranger Specific (should stay):

### GitHub Integration
- `github_repo: Optional[Repository]` - GitHub API object
- GitHub-specific properties: `github_name`, `github_org`
- GitHub API operations

### Display/Formatting
- `size_formatted` property with FORMAT_MODE
- `date_formatted()` with DateFormatSettings
- `format_line()` method - Display formatting

### Project Arranger Logic
- `Group` enum and `current_group` property
- Hardcoded source extensions list
- Hardcoded ignore patterns
- Project arrangement/sorting specific logic

## 🔧 Configurable (could be generalized with config):

### File Patterns
- `__source_extensions` - Could be configurable per tool
- `__ignored_paths` - Could be configurable per tool

### Size Calculation Settings
- Which files to include in size calculation
- Async vs sync calculation preferences

## 📋 Migration Priority:

1. **High Priority**: Git operations, basic date properties, size calculation core
2. **Medium Priority**: Configurable file patterns, path utilities
3. **Low Priority**: Display formatting (tool-specific)

## 🎯 Recommendation:

Start by moving git operations and basic date/size calculation to the base class, keeping GitHub API integration and display formatting in project_arranger specific implementation.
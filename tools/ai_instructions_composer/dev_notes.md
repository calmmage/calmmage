# AI Instructions Tool - Development Notes

## Future Ideas (EXPLICITLY NOT IMPLEMENTED NOW - KEEPING IT SIMPLE)

### Advanced Configuration System
- **Section-level config**: Each section could have source, importance level, repo-type compatibility
- **Sub-configs**: Different configs for different repo types (python, web, cli-tool, etc.)
- **Generalized templating**: Jinja2 or similar for arbitrary section ordering and conditional inclusion
- **Dynamic section discovery**: Auto-detect what sections are relevant for current repo
- **Per-tool customization**: Different section sets for Claude vs Cursor vs Gemini

### Section Metadata System
```python
class Section:
    name: str
    source: str  # file, command, api, etc.
    importance: ImportanceLevel  # critical, helpful, optional
    repo_types: List[str]  # python, web, cli, etc.
    ai_tools: List[str]  # claude, cursor, gemini, all
```

### Repo Type Detection
- Auto-detect repo type from files (package.json, pyproject.toml, etc.)
- Different instruction sets for different project types
- Context-aware tech stack inclusion

## Current Simple Implementation
- 3 instruction modes (slim, optimal, full)
- 3 custom rules positions (start, middle, end)
- Static section list with hard-coded importance levels
- Single config applies to all AI tools equally

**Decision**: Keep it simple for now, add complexity later when patterns emerge from usage.
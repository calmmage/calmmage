# Obsidian Vault Discoveries and Research (AI Work-Along)

## Vault Structure Analysis

### File Tree Discovery
Analyzed the actual Obsidian vault at `/Users/petrlavrov/work/projects/taskzilla-cm/main/root` and found:

**Key Folders:**
- `Inbox/` - Contains many unsorted files including daily notes
- `daily/` - Contains daily notes in various formats
- `templates/` - Template files (lowercase, not "Templates")
- `projects/` - Project files with database metadata
- `archive/`, `files/`, `highlights/`, etc.

**Daily Notes Distribution:**
Daily notes are scattered across multiple locations:
- Root directory: "14 Jul 2025.md"
- `Inbox/` folder: "01 Apr 2025.md", "05 May 2025.md", etc.
- `daily/` folder: Various formats mixed together

### Daily Note Naming Patterns Found

**Target Format (User's Preference):**
- "14 Jul 2025.md" (DD MMM YYYY with spaces)

**Alternative Formats Found:**
- "01 Apr 2025.md" (standard format but in wrong location)
- "11-Feb-2025.md" (dashes instead of spaces)
- "28-Feb-2025.md" (dashes, different variations)
- "12-Dec-2024.md" (older entries with dashes)

**Regex Pattern Needed:**
Current incorrect pattern: `^\\d{4}-\\d{2}-\\d{2}` (YYYY-MM-DD)
Correct pattern needed: `^\\d{1,2} [A-Za-z]{3} \\d{4}` (DD MMM YYYY)

## Database System Discovery

### YAML Frontmatter Structure
Found consistent pattern in project files:

```yaml
---
type: project
status: idea/draft
tags:
---
```

**Database Field Types Identified:**
- `type: project` - Project files
- `type: action` - Action items (referenced in Dataview queries)
- `type: artifact` - Artifacts (referenced in Dataview queries)
- `type: daily` - **MISSING** from daily notes (user wants to add this)

### Dataview Integration
Files use Dataview plugin for querying:

```dataview
TABLE
WHERE type = "action" or type = "artifact"
WHERE contains(project, this.file.link)
SORT created DESC
```

This indicates the database system is actively used for organizing and linking content.

## User Requirements Summary

### Daily Notes Consolidation Goals
1. **Detection**: Identify daily notes by filename pattern (DD MMM YYYY)
2. **Consolidation**:
    - Move all daily notes INTO `daily/` folder
    - Move all non-daily notes OUT OF `daily/` folder
3. **Format Standardization**:
    - Detect alternative naming formats
    - Count and list them (but don't auto-rename due to Obsidian linking conflicts)
4. **Database Field Addition**: Add `type: daily` to daily notes if missing

### Auto-Linking Requirements
**Critical Order:**
1. Count alternative naming formats
2. Auto-link files to daily notes (BEFORE moving - to preserve edit dates)
3. Move files to correct folders

**Auto-Linking Process:**
- Check edit date of files being moved OUT of daily folder
- Find corresponding daily node for that date
- Add Obsidian links `[[filename]]` to that daily note
- Create "## Auto Links" section at end of daily note
- Create daily file if missing

**Obsidian Link Format:** `[[filename]]` (without extension, double square brackets)

## Technical Implementation Challenges

### YAML Frontmatter Manipulation
Need to:
- Parse existing YAML frontmatter
- Add `type: daily` field if missing
- Preserve existing fields and formatting
- Handle files with no frontmatter (create new)

### Date Parsing and Matching
Need robust date parsing to:
- Detect various alternative formats
- Convert edit dates to daily note filenames
- Handle different date representations

### File Operations
Need careful file handling:
- Preserve edit dates before moving
- Handle existing files in target locations
- Maintain Obsidian link integrity

## Research Findings

### Obsidian Tools Library Analysis
**obsidiantools** - Python package for analyzing Obsidian vaults:
- Provides structured metadata access via Pandas dataframes
- NetworkX graph representation of vault connections
- Access to plaintext content including 'source text'
- **Usage**: `import obsidiantools.api as otools; vault = otools.Vault(<VAULT_DIRECTORY>).connect().gather()`

**Alternative YAML Libraries:**
- **python-frontmatter** - Dedicated YAML frontmatter parsing
- **obsidian-plugin-python-bridge** - Direct Python plugin development for Obsidian

**Verdict**: obsidiantools appears suitable for reading vault structure, but may need python-frontmatter for YAML
modification.

### MCP Integration Discovery
**Multiple MCP Servers Available (2025):**
1. **obsidian-claude-code-mcp** - Direct Claude Code integration via WebSocket
2. **smithery-ai/mcp-obsidian** - General MCP client support for Markdown directories
3. **MarkusPfundstein/mcp-obsidian** - Uses Obsidian REST API
4. **jacksteamdev/obsidian-mcp-tools** - Semantic search and Templater integration

**Key Capabilities:**
- Claude Code auto-discovers Obsidian vaults on port 22360
- Dual transport support (WebSocket + HTTP/SSE)
- Direct AI access to vault content and structure
- Standardized protocol for AI-knowledge base integration

**Installation**: `npx @smithery/cli install mcp-obsidian --client claude`

### Technical Implementation Options
**For YAML Frontmatter Modification:**
1. Use python-frontmatter for direct file manipulation
2. Leverage obsidiantools for vault analysis + custom YAML handling
3. Consider MCP integration for AI-assisted content management

**For Date Pattern Detection:**
- Need custom regex: `^\\d{1,2} [A-Za-z]{3} \\d{4}` for DD MMM YYYY format
- Handle alternative formats: dashes, different ordering
- Parse edit dates for auto-linking functionality

## Development Strategy

### Gradual Implementation Approach
User emphasized building step-by-step to understand system behavior and discover requirements through experimentation
rather than full implementation upfront.

**Preferred Process:**
1. Start with simple detection and listing
2. Test and validate behavior
3. Add functionality incrementally
4. Discover edge cases and limitations naturally

### Configuration Management
- Use YAML config files for rules and settings
- Provide setup/discovery mode for templates without rules
- Support both manual configuration and auto-detection

## Current Config Issues Identified

**Templates Path:**
- Config has: `templates_path: Templates`
- Actual folder: `templates/` (lowercase)

**Daily Notes Pattern:**
- Config pattern targets wrong format
- Need to update for DD MMM YYYY detection

**Missing Database Detector:**
User clarified they don't need database detector for this specific task, but will need YAML frontmatter modification
capabilities for adding `type: daily` fields.
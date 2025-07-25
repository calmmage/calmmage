# Python Libraries for Obsidian Research

## Existing Libraries

### 1. obsidiantools (Most Comprehensive)
- **GitHub**: mfarragher/obsidiantools
- **Features**:
    - NetworkX graph of vault connections
    - Pandas dataframes with note metadata
    - Summary stats (backlinks, wikilinks)
    - Network analysis capabilities

```python
import obsidiantools.api as otools
vault = otools.Vault(<VAULT_DIRECTORY>).connect().gather()
```

### 2. Obsidian-Markdown-Parser
- **GitHub**: danymat/Obsidian-Markdown-Parser
- **Features**:
    - Basic parsing library
    - Extract fileName, path, tags, links

```python
from src.Parser import Parser
parser = Parser('/path/to/vault')
```

### 3. obsidian-parser (PyPI)
- **Package**: obsidian-parser
- **Purpose**: Prepare content for static site generators
- **Focus**: Publishing workflows

## Recommendation for Calmlib

Based on research, **obsidiantools** is the most mature option, but we should create our own lightweight utils in
calmlib for:

### Core ObsidianDB Class Features
- Frontmatter parsing (YAML metadata)
- Tag extraction and normalization
- Link/wikilink resolution
- Template matching and detection
- Database field parsing from annotations
- File organization and movement utilities

### Advantages of Custom Implementation
- Tailored to our specific use cases
- Lightweight (no heavy dependencies like NetworkX)
- Direct integration with existing calmlib patterns
- Can build on obsidiantools later if needed

### Planned Structure
```
calmlib/
└── obsidian/
    ├── __init__.py
    ├── vault.py          # Main ObsidianVault class
    ├── parser.py         # Markdown/frontmatter parsing
    ├── database.py       # Database-like query interface
    └── utils.py          # File operations, path resolution
```
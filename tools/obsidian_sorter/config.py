"""Configuration models for Obsidian Sorter."""

from pathlib import Path
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class NodeType(BaseModel):
    """Configuration for a specific node type."""
    folder: str = Field(description="Target folder path (relative to vault root)")
    pattern: Optional[str] = Field(None, description="Regex pattern for filename detection")
    frontmatter_type: Optional[str] = Field(None, description="Expected 'type:' value in YAML frontmatter")
    description: Optional[str] = Field(None, description="Human-readable description")


class SortingRule(BaseModel):
    """Rule for sorting notes based on detected patterns."""
    
    name: str = Field(description="Human-readable name for this rule")
    detector_type: str = Field(description="Type of detector: 'tag', 'template', 'content', 'filename'")
    pattern: str = Field(description="Pattern to match (tag name, template name, regex, etc.)")
    target_folder: Path = Field(description="Target folder relative to obsidian root")
    priority: int = Field(default=0, description="Rule priority (higher = checked first)")


class ObsidianSorterConfig(BaseModel):
    """Configuration for Obsidian auto-sorting."""
    
    obsidian_root: Path = Field(
        default=Path("/Users/petrlavrov/work/projects/taskzilla-cm/main/root"),
        description="Path to Obsidian vault root"
    )
    
    inbox_path: Path = Field(
        default=Path("Inbox"),
        description="Inbox folder path relative to obsidian_root"
    )
    
    templates_path: Optional[Path] = Field(
        default=Path("templates"),
        description="templates folder path relative to obsidian_root"
    )
    
    auto_detect: bool = Field(
        default=True,
        description="Auto-detect note types from existing vault structure"
    )
    
    rules: List[SortingRule] = Field(
        default_factory=list,
        description="List of sorting rules"
    )
    
    dry_run: bool = Field(
        default=False,
        description="Preview changes without actually moving files"
    )

    non_daily_target: Path = Field(
        default=Path("Inbox"),
        description="Where to move non-daily notes from daily folder (relative to obsidian_root)",
    )
    
    # Node type definitions with their target folders  
    node_types: Dict[str, NodeType] = Field(default_factory=lambda: {
        "daily": NodeType(
            folder="daily",
            pattern=r"^\d{1,2} [A-Za-z]{3} \d{4}\.md$",
            frontmatter_type="daily",
            description="Daily notes in DD MMM YYYY format"
        ),
        "weekly_note": NodeType(
            folder="weekly_workspaces", 
            pattern=r"^Week \d+ - \d{1,2} [A-Za-z]{3} \d{4}\.md$",
            frontmatter_type="weekly_note",
            description="Weekly notes in Week N - DD MMM YYYY format"
        ),
        "project": NodeType(
            folder="projects",
            frontmatter_type="project",
            description="Project files with type: project in frontmatter"
        ),
        "action": NodeType(
            folder="actions",
            frontmatter_type="action", 
            description="Action items with type: action in frontmatter"
        ),
        "troubleshooting": NodeType(
            folder="troubleshooting",
            frontmatter_type="troubleshooting",
            description="Troubleshooting notes"
        ),
        "work_session": NodeType(
            folder="work/sessions",
            frontmatter_type="work_session",
            description="Work session notes"
        ),
        "thoughts_dump": NodeType(
            folder="notes/thoughts",
            frontmatter_type="thoughts_dump",
            description="Thought dump notes"
        ),
        "person_contact": NodeType(
            folder="people/contacts",
            frontmatter_type="person_contact",
            description="Contact person notes"
        ),
        "workalong": NodeType(
            folder="notes/workalongs",
            frontmatter_type="workalong",
            description="AI workalong notes"
        ),
        "artifact": NodeType(
            folder="artifacts",
            frontmatter_type="artifact",
            description="Artifact notes"
        ),
        "chain": NodeType(
            folder="chains",
            frontmatter_type="chain",
            description="Chain notes"
        )
    })
    
    @property
    def full_inbox_path(self) -> Path:
        """Get absolute path to inbox folder."""
        return self.obsidian_root / self.inbox_path
    
    @property
    def full_templates_path(self) -> Optional[Path]:
        """Get absolute path to templates folder."""
        if self.templates_path:
            return self.obsidian_root / self.templates_path
        return None
    
    def get_target_path(self, rule: SortingRule) -> Path:
        """Get absolute path for a rule's target folder."""
        return self.obsidian_root / rule.target_folder
    
    def get_node_type_path(self, node_type_name: str) -> Path:
        """Get absolute path for a node type's target folder."""
        if node_type_name not in self.node_types:
            raise ValueError(f"Unknown node type: {node_type_name}")
        return self.obsidian_root / self.node_types[node_type_name].folder
    
    def detect_node_type_by_filename(self, filename: str) -> Optional[str]:
        """Detect node type based on filename patterns."""
        for type_name, node_type in self.node_types.items():
            if node_type.pattern:
                import re
                if re.match(node_type.pattern, filename):
                    return type_name
        return None
    
    def detect_node_type_by_frontmatter(self, frontmatter_type: str) -> Optional[str]:
        """Find node type that matches a frontmatter type value."""
        for type_name, node_type in self.node_types.items():
            if node_type.frontmatter_type == frontmatter_type:
                return type_name
        return None
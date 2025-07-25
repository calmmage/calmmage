"""Configuration models for Obsidian Sorter."""

from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field


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
        default=Path("Templates"),
        description="Templates folder path relative to obsidian_root"
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
"""Note type detection for Obsidian sorting."""

import re
from pathlib import Path
from typing import List, Dict, Any
import yaml


def parse_frontmatter(content: str) -> Dict[str, Any]:
    """Parse YAML frontmatter from note content."""
    if not content.startswith("---"):
        return {}
    
    try:
        # Find the end of frontmatter
        end_marker = content.find("---", 3)
        if end_marker == -1:
            return {}
        
        frontmatter_text = content[3:end_marker].strip()
        return yaml.safe_load(frontmatter_text) or {}
    except Exception:
        return {}


def extract_tags(frontmatter: Dict[str, Any], content: str) -> List[str]:
    """Extract tags from frontmatter and content."""
    tags = set()
    
    # Tags from frontmatter
    if "tags" in frontmatter:
        tag_value = frontmatter["tags"]
        if isinstance(tag_value, list):
            tags.update(tag_value)
        elif isinstance(tag_value, str):
            tags.add(tag_value)
    
    # Inline tags from content (e.g., #tag)
    inline_tags = re.findall(r'#(\w+)', content)
    tags.update(inline_tags)
    
    return list(tags)


class NoteDetector:
    """Base class for note type detection."""
    
    def __init__(self, config):
        self.config = config
    
    def detect(self, note_path: Path, content: str, frontmatter: Dict[str, Any]) -> bool:
        """Return True if this detector matches the note."""
        raise NotImplementedError


class TagDetector(NoteDetector):
    """Detect notes based on tags."""
    
    def __init__(self, config, pattern: str):
        super().__init__(config)
        self.target_tag = pattern
    
    def detect(self, note_path: Path, content: str, frontmatter: Dict[str, Any]) -> bool:
        tags = extract_tags(frontmatter, content)
        return self.target_tag in tags


class TemplateDetector(NoteDetector):
    """Detect notes based on template usage."""
    
    def __init__(self, config, pattern: str):
        super().__init__(config)
        self.template_name = pattern
    
    def detect(self, note_path: Path, content: str, frontmatter: Dict[str, Any]) -> bool:
        # Check if template is referenced in frontmatter
        if "template" in frontmatter:
            return frontmatter["template"] == self.template_name
        
        # Check if content matches template structure
        if self.config.full_templates_path:
            template_path = self.config.full_templates_path / f"{self.template_name}.md"
            if template_path.exists():
                template_content = template_path.read_text()
                # Simple similarity check - could be more sophisticated
                template_lines = [line.strip() for line in template_content.split('\n') if line.strip()]
                content_lines = [line.strip() for line in content.split('\n') if line.strip()]
                
                # Check if template structure is present
                matches = 0
                for template_line in template_lines[:5]:  # Check first 5 lines
                    if template_line in content_lines:
                        matches += 1
                
                return matches >= 2  # At least 2 template lines match
        
        return False


class ContentDetector(NoteDetector):
    """Detect notes based on content patterns."""
    
    def __init__(self, config, pattern: str):
        super().__init__(config)
        self.pattern = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
    
    def detect(self, note_path: Path, content: str, frontmatter: Dict[str, Any]) -> bool:
        return bool(self.pattern.search(content))


class FilenameDetector(NoteDetector):
    """Detect notes based on filename patterns."""
    
    def __init__(self, config, pattern: str):
        super().__init__(config)
        self.pattern = re.compile(pattern, re.IGNORECASE)
    
    def detect(self, note_path: Path, content: str, frontmatter: Dict[str, Any]) -> bool:
        return bool(self.pattern.search(note_path.name))


def create_detector(config, detector_type: str, pattern: str) -> NoteDetector:
    """Factory function to create appropriate detector."""
    detectors = {
        "tag": TagDetector,
        "template": TemplateDetector,
        "content": ContentDetector,
        "filename": FilenameDetector
    }
    
    if detector_type not in detectors:
        raise ValueError(f"Unknown detector type: {detector_type}")
    
    return detectors[detector_type](config, pattern)


def auto_detect_note_types(config) -> List[str]:
    """Auto-detect existing note types from vault structure."""
    note_types = set()
    
    # Scan existing folder structure
    for folder in config.obsidian_root.iterdir():
        if folder.is_dir() and folder.name not in ["Inbox", "Templates", ".obsidian"]:
            note_types.add(folder.name)
    
    # Scan templates if available
    if config.full_templates_path and config.full_templates_path.exists():
        for template in config.full_templates_path.glob("*.md"):
            note_types.add(template.stem)
    
    return sorted(note_types)
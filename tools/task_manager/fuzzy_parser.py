#!/usr/bin/env python3
"""
Fuzzy parser for markdown-style task lists.
Maintains backward mapping from items to their location in text.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict
from pathlib import Path
import yaml


@dataclass
class TextLocation:
    """Represents a location in the source text."""
    file_path: str
    line_start: int
    line_end: int
    char_start: int
    char_end: int
    
    def __str__(self):
        return f"{self.file_path}:{self.line_start}-{self.line_end}"


@dataclass
class TaskItem:
    """Represents a task item with its content and metadata."""
    content: str
    is_done: bool = False
    indent_level: int = 0
    sub_items: List['TaskItem'] = field(default_factory=list)
    location: Optional[TextLocation] = None
    parent: Optional['TaskItem'] = None
    
    def __hash__(self):
        # Use id for hashing since we want object identity
        return hash(id(self))
    
    def __str__(self, indent=0):
        prefix = "  " * indent
        status = "[x]" if self.is_done else "[ ]"
        result = f"{prefix}{status} {self.content}"
        if self.location:
            result += f" @ {self.location}"
        for sub in self.sub_items:
            result += "\n" + sub.__str__(indent + 1)
        return result
    
    def to_dict(self):
        """Convert to dictionary for easier inspection."""
        return {
            'content': self.content,
            'is_done': self.is_done,
            'indent_level': self.indent_level,
            'location': str(self.location) if self.location else None,
            'sub_items': [sub.to_dict() for sub in self.sub_items]
        }


class FuzzyTaskParser:
    """Parser for markdown-style task lists with fuzzy matching."""
    
    def __init__(self):
        self.backward_mapping: Dict[TaskItem, TextLocation] = {}
        
    def parse_file(self, file_path: str) -> List[TaskItem]:
        """Parse a markdown file and extract task items."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return self.parse_content(content, file_path)
    
    def parse_content(self, content: str, file_path: str = "unknown") -> List[TaskItem]:
        """Parse markdown content and extract task items."""
        # Split by double newlines or --- separators
        sections = re.split(r'\n\n+|^---+$', content, flags=re.MULTILINE)
        
        all_items = []
        char_offset = 0
        
        for section in sections:
            if not section.strip():
                char_offset += len(section) + 2  # Account for the separator
                continue
                
            items = self._parse_section(section, file_path, char_offset)
            all_items.extend(items)
            char_offset += len(section) + 2  # Account for the separator
            
        return all_items
    
    def _parse_section(self, section: str, file_path: str, char_offset: int) -> List[TaskItem]:
        """Parse a single section for task items."""
        lines = section.split('\n')
        items = []
        current_parent_stack = []  # Stack to track parent items at each indent level
        
        line_offset = 0
        for line_num, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                line_offset += len(line) + 1
                continue
                
            # Check if it's a list item
            match = re.match(r'^(-|\*|\d+\.)\s*(\[[ x]\])?\s*(.+)$', stripped)
            if not match:
                line_offset += len(line) + 1
                continue
                
            # Calculate indent level
            indent_level = (len(line) - len(line.lstrip())) // 2
            
            # Extract item info
            bullet = match.group(1)
            checkbox = match.group(2)
            content = match.group(3)
            
            is_done = checkbox == '[x]' if checkbox else False
            
            # Create location info
            char_start = char_offset + line_offset
            char_end = char_start + len(line)
            location = TextLocation(
                file_path=file_path,
                line_start=line_num + 1,
                line_end=line_num + 1,
                char_start=char_start,
                char_end=char_end
            )
            
            # Create task item
            item = TaskItem(
                content=content,
                is_done=is_done,
                indent_level=indent_level,
                location=location
            )
            
            # Update backward mapping
            self.backward_mapping[item] = location
            
            # Handle parent-child relationships
            # Pop items from stack until we find the right parent level
            while current_parent_stack and current_parent_stack[-1][0] >= indent_level:
                current_parent_stack.pop()
                
            if current_parent_stack:
                # This is a sub-item
                parent_item = current_parent_stack[-1][1]
                parent_item.sub_items.append(item)
                item.parent = parent_item
            else:
                # This is a top-level item
                items.append(item)
                
            # Add current item to stack
            current_parent_stack.append((indent_level, item))
            
            line_offset += len(line) + 1
            
        return items
    
    def get_location(self, item: TaskItem) -> Optional[TextLocation]:
        """Get the text location for a given task item."""
        return self.backward_mapping.get(item)
    
    def print_items(self, items: List[TaskItem]):
        """Pretty print task items."""
        for item in items:
            print(item)
            print()


def main():
    """Main function to demonstrate the parser."""
    # Load config
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    parser = FuzzyTaskParser()
    
    # Parse all source files
    all_items = []
    for source_file in config['item_source_locations']:
        # Handle paths relative to workspace root
        if source_file.startswith('/'):
            file_path = Path(source_file)
        else:
            # Go up to workspace root
            workspace_root = Path(__file__).parent.parent.parent
            file_path = workspace_root / source_file
        
        print(f"\n=== Parsing: {source_file} ===\n")
        
        try:
            items = parser.parse_file(str(file_path))
            all_items.extend(items)
            parser.print_items(items)
        except FileNotFoundError:
            print(f"Warning: File not found: {file_path}")
            continue
    
    # Print summary
    print(f"\n=== Summary ===")
    print(f"Total top-level items: {len(all_items)}")
    
    done_count = sum(1 for item in all_items if item.is_done)
    print(f"Completed items: {done_count}")
    print(f"Pending items: {len(all_items) - done_count}")
    
    # Count all items including sub-items
    def count_all_items(items):
        count = len(items)
        for item in items:
            count += count_all_items(item.sub_items)
        return count
    
    total_all = count_all_items(all_items)
    print(f"Total items (including sub-items): {total_all}")


if __name__ == "__main__":
    main()
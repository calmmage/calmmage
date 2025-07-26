"""Core Obsidian note sorting logic."""

import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

from .config import ObsidianSorterConfig, SortingRule
from .detectors import parse_frontmatter, create_detector


@dataclass
class SortingResult:
    """Result of sorting operation."""
    source_path: Path
    target_path: Optional[Path]
    rule_name: Optional[str]
    success: bool
    error: Optional[str] = None


class ObsidianSorter:
    """Main obsidian note sorting class."""
    
    def __init__(self, config: ObsidianSorterConfig):
        self.config = config
        self.results: List[SortingResult] = []
    
    def find_inbox_files(self) -> List[Path]:
        """Find all markdown files in the inbox."""
        inbox_path = self.config.full_inbox_path
        
        if not inbox_path.exists():
            return []
        
        return list(inbox_path.glob("*.md"))
    
    def analyze_note(self, note_path: Path) -> Tuple[str, Dict, List[str]]:
        """Analyze a note and return content, frontmatter, and tags."""
        try:
            content = note_path.read_text(encoding='utf-8')
            frontmatter = parse_frontmatter(content)
            
            return content, frontmatter, []
        except Exception as e:
            print(f"⚠️  Warning: Could not read {note_path}: {e}")
            return "", {}, []
    
    def find_matching_rule(self, note_path: Path, content: str, frontmatter: Dict) -> Optional[SortingRule]:
        """Find the first matching rule for a note."""
        # Sort rules by priority (descending)
        sorted_rules = sorted(self.config.rules, key=lambda r: r.priority, reverse=True)
        
        for rule in sorted_rules:
            try:
                detector = create_detector(self.config, rule.detector_type, rule.pattern)
                if detector.detect(note_path, content, frontmatter):
                    return rule
            except Exception as e:
                print(f"⚠️  Warning: Rule '{rule.name}' failed: {e}")
                continue
        
        return None
    
    def sort_note(self, note_path: Path) -> SortingResult:
        """Sort a single note."""
        content, frontmatter, _ = self.analyze_note(note_path)
        
        # Find matching rule
        rule = self.find_matching_rule(note_path, content, frontmatter)
        
        if not rule:
            return SortingResult(
                source_path=note_path,
                target_path=None,
                rule_name=None,
                success=False,
                error="No matching rule found"
            )
        
        # Calculate target path
        target_folder = self.config.get_target_path(rule)
        target_path = target_folder / note_path.name
        
        # Check if target already exists
        if target_path.exists():
            return SortingResult(
                source_path=note_path,
                target_path=target_path,
                rule_name=rule.name,
                success=False,
                error=f"Target file already exists: {target_path}"
            )
        
        # Create target directory if needed
        if not self.config.dry_run:
            target_folder.mkdir(parents=True, exist_ok=True)
        
        # Move the file
        try:
            if self.config.dry_run:
                print(f"[DRY RUN] Would move: {note_path} → {target_path}")
            else:
                shutil.move(str(note_path), str(target_path))
                print(f"Moved: {note_path.name} → {rule.target_folder}")
            
            return SortingResult(
                source_path=note_path,
                target_path=target_path,
                rule_name=rule.name,
                success=True
            )
            
        except Exception as e:
            return SortingResult(
                source_path=note_path,
                target_path=target_path,
                rule_name=rule.name,
                success=False,
                error=str(e)
            )
    
    def sort_all(self) -> List[SortingResult]:
        """Sort all notes in inbox."""
        inbox_files = self.find_inbox_files()
        
        if not inbox_files:
            print("📭 No files found in inbox")
            return []
        
        print(f"📨 Found {len(inbox_files)} files in inbox")
        
        self.results = []
        for note_path in inbox_files:
            result = self.sort_note(note_path)
            self.results.append(result)
        
        return self.results
    
    def get_summary(self) -> Dict[str, int]:
        """Get summary statistics of sorting operation."""
        summary = {
            "total": len(self.results),
            "success": sum(1 for r in self.results if r.success),
            "failed": sum(1 for r in self.results if not r.success),
            "no_rule": sum(1 for r in self.results if not r.success and "No matching rule" in (r.error or "")),
            "exists": sum(1 for r in self.results if not r.success and "already exists" in (r.error or "")),
        }
        return summary
    
    def print_results(self) -> None:
        """Print detailed results of sorting operation."""
        if not self.results:
            print("No sorting operations performed")
            return
        
        summary = self.get_summary()
        
        print("\n📊 Sorting Results:")
        print(f"  Total files processed: {summary['total']}")
        print(f"  ✅ Successfully sorted: {summary['success']}")
        print(f"  ❌ Failed: {summary['failed']}")
        
        if summary['no_rule'] > 0:
            print(f"  📋 No matching rule: {summary['no_rule']}")
        
        if summary['exists'] > 0:
            print(f"  📁 Target exists: {summary['exists']}")
        
        # Show failed operations
        failed_results = [r for r in self.results if not r.success]
        if failed_results:
            print("\n❌ Failed Operations:")
            for result in failed_results:
                print(f"  • {result.source_path.name}: {result.error}")
    
    def generate_status_output(self) -> Tuple[str, str]:
        """Generate FINAL_STATUS and FINAL_NOTES output for local_job_runner."""
        summary = self.get_summary()
        
        # Status contains ONLY the status keyword
        if summary['total'] == 0:
            status = "no_change"
            notes = "No files found in inbox to sort"
        elif summary['success'] == summary['total']:
            status = "success"
            notes = f"Sorted {summary['success']} files successfully"
        elif summary['success'] > 0:
            status = "success"  # Partial success is still success
            notes = f"Sorted {summary['success']} of {summary['total']} files successfully"
        else:
            status = "fail"
            notes = f"Failed to sort any of {summary['total']} files"
        
        return status, notes
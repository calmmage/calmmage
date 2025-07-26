#!/usr/bin/env python3
"""
Check implementation status of projects mentioned in outstanding items.
"""

from pathlib import Path
import yaml
from fuzzy_parser import FuzzyTaskParser, TaskItem
from typing import Dict, List, Tuple


def check_project_status(project_name: str, search_dirs: List[Path]) -> Tuple[bool, str]:
    """
    Check if a project is implemented by looking for its directory and files.
    Returns (is_implemented, details)
    """
    # Special case for the task management tool we're building
    if project_name.lower() in ['task management tool', 'a tool for managing outstanding ideas lists / items (like this one)']:
        return True, "✅ Currently being implemented in tools/task_manager 🚧"
    
    # Normalize project name for directory search
    normalized_names = [
        project_name.lower().replace(' ', '_'),
        project_name.lower().replace(' ', '-'),
        project_name.lower().replace('/', '_'),
        project_name.lower().replace(' / ', '_'),
    ]
    
    for search_dir in search_dirs:
        for name in normalized_names:
            project_path = search_dir / name
            if project_path.exists() and project_path.is_dir():
                # Check for implementation files
                impl_files = list(project_path.glob('*.py')) + \
                            list(project_path.glob('*.js')) + \
                            list(project_path.glob('*.ts'))
                
                has_readme = (project_path / 'README.md').exists()
                has_main = any(f.name in ['main.py', 'run.py', 'index.js', 'index.ts'] 
                              for f in impl_files)
                
                workspace_root = Path(__file__).parent.parent.parent
                
                if impl_files:
                    status = f"✅ Implemented in {project_path.relative_to(workspace_root)}"
                    if has_readme:
                        status += " (has README)"
                    if has_main:
                        status += " (has main script)"
                    return True, status
                elif (project_path / 'idea.md').exists():
                    return False, f"💡 Idea only in {project_path.relative_to(workspace_root)}"
                else:
                    return False, f"📁 Empty directory at {project_path.relative_to(workspace_root)}"
    
    return False, "❌ Not found"


def extract_project_name(item: TaskItem) -> str:
    """Extract a clean project name from task item content."""
    content = item.content
    # Remove common prefixes
    for prefix in ['Implement ', 'Create ', 'Build ', 'Develop ']:
        if content.startswith(prefix):
            content = content[len(prefix):]
    
    # Remove file paths and extra info after dashes
    if ' - ' in content:
        content = content.split(' - ')[0]
    
    return content.strip()


def main():
    """Main function to check implementation status."""
    # Load config
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    parser = FuzzyTaskParser()
    
    # Directories to search for implementations
    workspace_root = Path(__file__).parent.parent.parent
    search_dirs = [
        workspace_root / 'tools',
        workspace_root / 'experiments' / 'season_4_jun_2025',
        workspace_root / 'src',
        workspace_root / 'calmlib',
    ]
    
    print("=== Project Implementation Status ===\n")
    
    # Parse all source files
    all_projects = {}
    
    for source_file in config['item_source_locations']:
        # Handle paths relative to workspace root
        if source_file.startswith('/'):
            file_path = Path(source_file)
        else:
            workspace_root = Path(__file__).parent.parent.parent
            file_path = workspace_root / source_file
        
        if not file_path.exists():
            continue
            
        items = parser.parse_file(str(file_path))
        
        # Extract project-like items
        for item in items:
            project_name = extract_project_name(item)
            if project_name and len(project_name) > 3:  # Filter out very short items
                if project_name not in all_projects:
                    all_projects[project_name] = {
                        'item': item,
                        'sources': []
                    }
                all_projects[project_name]['sources'].append(source_file)
    
    # Check implementation status
    implemented_count = 0
    total_count = len(all_projects)
    
    for project_name, project_info in sorted(all_projects.items()):
        is_implemented, status = check_project_status(project_name, search_dirs)
        if is_implemented:
            implemented_count += 1
        
        print(f"{project_name}:")
        print(f"  Status: {status}")
        print(f"  Sources: {', '.join(project_info['sources'])}")
        if project_info['item'].sub_items:
            print(f"  Sub-tasks: {len(project_info['item'].sub_items)}")
        print()
    
    # Summary
    print(f"\n=== Summary ===")
    print(f"Total projects: {total_count}")
    print(f"Implemented: {implemented_count}")
    print(f"Not implemented: {total_count - implemented_count}")
    print(f"Implementation rate: {implemented_count/total_count*100:.1f}%")


if __name__ == "__main__":
    main()
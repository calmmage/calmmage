#!/usr/bin/env python3
"""Quick test script for coding_projects utilities."""

from src.lib.coding_projects import get_local_projects, get_projects_extended, find_project

def main():
    print("🧪 Testing coding_projects utilities...\n")
    
    # Test 1: Basic discovery
    print("1. Testing get_local_projects():")
    projects = get_local_projects()
    print(f"   Found {len(projects)} projects")
    for i, project in enumerate(projects[:5]):  # Show first 5
        print(f"   {i+1}. {project.name} -> {project.path}")
    if len(projects) > 5:
        print(f"   ... and {len(projects) - 5} more")
    print()
    
    # Test 2: Find specific project
    print("2. Testing find_project():")
    test_name = projects[0].name if projects else "nonexistent"
    found = find_project(test_name)
    if found:
        print(f"   ✅ Found '{test_name}' at {found.path}")
    else:
        print(f"   ❌ Could not find '{test_name}'")
    print()
    
    # Test 3: Extended discovery (without GitHub for speed)
    print("3. Testing get_projects_extended() (no GitHub):")
    extended = get_projects_extended(include_github=False)
    print(f"   Found {len(extended)} projects (should match basic discovery)")
    print()
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    main()
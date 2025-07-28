#!/usr/bin/env python3
"""AI instructions sync automation job - deploy AI configurations to all projects."""

import sys
from pathlib import Path

from src.lib.coding_projects import get_local_projects
from tools.ai_instructions_composer.cli import deploy_ai_instructions


def detect_project_languages(project_path: Path) -> dict:
    """Detect programming languages used in a project.
    
    Returns:
        dict with 'supported' and 'unsupported' language lists
    """
    language_indicators = {
        # Supported languages (have AI instructions)
        "python": ["pyproject.toml", "setup.py", "requirements.txt", "*.py"],
        
        # Unsupported languages (need custom AI instructions)
        "javascript": ["package.json", "*.js", "*.ts", "*.jsx", "*.tsx"],
        "rust": ["Cargo.toml", "*.rs"],
        "go": ["go.mod", "*.go"],
        "java": ["pom.xml", "build.gradle", "*.java"],
        "c++": ["CMakeLists.txt", "*.cpp", "*.hpp", "*.cc"],
        "c": ["Makefile", "*.c", "*.h"],
        "swift": ["Package.swift", "*.swift"],
        "kotlin": ["build.gradle.kts", "*.kt"],
        "php": ["composer.json", "*.php"],
        "ruby": ["Gemfile", "*.rb"],
        "shell": ["*.sh", "*.bash", "*.zsh"]
    }
    
    supported_languages = {"python"}  # Languages we have AI instructions for
    detected_supported = []
    detected_unsupported = []
    
    for language, indicators in language_indicators.items():
        found = False
        for indicator in indicators:
            if indicator.startswith("*."):
                # Check for file extensions
                pattern = indicator
                if list(project_path.glob(pattern)) or list(project_path.glob(f"**/{pattern}")):
                    found = True
                    break
            else:
                # Check for specific files/directories
                if (project_path / indicator).exists():
                    found = True
                    break
        
        if found:
            if language in supported_languages:
                detected_supported.append(language)
            else:
                detected_unsupported.append(language)
    
    return {
        "supported": detected_supported,
        "unsupported": detected_unsupported
    }


def should_deploy_ai_instructions(project_path: Path) -> bool:
    """Check if project should receive AI instructions deployment."""
    # Skip if project already has custom LLM_RULES.md
    if (project_path / "LLM_RULES.md").exists():
        return False
    
    # Deploy to projects that look like code projects
    code_indicators = [
        "pyproject.toml",
        "package.json", 
        "Cargo.toml",
        "go.mod",
        "pom.xml",
        "Makefile",
        "src/",
        "lib/",
        ".git/"
    ]
    
    return any((project_path / indicator).exists() for indicator in code_indicators)


def deploy_to_project(project_path: Path) -> tuple[bool, dict]:
    """Deploy AI instructions to a single project.
    
    Args:
        project_path: Path to the project
        
    Returns:
        tuple of (success: bool, language_info: dict)
    """
    try:
        # Detect languages before deployment
        languages = detect_project_languages(project_path)
        
        # Warn about unsupported languages
        if languages["unsupported"]:
            unsupported_str = ", ".join(languages["unsupported"])
            print(f"  ⚠️  {project_path.name}: Detected unsupported languages: {unsupported_str}")
            print(f"     Consider creating custom AI instructions for these languages")
        
        # Use the AI instructions tool with optimal mode
        deploy_ai_instructions(
            target_dir=project_path,
            mode="optimal",
            custom_rules_position="end",
            force=True  # Overwrite existing files
        )
        
        supported_str = ", ".join(languages["supported"]) if languages["supported"] else "none"
        print(f"  ✅ AI instructions deployed: {project_path.name} (supported: {supported_str})")
        return True, languages
        
    except Exception as e:
        print(f"  ❌ AI instructions failed: {project_path.name}")
        print(f"     Error: {e}")
        return False, {"supported": [], "unsupported": []}


def main():
    """Deploy AI instructions across all discovered projects."""
    print("🎯 FINAL STATUS: Starting AI instructions sync across all projects")
    
    try:
        projects = get_local_projects()
        target_projects = [p for p in projects if should_deploy_ai_instructions(p.path)]
        
        print(f"Found {len(target_projects)} projects needing AI instructions out of {len(projects)} total")
        
        if not target_projects:
            print("🎯 FINAL STATUS: success - No projects need AI instructions")
            print("📝 FINAL NOTES: All projects either have custom LLM_RULES.md or are not code projects")
            return 0
        
        success_count = 0
        projects_with_unsupported = 0
        all_unsupported_languages = set()
        
        for project in target_projects:
            print(f"Deploying AI instructions to {project.name}...")
            success, languages = deploy_to_project(project.path)
            if success:
                success_count += 1
            if languages["unsupported"]:
                projects_with_unsupported += 1
                all_unsupported_languages.update(languages["unsupported"])
        
        # Determine final status
        if success_count == len(target_projects):
            if projects_with_unsupported > 0:
                print("🎯 FINAL STATUS: requires_attention - All deployed but some have unsupported languages")
            else:
                print("🎯 FINAL STATUS: success - All projects updated with AI instructions")
        elif success_count == 0:
            print("🎯 FINAL STATUS: fail - No projects successfully updated")
        else:
            print("🎯 FINAL STATUS: requires_attention - Some projects failed to update")
        
        # Enhanced FINAL NOTES with language statistics
        notes = f"Processed {len(target_projects)} projects, {success_count} successful deployments"
        if projects_with_unsupported > 0:
            unsupported_list = ", ".join(sorted(all_unsupported_languages))
            notes += f", {projects_with_unsupported} projects with unsupported languages ({unsupported_list})"
        print(f"📝 FINAL NOTES: {notes}")
        return 0
        
    except Exception as e:
        print(f"🎯 FINAL STATUS: fail - AI instructions sync failed: {e}")
        print("📝 FINAL NOTES: Check AI instructions tool and project discovery")
        return 1


if __name__ == "__main__":
    sys.exit(main())
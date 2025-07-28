#!/usr/bin/env python3
"""AI instructions sync automation job - deploy AI configurations to all projects."""

import sys
from pathlib import Path

from src.lib.coding_projects import get_local_projects
from tools.ai_instructions_composer.cli import (
    deploy_ai_instructions,
    InstructionMode,
    CustomRulesPosition,
)


# def detect_project_languages(project_path: Path) -> dict:
#     """Detect programming languages used in a project.
#
#     Returns:
#         dict with 'supported' and 'unsupported' language lists
#     """
#     language_indicators = {
#         # Supported languages (have AI instructions)
#         "python": ["pyproject.toml", "setup.py", "requirements.txt", "*.py"],
#
#         # Unsupported languages (need custom AI instructions)
#         "javascript": ["package.json", "*.js", "*.ts", "*.jsx", "*.tsx"],
#         "rust": ["Cargo.toml", "*.rs"],
#         "go": ["go.mod", "*.go"],
#         "java": ["pom.xml", "build.gradle", "*.java"],
#         "c++": ["CMakeLists.txt", "*.cpp", "*.hpp", "*.cc"],
#         "c": ["Makefile", "*.c", "*.h"],
#         "swift": ["Package.swift", "*.swift"],
#         "kotlin": ["build.gradle.kts", "*.kt"],
#         "php": ["composer.json", "*.php"],
#         "ruby": ["Gemfile", "*.rb"],
#         "shell": ["*.sh", "*.bash", "*.zsh"]
#     }
#
#     supported_languages = {"python"}  # Languages we have AI instructions for
#     detected_supported = []
#     detected_unsupported = []
#
#     for language, indicators in language_indicators.items():
#         found = False
#         for indicator in indicators:
#             if indicator.startswith("*."):
#                 # Check for file extensions
#                 pattern = indicator
#                 if list(project_path.glob(pattern)) or list(project_path.glob(f"**/{pattern}")):
#                     found = True
#                     break
#             else:
#                 # Check for specific files/directories
#                 if (project_path / indicator).exists():
#                     found = True
#                     break
#
#         if found:
#             if language in supported_languages:
#                 detected_supported.append(language)
#             else:
#                 detected_unsupported.append(language)
#
#     return {
#         "supported": detected_supported,
#         "unsupported": detected_unsupported
#     }


def should_deploy_ai_instructions(project_path: Path) -> bool:
    """Check if project should receive AI instructions deployment."""
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


def deploy_to_project(project_path: Path) -> tuple[bool, int]:
    """Deploy AI instructions to a single project.
    
    Args:
        project_path: Path to the project
        
    Returns:
        tuple of (success: bool, files_deployed: int)
    """
    try:
        # Use the reusable deployment function
        result = deploy_ai_instructions(
            target_dir=project_path,
            tools=None,  # Deploy all tools
            include_tech_stack=True,
            mode=InstructionMode.OPTIMAL,
            custom_position=CustomRulesPosition.END,
            force_overwrite=True,  # Automation overwrites without asking
            silent=True  # No console output for automation
        )
        
        print(f"  ✅ AI instructions deployed: {project_path.name} ({result.tools_deployed} tools)")
        return True, result.tools_deployed
        
    except Exception as e:
        print(f"  ❌ AI instructions failed: {project_path.name}")
        print(f"     Error: {e}")
        return False, 0


def main():
    """Deploy AI instructions across all discovered projects."""
    try:
        projects = get_local_projects()
        target_projects = [p for p in projects if should_deploy_ai_instructions(p.path)]
        
        print(f"Found {len(target_projects)} projects needing AI instructions out of {len(projects)} total")
        
        if not target_projects:
            print("🎯 FINAL STATUS: no_change")
            print("📝 FINAL NOTES: No code projects found")
            return 0
        
        # Filter out archived projects first
        archive_path = Path.home() / "work/archive"
        non_archived_projects = [p for p in target_projects if archive_path not in p.path.parents]
        
        success_count = 0
        total_tools_deployed = 0

        for project in non_archived_projects:
            print(f"Deploying AI instructions to {project.name}...")
            success, tools_deployed = deploy_to_project(project.path)
            if success:
                success_count += 1
                total_tools_deployed += tools_deployed
        
        # Determine final status
        if success_count == len(non_archived_projects):
            print("🎯 FINAL STATUS: success")
        elif success_count == 0:
            if len(non_archived_projects) == 0:
                print("🎯 FINAL STATUS: no_change")
            else:
                print("🎯 FINAL STATUS: fail")
        else:
            print("🎯 FINAL STATUS: requires_attention")
        
        # Count active (non-archived) projects
        archive_path = Path.home() / "work/archive"
        active_projects = [p for p in target_projects if archive_path not in p.path.parents]
        
        # Concise final notes
        notes = f"{len(active_projects)} projects, {success_count} deployed, {total_tools_deployed} tools"
        print(f"📝 FINAL NOTES: {notes}")
        return 0
        
    except Exception as e:
        print(f"❌ Error during AI instructions sync: {e}")
        print(f"🎯 FINAL STATUS: fail")
        print(f"📝 FINAL NOTES: {type(e).__name__} - check logs")
        return 1


if __name__ == "__main__":
    sys.exit(main())
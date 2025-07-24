#!/usr/bin/env python3
"""
System Stats Job - Demo job that succeeds and provides meaningful statistics.

This job demonstrates:
- Successful completion with meaningful output
- System information gathering
- Structured data reporting
"""

import os
import sys
import shutil
import time
from datetime import datetime
from pathlib import Path


def get_disk_usage(path: str) -> dict:
    """Get disk usage statistics for a path."""
    try:
        usage = shutil.disk_usage(path)
        total_gb = usage.total / (1024**3)
        used_gb = usage.used / (1024**3)
        free_gb = usage.free / (1024**3)
        used_percent = (usage.used / usage.total) * 100
        
        return {
            "path": path,
            "total_gb": round(total_gb, 2),
            "used_gb": round(used_gb, 2),
            "free_gb": round(free_gb, 2),
            "used_percent": round(used_percent, 1)
        }
    except Exception as e:
        return {"path": path, "error": str(e)}


def count_files_in_directory(path: str) -> dict:
    """Count files and directories in a path."""
    try:
        path_obj = Path(path)
        if not path_obj.exists():
            return {"path": path, "error": "Path does not exist"}
        
        files = 0
        dirs = 0
        total_size = 0
        
        for item in path_obj.rglob("*"):
            if item.is_file():
                files += 1
                try:
                    total_size += item.stat().st_size
                except (OSError, PermissionError) as e:
                    print(f"⚠️  Warning: Cannot read file {item}: {e}")
                    continue  # Skip files we can't read
            elif item.is_dir():
                dirs += 1
        
        return {
            "path": path,
            "files": files,
            "directories": dirs,
            "total_size_mb": round(total_size / (1024**2), 2)
        }
    except Exception as e:
        return {"path": path, "error": str(e)}


def get_python_info() -> dict:
    """Get Python environment information."""
    return {
        "version": sys.version.split()[0],
        "executable": sys.executable,
        "platform": sys.platform,
        "path_entries": len(sys.path)
    }


def main():
    """Main job function that gathers and reports system statistics."""
    print("📊 System Stats Job Starting...")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Gather system statistics
    print("🔍 Gathering system information...")
    time.sleep(0.5)
    
    # Python environment
    python_info = get_python_info()
    print("🐍 Python Environment:")
    print(f"   Version: {python_info['version']}")
    print(f"   Executable: {python_info['executable']}")
    print(f"   Platform: {python_info['platform']}")
    print(f"   Path entries: {python_info['path_entries']}")
    print()
    
    # Disk usage for key directories
    print("💾 Disk Usage:")
    important_paths = [
        str(Path.home()),
        "/tmp",
        str(Path.cwd())
    ]
    
    for path in important_paths:
        usage = get_disk_usage(path)
        if "error" in usage:
            print(f"   {path}: Error - {usage['error']}")
        else:
            print(f"   {path}: {usage['used_gb']}GB used / {usage['total_gb']}GB total ({usage['used_percent']}%)")
    print()
    
    # File counts in current workspace
    print("📁 Workspace Analysis:")
    workspace_paths = [
        str(Path.cwd()),
        str(Path.home() / "Downloads"),
    ]
    
    for path in workspace_paths:
        if Path(path).exists():
            stats = count_files_in_directory(path)
            if "error" in stats:
                print(f"   {path}: Error - {stats['error']}")
            else:
                print(f"   {path}: {stats['files']} files, {stats['directories']} dirs, {stats['total_size_mb']}MB")
    print()
    
    # Process information
    print("⚡ Process Information:")
    print(f"   Process ID: {os.getpid()}")
    print(f"   Parent PID: {os.getppid()}")
    print(f"   User: {os.getenv('USER', 'unknown')}")
    print(f"   Working directory: {os.getcwd()}")
    print()
    
    # Summary
    total_checks = len(important_paths) + len(workspace_paths) + 4  # 4 for python/process info
    print("✅ System Stats Job Completed Successfully!")
    print(f"📈 Generated {total_checks} statistical reports")
    print("🕐 Total execution time: ~1.5 seconds")
    
    return 0


if __name__ == "__main__":
    exit(main())
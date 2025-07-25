#!/usr/bin/env python3
"""
Cleanup Folders Job - File system maintenance example.

This job demonstrates:
- File system operations
- Configuration via YAML
- Safe cleanup with dry-run mode
- Detailed logging
"""

import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

try:
    from calmlib.utils.logging_utils import setup_logging
    setup_logging()
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def load_config() -> Dict[str, Any]:
    """Load configuration from config.yaml."""
    config_path = Path(__file__).parent / "config.yaml"
    
    if not config_path.exists():
        logger.warning(f"Config file not found: {config_path}")
        return get_default_config()
    
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        logger.info(f"Loaded config from: {config_path}")
        return config
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """Get default configuration."""
    return {
        "cleanup_targets": [
            {
                "name": "Downloads folder",
                "path": "~/Downloads",
                "max_age_days": 30,
                "file_patterns": ["*.tmp", "*.temp", "*.download"],
                "enabled": True
            },
            {
                "name": "Temp files",
                "path": "/tmp",
                "max_age_days": 7,
                "file_patterns": ["temp_*", "*.cache"],
                "enabled": False  # Disabled by default for safety
            }
        ],
        "dry_run": True,
        "preserve_recent": True,
        "log_details": True
    }


def cleanup_directory(target: Dict[str, Any], dry_run: bool = True) -> Dict[str, int]:
    """Clean up a single directory based on configuration."""
    results = {"files_removed": 0, "bytes_freed": 0, "errors": 0}
    
    if not target.get("enabled", True):
        logger.info(f"Skipping disabled target: {target['name']}")
        return results
    
    target_path = Path(target["path"]).expanduser()
    if not target_path.exists():
        logger.warning(f"Target path does not exist: {target_path}")
        return results
    
    max_age_days = target.get("max_age_days", 30)
    cutoff_date = datetime.now() - timedelta(days=max_age_days)
    file_patterns = target.get("file_patterns", ["*"])
    
    logger.info(f"🧹 Cleaning up: {target['name']} ({target_path})")
    logger.info(f"📅 Removing files older than {max_age_days} days ({cutoff_date.date()})")
    
    files_to_remove = []
    
    # Find files matching patterns and age criteria
    for pattern in file_patterns:
        for file_path in target_path.glob(pattern):
            if file_path.is_file():
                try:
                    file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_mtime < cutoff_date:
                        files_to_remove.append(file_path)
                except OSError as e:
                    logger.error(f"Error checking file {file_path}: {e}")
                    results["errors"] += 1
    
    # Sort by modification time (oldest first)
    files_to_remove.sort(key=lambda p: p.stat().st_mtime)
    
    logger.info(f"📋 Found {len(files_to_remove)} files to remove")
    
    # Remove files
    for file_path in files_to_remove:
        try:
            file_size = file_path.stat().st_size
            
            if dry_run:
                logger.info(f"[DRY RUN] Would remove: {file_path} ({file_size} bytes)")
            else:
                file_path.unlink()
                logger.info(f"🗑️  Removed: {file_path} ({file_size} bytes)")
            
            results["files_removed"] += 1
            results["bytes_freed"] += file_size
            
        except OSError as e:
            logger.error(f"Error removing file {file_path}: {e}")
            results["errors"] += 1
    
    return results


def format_bytes(bytes_count: int) -> str:
    """Format bytes in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} TB"


def main():
    """Main job function."""
    logger.info("🧹 Cleanup Folders Job Starting...")
    
    # Load configuration
    config = load_config()
    dry_run = config.get("dry_run", True)
    
    if dry_run:
        logger.info("🔍 Running in DRY RUN mode - no files will be deleted")
    else:
        logger.warning("⚠️  Running in LIVE mode - files WILL BE DELETED")
    
    # Process each cleanup target
    total_results = {"files_removed": 0, "bytes_freed": 0, "errors": 0}
    
    for target in config.get("cleanup_targets", []):
        try:
            results = cleanup_directory(target, dry_run)
            
            # Aggregate results
            for key in total_results:
                total_results[key] += results[key]
                
        except Exception as e:
            logger.error(f"Error processing target {target.get('name', 'unknown')}: {e}")
            total_results["errors"] += 1
    
    # Print summary
    logger.info("📊 Cleanup Summary:")
    logger.info(f"   Files processed: {total_results['files_removed']}")
    logger.info(f"   Space freed: {format_bytes(total_results['bytes_freed'])}")
    logger.info(f"   Errors: {total_results['errors']}")
    
    if dry_run:
        logger.info("ℹ️  This was a dry run. Set dry_run: false in config.yaml to actually delete files.")
    
    if total_results["errors"] > 0:
        logger.warning("⚠️  Job completed with errors")
        return 1
    else:
        logger.info("✅ Cleanup Folders Job Completed Successfully!")
        return 0


if __name__ == "__main__":
    exit(main())
#!/usr/bin/env python3

import json
import re
from datetime import datetime
from pathlib import Path

# Keys to ignore (exact matches)
IGNORED_KEYS = {
    "last-analytics-stamp",
    "lastShowIndicatorTime",
    "file-mod-date",
    "parent-mod-date",
    "mod-count",
    "LSSharedFileList",  # Tracks recent/frequent items
    "RecentApplications",
    "RecentDocuments",
    "FXRecentFolders",
    "NSNavRecentPlaces",
    "CloudDocsMovedToiCloud",  # iCloud sync status
    "NSWindow Frame",  # Window positions
    "NSStatusItem Preferred Position",  # Menu bar item positions
    "ATXUpdatePredictionsLoggerCountsDictionary-ActionPredictions",
    "OwnedDeviceLastPublishDate",
    "PlaceInferenceMetricsClientQueryCount1",
    "ActivityBaseDates",
}

# Regex patterns for keys to ignore
IGNORED_PATTERNS = [
    r".*timestamp.*",
    r".*lastOpened.*",
    r".*LastUsed.*",
    r".*LastOpen.*",
    r".*Recent.*",
    r".*History.*",
    r".*Position.*",  # Window/UI element positions
    r".*Location.*",  # Window/UI element locations
    r".*Frame.*",  # Window frames
    r".*Date$",  # Matches fields ending in Date like OwnedDeviceLastPublishDate
    r".*Count.*",  # Matches counter fields like PlaceInferenceMetricsClientQueryCount
    r".*Last_.*",  # Matches fields with Last_ like _DKThrottledActivityLast_
    r".*BaseDates.*",  # Matches ActivityBaseDates
]


def should_keep_key(key):
    """Determine if a key should be kept in the cleaned output."""
    if key in IGNORED_KEYS:
        return False

    # Check against regex patterns
    for pattern in IGNORED_PATTERNS:
        if re.match(pattern, key, re.IGNORECASE):
            return False

    # Add this new check for timestamp-like values in the key name
    if any(time_word in key.lower() for time_word in ["time", "date", "last"]):
        return False

    return True


def clean_value(value):
    """Clean or filter out noisy values."""
    # Add check for timestamp-like strings
    if isinstance(value, str):
        # Try to parse as ISO format datetime
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return None  # Filter out timestamp values
        except ValueError:
            pass

    # Existing checks
    if value is None:
        return None

    if isinstance(value, (dict, list)) and not value:
        return None

    if isinstance(value, str) and not value.strip():
        return None

    # Add check for numeric counters that change frequently
    if isinstance(value, (int, float)) and value > 100:
        return None

    return value


def clean_diff_data(diff_data):
    """Recursively clean the diff data."""
    if isinstance(diff_data, dict):
        result = {}
        for key, value in diff_data.items():
            # Skip ignored keys
            if not should_keep_key(key):
                continue

            # Recursively clean nested structures
            if isinstance(value, (dict, list)):
                cleaned_value = clean_diff_data(value)
                if cleaned_value is not None:  # Only include non-empty results
                    result[key] = cleaned_value
            else:
                cleaned_value = clean_value(value)
                if cleaned_value is not None:
                    result[key] = cleaned_value

        return result if result else None

    elif isinstance(diff_data, list):
        result = []
        for item in diff_data:
            cleaned_item = clean_diff_data(item)
            if cleaned_item is not None:
                result.append(cleaned_item)
        return result if result else None

    else:
        return clean_value(diff_data)


def clean_diff(diff_file, output_file, verbose=False):
    """Clean and filter macOS settings diff output"""
    # Load the diff data
    if verbose:
        print(f"Loading diff from {diff_file}...")

    with open(diff_file) as f:
        diff_data = json.load(f)

    # Clean the diff data
    if verbose:
        print("Cleaning diff data...")

    cleaned_diff = clean_diff_data(diff_data)

    # Save cleaned diff
    output_path = Path(output_file)
    with open(output_path, "w") as f:
        json.dump(cleaned_diff, f, indent=2)

    if verbose:
        print(f"\nSaved cleaned diff to {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Clean and filter macOS settings diff output"
    )
    parser.add_argument(
        "--diff_file",
        default="output/settings_diff.json",
        help="JSON file containing the settings diff",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output/settings_diff_cleaned.json",
        help="Output JSON file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose processing information",
    )
    args = parser.parse_args()

    clean_diff(args.diff_file, args.output, args.verbose)

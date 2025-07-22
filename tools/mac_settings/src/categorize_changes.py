#!/usr/bin/env python3

import json
from pathlib import Path

import yaml


def load_config():
    """Load settings filter configuration"""
    config_path = Path(__file__).parent.parent / "config" / "settings_filter.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def categorize_changes(diff_data, config):
    """Categorize changes into interesting, boring, and unsorted"""
    result = {"interesting": {}, "boring": {}, "unsorted": {}}

    interesting_domains = set(config.get("interesting", {}).get("domains", []))
    interesting_keys = config.get("interesting", {}).get("keys", {})

    boring_domains = set(config.get("boring", {}).get("domains", []))
    boring_keys = config.get("boring", {}).get("keys", {})

    for domain, changes in diff_data.items():
        if not isinstance(changes, dict):
            continue

        # Check if entire domain is interesting or boring
        if domain in interesting_domains:
            result["interesting"][domain] = changes
            continue

        if domain in boring_domains:
            result["boring"][domain] = changes
            continue

        # Check individual keys
        for key, value in changes.items():
            # Check if key is interesting
            if domain in interesting_keys and key in interesting_keys[domain]:
                if domain not in result["interesting"]:
                    result["interesting"][domain] = {}
                result["interesting"][domain][key] = value
                continue

            # Check if key is boring
            if domain in boring_keys and key in boring_keys[domain]:
                if domain not in result["boring"]:
                    result["boring"][domain] = {}
                result["boring"][domain][key] = value
                continue

            # If neither interesting nor boring, it's unsorted
            if domain not in result["unsorted"]:
                result["unsorted"][domain] = {}
            result["unsorted"][domain][key] = value

    return result


def process_changes(input_file, output_file, verbose=False):
    """Process cleaned changes and categorize them"""
    # Load config
    config = load_config()

    # Load the cleaned diff data
    if verbose:
        print(f"Loading cleaned diff from {input_file}...")

    with open(input_file) as f:
        diff_data = json.load(f)

    # Categorize the changes
    if verbose:
        print("Categorizing changes...")

    categorized_diff = categorize_changes(diff_data, config)

    # Save categorized diff
    output_path = Path(output_file)
    with open(output_path, "w") as f:
        json.dump(categorized_diff, f, indent=2)

    if verbose:
        print(f"\nSaved categorized diff to {output_path}")

        # Print summary
        print("\nChange categories:")
        print(f"Interesting changes: {len(categorized_diff['interesting'])} domains")
        print(f"Boring changes: {len(categorized_diff['boring'])} domains")
        print(f"Unsorted changes: {len(categorized_diff['unsorted'])} domains")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Categorize macOS settings changes")
    parser.add_argument(
        "--input",
        default="output/settings_diff_cleaned.json",
        help="JSON file containing the cleaned settings diff",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output/settings_diff_categorized.json",
        help="Output JSON file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose processing information",
    )
    args = parser.parse_args()

    process_changes(args.input, args.output, args.verbose)

#!/usr/bin/env python3

import json
import subprocess
import tempfile
from pathlib import Path


def deep_diff(d1, d2):
    """Compare two dictionaries/lists and return their differences."""
    diff = {}

    # Handle lists specially
    if isinstance(d1, list) and isinstance(d2, list):
        list_diff = {"added": [], "removed": [], "changed": []}

        # First, find exact matches and remove them from consideration
        remaining1 = d1.copy()
        remaining2 = d2.copy()

        # Remove exact matches
        for item1 in d1[:]:
            if item1 in d2:
                remaining1.remove(item1)
                remaining2.remove(item1)

        # For dictionaries in lists, try to match by common keys
        if (
            remaining1
            and remaining2
            and all(isinstance(x, dict) for x in remaining1)
            and all(isinstance(x, dict) for x in remaining2)
        ):
            matched_pairs = []

            # Try to match items based on key intersection
            for i, item1 in enumerate(remaining1):
                best_match = None
                best_match_idx = None
                max_common_keys = 0

                for j, item2 in enumerate(remaining2):
                    if j not in [p[1] for p in matched_pairs]:
                        common_keys = set(item1.keys()) & set(item2.keys())
                        if len(common_keys) > max_common_keys:
                            max_common_keys = len(common_keys)
                            best_match = item2
                            best_match_idx = j

                if best_match and max_common_keys > 0:
                    matched_pairs.append((i, best_match_idx))
                    list_diff["changed"].append(deep_diff(item1, best_match))

            # Remove matched items from remaining lists
            for i1, i2 in reversed(matched_pairs):
                remaining1.pop(i1)
                remaining2.pop(i2)

        # Whatever is left is added or removed
        list_diff["added"] = remaining2
        list_diff["removed"] = remaining1

        return (
            list_diff
            if list_diff["added"] or list_diff["removed"] or list_diff["changed"]
            else {}
        )

    # Handle dictionaries
    elif isinstance(d1, dict) and isinstance(d2, dict):
        for k in d1:
            if k in d2:
                if isinstance(d1[k], (dict, list)) and isinstance(d2[k], (dict, list)):
                    nested_diff = deep_diff(d1[k], d2[k])
                    if nested_diff:
                        diff[k] = nested_diff
                elif d1[k] != d2[k]:
                    diff[k] = {"old": d1[k], "new": d2[k]}

        # Check for keys only in d2
        for k in d2:
            if k not in d1:
                diff[k] = {"old": None, "new": d2[k]}

        # Check for keys only in d1
        for k in d1:
            if k not in d2:
                diff[k] = {"old": d1[k], "new": None}

    # Handle primitive values
    else:
        if d1 != d2:
            return {"old": d1, "new": d2}

    return diff


def diff_settings(before_file, output_file, verbose=False):
    """Compare macOS format between two states"""
    # Load the before state
    with open(before_file) as f:
        before_state = json.load(f)

    # Get current state using dump_settings.py
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Run dump_settings.py to get current state
        script_dir = Path(__file__).parent
        dump_script = script_dir / "dump_settings.py"
        subprocess.run(["python3", str(dump_script), "-o", str(tmp_path)], check=True)

        # Load current state
        with open(tmp_path) as f:
            current_state = json.load(f)

        # Compare states
        if verbose:
            print("Comparing states...")

        differences = deep_diff(before_state, current_state)

        # Save differences to file
        output_path = Path(output_file)
        with open(output_path, "w") as f:
            json.dump(differences, f, indent=2)

        if verbose:
            print(f"\nSaved differences to {output_path}")

    finally:
        # Clean up temporary file
        Path(tmp_path).unlink()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Compare macOS format between two states"
    )
    parser.add_argument(
        "--before_file",
        default="output/reference.json",
        help="JSON file containing the before state",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output/settings_diff.json",
        help="Output JSON file for the diff",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose processing information",
    )
    args = parser.parse_args()

    diff_settings(args.before_file, args.output, args.verbose)

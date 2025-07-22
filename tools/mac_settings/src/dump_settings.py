#!/usr/bin/env python3

import subprocess
import json
import plistlib
import tempfile
import os
from pathlib import Path
from datetime import datetime


# Add custom JSON encoder
class DefaultsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return None  # Discard bytes objects
        return super().default(obj)


def get_domains():
    """Get list of domains from defaults command"""
    result = subprocess.run(["defaults", "domains"], capture_output=True, text=True)
    # Split on commas and clean up whitespace
    domains = [d.strip() for d in result.stdout.split(",")]
    return domains


def export_domain(domain):
    """Export a single domain to plist and convert to dict"""
    try:
        # Create temporary file for the plist
        with tempfile.NamedTemporaryFile(suffix=".plist", delete=False) as tmp:
            tmp_path = tmp.name

        # Export domain to binary plist
        subprocess.run(["defaults", "export", domain, tmp_path], check=True)

        # Read the plist file
        with open(tmp_path, "rb") as f:
            try:
                data = plistlib.load(f)
                return data
            except Exception as e:
                print(f"Error parsing plist for domain {domain}: {e}")
                return None
    except subprocess.CalledProcessError as e:
        print(f"Error exporting domain {domain}: {e}")
        return None
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def dump_settings(output_file, verbose=False):
    """Export macOS defaults to JSON file"""
    # Get all domains
    domains = get_domains()

    # Create result dictionary
    result = {}

    # Process each domain
    for domain in domains:
        if verbose:
            print(f"Processing {domain}...")
        data = export_domain(domain)
        if data is not None:
            result[domain] = data

    # Write to JSON file
    output_path = Path(output_file)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, cls=DefaultsEncoder)

    if verbose:
        print(f"\nExported defaults to {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Export macOS defaults to JSON")
    parser.add_argument(
        "-o",
        "--output",
        default="output/all_defaults.json",
        help="Output JSON file path",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose processing information",
    )
    args = parser.parse_args()

    dump_settings(args.output, args.verbose)

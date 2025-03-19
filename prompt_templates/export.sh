#!/bin/bash

# Set output file name
output_file="merged_prompts.md"

# Remove output file if it exists
rm -f "$output_file"

# Find all .md files recursively and append them to the output file
# Adding a newline between files for better readability
find . -type f -name "*.md" | while read -r file; do
    echo -e "\n## File: $file\n" >> "$output_file"
    cat "$file" >> "$output_file"
    echo -e "\n" >> "$output_file"
done

echo "All markdown files have been merged into $output_file" 
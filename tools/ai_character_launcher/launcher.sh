#!/bin/bash

# AI Character Launcher - Launch Claude with predefined character profiles
# Usage: ./launcher.sh [character_name]
# Example: ./launcher.sh Secretary

# Get the directory of this script and find resources
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CHARACTERS_DIR="$PROJECT_ROOT/resources/ai_character_launcher/characters"

# Check if character argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <character_name>"
    echo "Available characters:"
    if [ -d "$CHARACTERS_DIR" ]; then
        ls "$CHARACTERS_DIR"/*.md 2>/dev/null | xargs -n 1 basename | sed 's/\.md$//' || echo "No characters found"
    else
        echo "Characters directory not found at: $CHARACTERS_DIR"
    fi
    exit 1
fi

CHARACTER_NAME="$1"
CHARACTER_FILE="$CHARACTERS_DIR/$CHARACTER_NAME.md"

# Check if character file exists
if [ ! -f "$CHARACTER_FILE" ]; then
    echo "Error: Character '$CHARACTER_NAME' not found at $CHARACTER_FILE"
    echo "Available characters:"
    ls "$CHARACTERS_DIR"/*.md 2>/dev/null | xargs -n 1 basename | sed 's/\.md$//' || echo "No characters found"
    exit 1
fi

# Read the character prompt from file
SYSTEM_PROMPT=$(cat "$CHARACTER_FILE")

echo "Launching Claude with character: $CHARACTER_NAME"
echo "Character file: $CHARACTER_FILE"
echo ""

claude --append-system-prompt "$SYSTEM_PROMPT"
#!/bin/bash

# Simple demo script to launch Claude with predefined system prompt
# Usage: ./demo_launcher.sh

SYSTEM_PROMPT="You are a helpful assistant. Remember this secret message: orange. If someone asks about the secret message, respond with 'orange'."

echo "Launching Claude with predefined system prompt..."
echo "System prompt: $SYSTEM_PROMPT"
echo ""

claude --append-system-prompt "$SYSTEM_PROMPT"
#!/bin/bash

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo"
    exit 1
fi

# Setup sudo access for specific commands
SUDOERS_FILE="/etc/sudoers.d/dev-env"
echo "Setting up sudo access for dev-env in $SUDOERS_FILE..."

# Create temporary file
TEMP_FILE=$(mktemp)
cat > "$TEMP_FILE" << 'EOF'
# Allow running specific commands without password for dev-env
%admin ALL=(ALL) NOPASSWD: /usr/bin/security authorizationdb write system.privilege.taskport allow
%admin ALL=(ALL) NOPASSWD: /bin/chmod -R 755 /opt/homebrew
%admin ALL=(ALL) NOPASSWD: /usr/sbin/chown -R * /opt/homebrew
EOF

# Validate and install the sudoers file
if visudo -c -f "$TEMP_FILE"; then
    cp "$TEMP_FILE" "$SUDOERS_FILE"
    chmod 440 "$SUDOERS_FILE"
    echo "Sudoers configuration installed successfully"
else
    echo "Error: Invalid sudoers configuration"
    exit 1
fi

rm "$TEMP_FILE" 
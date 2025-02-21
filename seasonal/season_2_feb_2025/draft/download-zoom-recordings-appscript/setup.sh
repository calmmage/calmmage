#!/bin/bash

echo "Setting up Zoom Recording Downloader development environment..."

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install Node.js and npm first."
    echo "Visit https://nodejs.org/ to download and install."
    exit 1
fi

# Install clasp globally if not installed
if ! command -v clasp &> /dev/null; then
    echo "Installing clasp globally..."
    npm install -g @google/clasp
fi

# Create src directory if it doesn't exist
mkdir -p src

# Move .gs files to src if they exist in root
for file in *.gs; do
    if [ -f "$file" ]; then
        mv "$file" src/
        echo "Moved $file to src/"
    fi
done

# Check if .clasp.json exists
if [ ! -f ".clasp.json" ]; then
    echo "No .clasp.json found. You'll need to run 'clasp create' or 'clasp clone'"
    echo "Would you like to create a new Apps Script project? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]; then
        clasp create --title "Zoom Recording Downloader" --type standalone
    fi
fi

# Setup git hooks
if [ -d ".git" ]; then
    echo "Setting up git hooks..."
    
    # Create pre-commit hook
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "Running pre-commit checks..."

# Check if any .gs files are in root instead of src/
if ls *.gs 1> /dev/null 2>&1; then
    echo "Error: .gs files should be in src/ directory"
    exit 1
fi

# Add more checks here if needed
exit 0
EOF

    # Create post-commit hook that pushes to Apps Script
    cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
echo "Pushing changes to Google Apps Script..."
clasp push
EOF

    # Make hooks executable
    chmod +x .git/hooks/pre-commit
    chmod +x .git/hooks/post-commit
    
    echo "Git hooks installed successfully"
fi

echo "
Setup complete! Next steps:

1. Enable Google Apps Script API:
   - Visit https://script.google.com/home/usersettings
   - Turn on 'Google Apps Script API'

2. Login to clasp:
   clasp login

3. Start development:
   clasp push --watch

Note: To disable automatic push on commit, remove or modify .git/hooks/post-commit
" 
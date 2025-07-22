# New Mini Project Creation

## Command
```bash
new_mini [name] [--idea "project idea"]
```

## Steps
1. Name Processing
   - If no name provided:
     - Prompt user "What mini-project do you want to create?"
     - Use response to generate name
   - Validate name with AI (using query_gpt from calmlib)
     - If not good -> generate concise name with AI

2. Location Selection
   - Use seasonal folder management
   - Create in current season's folder
   - Auto-roll/rename folders if needed
     - 1) if folder time span doesn't match it name anymore -> auto-rename
     - 2) if count > threshold (7) or time threshold reached 
       - -> create new seasonal folder
       - -> update 'latest' symlink

3. Project Creation
   - Create mini-project directory
   - If idea provided:
     - Create idea.md with description
   - If not provided:
     - Prompt user "What's the project idea?"
   - Copy absolute path to clipboard
   - Print "Copied {path}"

## Flow Diagram
```mermaid
graph TD
    A[Start] --> B{Has name?}
    B -->|No| C[Ask "What mini-project?"]
    B -->|Yes| D[Validate name with AI]
    C --> D
    D -->|Not Good| E[Generate AI name]
    D -->|Good| F[Get seasonal folder]
    E --> F
    F --> G[Create directory]
    G --> H{Has idea?}
    H -->|No| I[Ask "What's the idea?"]
    H -->|Yes| J[Create idea.md]
    I --> J
    J --> K[Copy path]
    K --> L[End]
```

# Raw
1. Core Flow:
   - If no name provided:
     - Ask "What mini-project do you want to create?"
     - Validate/generate concise name with AI
   - Create in seasonal folder structure
   - Auto-manage seasonal folders (link to Seasonal Folder Management feature)

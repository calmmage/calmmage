# New Project Creation

## Command
```bash
new_project [name] [-t template] [--private]
```

## Steps
1. Name Processing
   - If no name provided:
     - Prompt user "What do you want to do?"
     - Use response to generate name
   - Validate name with AI (using query_gpt from calmlib)
     - If not good -> generate concise name with AI
   - Check GitHub for name conflicts

2. Template Selection
   - If template provided:
     - Use fuzzy-matching (see [Template Name Parsing](../features/template_name_parsing.md))
     - [TODO] Port logic from old dev_env (calmlib.match_subsequence)
   - If no template -> use default

3. Project Creation
   - Create GitHub repository from template
   - Clone to Experiments Destination
   - Copy absolute path to clipboard
   - Print "Copied {path}"

## Flow Diagram
```mermaid
graph TD
    A[Start] --> B{Has name?}
    B -->|No| C[Ask "What do you want to do?"]
    B -->|Yes| D[Validate name with AI]
    C --> D
    D -->|Not Good| E[Generate AI name]
    D -->|Good| F[Check GitHub conflicts]
    E --> F
    F --> G{Has template?}
    G -->|Yes| H[Fuzzy match template]
    G -->|No| I[Use default template]
    H --> J[Create GitHub repo from template]
    I --> J
    J --> K[Clone to Experiments destination]
    K --> L[Copy path to clipboard]
    L --> M[Print "Copied {path}"]
```
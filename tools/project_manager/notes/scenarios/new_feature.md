# New Feature Creation

## Command
```bash
new_feature [name] [-p project] [--idea "feature idea"]
```

## Steps
1. Name Processing
   - If no name provided:
     - Prompt user "What feature do you want to add?"
     - Use response to generate name
   - Validate name with AI (using query_gpt from calmlib)
     - If not good -> generate concise name with AI

2. Project Detection
   - If project not explicitly provided:
     - Try to auto-detect from current directory
     - If detection fails -> use default project
     - Ask for confirmation with timeout (auto-yes)
       ```
       Using project: {project_name} (auto-confirm in 5s)...
       ```

3. Feature Creation
   - Create feature directory: `{project}/dev/draft/{feature_name}`
   - Create new git branch: `feature/{feature_name}`
   - If idea not provided:
     - Prompt user "What's the feature idea?"
   - Create idea.md with provided description
   - Copy absolute path to clipboard
   - Print "Copied {path}"

## Flow Diagram
```mermaid
graph TD
    A[Start] --> B{Has name?}
    B -->|No| C[Ask "What feature?"]
    B -->|Yes| D[Validate name with AI]
    C --> D
    D -->|Not Good| E[Generate AI name]
    D -->|Good| F[Create feature dir]
    E --> F
    F --> G{Project specified?}
    G -->|No| H[Try auto-detect]
    H --> I{Detection successful?}
    I -->|No| J[Use default]
    I -->|Yes| K[Use detected]
    G -->|Yes| K
    J --> L[Confirm with timeout]
    K --> L
    L --> M[Create branch]
    M --> N{Has idea?}
    N -->|No| O[Ask "What's the idea?"]
    N -->|Yes| P[Create idea.md]
    O --> P
    P --> Q[Copy path]
    Q --> R[End]
```

# Raw
now, even more streamlined.
- new folder at dev/draft/feature_name
- ai "is this a good feature name" -> use/generate
- new branch
- idea (ask if not) -> /idea.md

- (steps from above for determining project)
- (steps from @new_project.md for copying abs path)

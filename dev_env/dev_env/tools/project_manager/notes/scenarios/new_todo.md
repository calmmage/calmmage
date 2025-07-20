# New Todo Creation

## Command
```bash
new_todo [text] [--open] [-p project]
```

## Steps
1. Todo Text Processing
   - If no text provided:
     - Prompt user "What do you want to do?"
     - Use response as todo text

2. Project Detection
   - If project not explicitly provided:
     - Try to auto-detect from current directory
     - If detection fails -> use default project
     - Ask for confirmation with timeout (auto-yes)
       ```
       Using project: {project_name} (auto-confirm in 5s)...
       ```

3. Todo Creation
   - Generate target path: `{project}/dev/todo_{date}.md`
   - If --open flag:
     - Open todo.md in Sublime Text
   - Else:
     - Append todo in format: `- [ ] {todo_text}`
     - Print "Added todo to {path}"

## Flow Diagram
```mermaid
graph TD
    A[Start] --> B{Has text?}
    B -->|No| C[Ask "What do you want to do?"]
    B -->|Yes| D[Use provided text]
    C --> D
    D --> E{Project specified?}
    E -->|No| F[Try auto-detect]
    F --> G{Detection successful?}
    G -->|No| H[Use default]
    G -->|Yes| I[Use detected]
    E -->|Yes| I
    H --> J[Confirm with timeout]
    I --> J
    J --> K{Open flag?}
    K -->|Yes| L[Open in Sublime]
    K -->|No| M[Append todo]
    L --> N[End]
    M --> N
```

# Raw
ok, let's try a little more streamlined

- new todo:
1) if not provided ask me "what do you want to do"
2) if not provided 
-> auto-determine project
if able to -> name
if not -> default
ask for confirmation (with timeout, auto-yes)

write to 
project/dev/todo_{date}.md
in a format 
- [ ] todo

Bonus:
special keyword "open" or flag --open
-> then opens a todo.md in sublime instead of writing to it.
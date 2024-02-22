# Project Folder Deeplink
npm install && npm run dev

Open a project folder with a specified tool

```bash
open -a "Visual Studio Code" /Users/michael/Projects/Python/Python-Scripts
```

# Actions:

1) Open a project folder with a specified tool
2) Create a deep link
   - Example:
     - `raycast://open-project?path=/Users/michael/Projects/Python/Python-Scripts&tool=vscode`
3) Handle a deep link 
   - Args: 
     - Path
     - Tool (Optional)
   If no tool provided - show a list of tools to choose from
4) Things to configure for the extension:
   - Tools list (name + alias)
   - Default tool


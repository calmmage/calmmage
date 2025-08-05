# Python Execution Requirements

**Always use uv for Python command execution**

**For running Python scripts:**
```bash
uv run python script.py
```

**For running Typer CLI tools:**
```bash
uv run typer path/to/cli.py run [command] [args]
```

**Examples:**
- `uv run python script.py`
- `uv run typer path/to/cli.py run [command]`

**Never use bare python or direct script execution - always prefix with `uv run`**

**Use absolute imports instead of sys.path.append()**
- Prefer direct imports when possible: `from module_name.file import Class`
- Avoid adding paths manually with `sys.path.append()`
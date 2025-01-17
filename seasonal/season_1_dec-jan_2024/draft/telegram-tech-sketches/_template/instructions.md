# Mini-Project Templates Instructions

## Template Location
Mini-project templates should be placed in one of these locations:

1. **Default Location** (Recommended):
   Place templates in the project manager's templates directory:
   ```
   dev-env/
   └── dev_env/
       └── tools/
           └── project_manager/
               ├── templates/           # Templates directory
               │   ├── mini-botspot-template/
               │   └── other-templates/
               ├── project_manager.py
               └── pm_cli.py
   ```

2. **Custom Location** (Optional):
   You can configure a custom templates directory in `pm_config.yaml`:
   ```yaml
   templates_dir: "/path/to/your/templates"
   ```

## Creating New Templates

1. Create a new directory with your template name (use hyphens for spaces)
2. Add all necessary template files
3. Make sure to include:
   - `idea.md` (optional) - Template's purpose and usage
   - Any other files needed for the project type

## Using Templates

Templates can be used in two ways:

1. **Automatic Detection**:
   ```bash
   pm new-mini-project my-test-bot
   # Will automatically use mini-botspot-template if name contains 'bot'
   ```

2. **Explicit Template**:
   ```bash
   pm new-mini-project my-project -t mini-botspot-template
   ```

## Available Templates

Currently available templates:
- `mini-botspot-template` - Basic template for Telegram bots

## Adding New Templates

1. Create your template directory following the structure above
2. Add the template name to `complete_mini_project_template()` in `pm_cli.py`:
   ```python
   def complete_mini_project_template(incomplete: str):
       templates = [
           "mini-botspot-template",
           "your-new-template"  # Add here
       ]
       return [t for t in templates if t.startswith(incomplete)]
   ```

## Template Structure Best Practices

1. Use clear, descriptive names with hyphens
2. Include a `sample.env` for required environment variables
3. Document template usage in `idea.md` or `README.md`
4. Keep templates minimal but functional 
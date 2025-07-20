# Dev-Env Project Guidelines

## Build/Test/Lint Commands

```bash
# Install dependencies
poetry install

# Run all tests
poetry run pytest

# Run a single test
poetry run pytest tests/path/to/test_file.py::test_function_name

# Code formatting and linting
poetry run black dev_env/
poetry run isort dev_env/
poetry run flake8 dev_env/
poetry run vulture dev_env/ --min-confidence 80
```

## Code Style Guidelines

- **Line length**: 100 characters max
- **Formatting**: Use Black with line length 100
- **Imports**: Use isort with Black profile, group imports by standard, third-party,
  first-party
- **Types**: Python 3.11+, static type hints recommended
- **Naming**: Snake_case for variables/functions, PascalCase for classes
- **Documentation**: Docstrings for public functions and classes
- **Error handling**: Use specific exceptions, proper context
- **Linting**: Use flake8, isort, black, vulture
- **Pre-commit hooks**: Required before committing

## Project Structure

- Use `/dev_env` for main code
- Tests in `/tests` mirroring module structure
- Development notebooks in `/dev` directory
- [x] check if repo name in pyproject.toml is still 'project_name'
  - [x] see if there's still a folder 'project_name' in the root
  -  if yes - ask user the project name and change it in pyproject.toml and in the folder name
- [x] use project name to fill all .pre-commit-config.yaml values where it is required.
- [x] remove duplicate --exclude flags in vulture pre-commit
- [ ] move tools folder to dev_env - and update aliases

- [x] line 1-7 (nbstripout removal): Add a new function `_add_nbstripout(repo_path: Path)` with the original nbstripout config and call it in `_add_precommit()`

- [x] line 8-14 (black config): Fix `_add_black()` function to use the original black config instead of black-jupyter

- [x] line 23 (vulture exclude): Remove unnecessary exclude in `_add_vulture()` function:
  ```python
  args: [
      "--min-confidence", "80",
      "{source_dir_name}"  # project_name
  ]
  ```

- [ ] line 43 (flake8 path): Add back file path restriction in `_add_flake8()`:
  ```python
  files: ^{source_dir_name}/.*\.py$
  ```

- [x] line 64 (isort path): Add back file path restriction in `_add_isort()`:
  ```python
  files: ^.*\.py$
  ```

- [x] line 44 (exclude pattern): Add back .venv to exclusions in `_add_flake8()`:
  ```python
  "--exclude=.venv,.git,__pycache__,build,dist",
  ```

- [x] Add poetry install functionality for test tools:
  - [x] Add _install_all_test_dependencies function to install all packages in a single command
  - [x] Remove individual package installations from tool functions
  - [x] Update _add_precommit to use the new function

Cool Features to Add:
- [ ] Add pre-commit autoupdate functionality:
  ```python
  def _update_precommit_hooks(repo_path: Path):
      """Update all pre-commit hook versions to latest."""
      subprocess.run(["pre-commit", "autoupdate"], cwd=repo_path, check=True)
  ```

- [ ] Add parallel test execution for faster CI:
  ```python
  def _add_codecov(repo_path: Path):
      content = dedent(
          f"""
              args: [
              "--cov={source_dir_name}",
              "--cov-report=xml",
              "--cov-fail-under={settings.codecov_fail_under}",
              "-n auto",  # Add parallel execution
              ]
          """
      )
  ```

CI Improvements:
- [ ] Add pre-commit checks to CI workflow
- [ ] Add codecov reporting to CI workflow
- [ ] Add dependency security scanning to CI workflow

Config Improvements:
- [ ] Add configurable tool versions to config.yaml
- [ ] Add configurable exclusion patterns to config.yaml

Repository Features:
- [ ] Auto-generate README.md template with badges
- [ ] Add automatic version bumping with commitizen
- [ ] Add automatic changelog generation
- [ ] Add dependabot configuration
- [ ] Add GitHub issue templates
- [ ] Add automatic PR labeling
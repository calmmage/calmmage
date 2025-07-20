import re
import subprocess
from enum import Enum
from functools import lru_cache
from pathlib import Path
from textwrap import dedent, indent
from typing import List

import pyperclip
import toml
import typer
import yaml
from calmlib.utils import fix_path
from loguru import logger
from pydantic_settings import BaseSettings

app = typer.Typer()


class Operation(str, Enum):
    ADD_VULTURE = "add-vulture"
    ADD_BLACK = "add-black"
    UPDATE_YAML_TESTS = "update-yaml-tests"
    UPGRADE_DOCKERFILE = "upgrade-dockerfile"
    UPGRADE_PYPROJECT = "upgrade-pyproject"
    ADD_PRECOMMIT = "add-precommit"
    UPGRADE_LIBS = "upgrade-libs"
    RUN_ALL = "run-all"


class Settings(BaseSettings):
    root_paths: List[Path]
    codecov_fail_under: int = 80

    @classmethod
    def from_yaml(cls, path: Path):
        with open(path) as file:
            config_data = yaml.safe_load(file)

        # Expand user directory for each path in root_paths
        config_data["root_paths"] = [
            Path(p).expanduser() for p in config_data["root_paths"]
        ]

        return cls(**config_data)


# Initialize settings with the loaded configuration
config_path = Path(__file__).parent / "config.yaml"
settings = Settings.from_yaml(config_path)


def _add_precommit_tool_if_missing(repo_path: Path, tool_name: str, content: str):
    """Add a pre-commit tool configuration if it's not already present.

    Args:
        repo_path: Path to the repository
        tool_name: Name of the tool to add
        content: Tool configuration content
    """
    logger.debug(f"Adding pre-commit tool if missing: {tool_name}")
    pre_commit_config_path = repo_path / ".pre-commit-config.yaml"

    content = indent(content, "  ")

    if not pre_commit_config_path.exists():
        logger.warning(
            f"No .pre-commit-config.yaml found at {pre_commit_config_path}. Creating new file."
        )
        # Create new file with repos: header
        pre_commit_config_path.write_text("repos:\n" + content)
        return

    # Read existing content
    existing_content = pre_commit_config_path.read_text().strip()

    # If file is empty or doesn't have repos: header
    if not existing_content.strip() or "repos:" not in existing_content:
        existing_content = "repos:\n" + content
    else:
        # Check if tool is already in it
        if tool_name in existing_content:
            tool_line = [
                line for line in existing_content.splitlines() if tool_name in line
            ][-1]
            if tool_line.strip().startswith("#"):
                logger.info(
                    f"Found {tool_name} in .pre-commit-config.yaml, but it's commented out. Will add {tool_name} anew."
                )
            else:
                logger.warning(
                    f"Seems like {tool_name} is already in .pre-commit-config.yaml. Skipping."
                )
                return
        existing_content = existing_content.rstrip() + "\n" + content

    pre_commit_config_path.write_text(existing_content)


def _add_pyproject_section_if_missing(repo_path: Path, section: str, content: str):
    pyproject_toml_path = repo_path / "pyproject.toml"
    if not pyproject_toml_path.exists():
        logger.warning(f"No pyproject.toml found at {pyproject_toml_path}. Skipping.")
        raise ValueError("No pyproject.toml found")
    pyproject_toml_content = pyproject_toml_path.read_text()

    if section in pyproject_toml_content:
        logger.info(f"Section {section} already exists in pyproject.toml. Skipping.")
        return

    pyproject_toml_content = pyproject_toml_content.rstrip() + "\n" + content
    pyproject_toml_path.write_text(pyproject_toml_content)


def check_and_fix_poetry_project_name(path: Path, candidate: str) -> None:
    """Check and fix project name in pyproject.toml if needed.

    Args:
        path: Path to the repository root
        candidate: Candidate project name to use
    """
    # step 1: find pyproject toml path, check if exists
    pyproject_path = path / "pyproject.toml"
    if not pyproject_path.exists():
        logger.warning(f"No pyproject.toml found at {pyproject_path}. Skipping.")
        return

    # step 2: load pyproject toml
    pyproject_content = pyproject_path.read_text()
    pyproject_data = toml.loads(pyproject_content)

    if "tool" not in pyproject_data or "poetry" not in pyproject_data["tool"]:
        logger.warning("No [tool.poetry] section found in pyproject.toml. Skipping.")
        return

    # step 3: check what is the name
    current_name = pyproject_data["tool"]["poetry"].get("name")

    # - if name is 'project_name'
    # replace with candidate
    if current_name == "project-name":
        logger.info(f"Replacing placeholder project name with {candidate}")
        content = pyproject_path.read_text()
        content = re.sub(r'name\s*=\s*"project-name"', f'name = "{candidate}"', content)
        pyproject_path.write_text(content)
    # if name is present:
    #  compare with candidate
    #  raise warning if different, return
    elif current_name and current_name != candidate:
        logger.warning(
            f"Project name mismatch: {current_name} in pyproject.toml vs {candidate} provided. "
            "Not changing existing name."
        )
        return current_name


def add_source_package_to_pyproject_toml(path: Path, package_name: str):
    """Add a package to the pyproject.toml file.

    Args:
        path: Path to the repository root
        candidate: Candidate project name to use
    """

    # step 1: find pyproject toml path, check if exists
    pyproject_path = path / "pyproject.toml"
    if not pyproject_path.exists():
        logger.warning(f"No pyproject.toml found at {pyproject_path}. Skipping.")
        return

    # step 2: load pyproject toml
    pyproject_content = pyproject_path.read_text()
    pyproject_data = toml.loads(pyproject_content)

    if "tool" not in pyproject_data or "poetry" not in pyproject_data["tool"]:
        logger.warning("No [tool.poetry] section found in pyproject.toml. Skipping.")
        return

    current_packages = pyproject_data["tool"]["poetry"].get("packages", [])
    # packages=[
    #   { include = "src", from = "." },
    #   { include = "swe_bench", from = "." }
    # ]
    if not current_packages:
        # add a new section with regexp
        new_text = dedent(
            f"""
            packages=[
                {{ include = "{package_name}", from = "." }},
            ]
            """
        )
        # find the [tool.poetry] section
        pos = pyproject_content.find("[tool.poetry]") + len("[tool.poetry]")
        # find the next section header
        next_header = re.search(r"\n\[(.*)\]", pyproject_content[pos:])
        if next_header:
            next_header = next_header.group(1)
        else:
            next_header = ""
        pos = pyproject_content.find(next_header) - 1
        pyproject_content = (
            pyproject_content[:pos].strip()
            + new_text
            + "\n\n"
            + pyproject_content[pos:]
        )

        pyproject_path.write_text(pyproject_content.rstrip())
    # if not any(p.get("include") == package_name for p in current_packages):
    elif not any(p.get("include") == package_name for p in current_packages):
        raise NotImplementedError(
            "Adding packages to existing list is not implemented yet"
        )
        # current_packages.append({"include": package_name, "from": "."})
        # pyproject_data["tool"]["poetry"]["packages"] = current_packages
        # pyproject_path.write_text(toml.dumps(pyproject_data))
        # 1) a - if ppackages= is present -
        # 2) b - asd


@lru_cache()
def _get_source_dir_name(repo_path: Path) -> str:
    """

    :param repo_path:
    :return:
    """
    # step 1: fix path to work with abs_path
    repo_path = fix_path(repo_path)
    candidates = []

    source_dir_name = None
    candidates.append(repo_path.name)

    # step 2: check and fix project name in pyproject.toml
    res = check_and_fix_poetry_project_name(repo_path, candidate=repo_path.name)
    if res is not None:
        # logger.warning(
        #     f"Name conflict in pyproject.toml: folder name - {repo_path.name}, project name - {res}. "
        #     # f"Using {res}"
        # )
        # source_dir_name = res
        candidates.append(res)

    candidates.append("src")

    for candidate in candidates:
        if (repo_path / candidate).exists():
            logger.info(
                f"Found source directory: {candidate}. Using it for pre-commit setup."
            )
            source_dir_name = candidate
            break
        if (repo_path / candidate.replace("-", "_")).exists():
            logger.info(
                f"Found source directory: {candidate}. Using it for pre-commit setup."
            )
            source_dir_name = candidate.replace("-", "_")
            break

    # if none of the candadtes exist, ask user for a name
    if source_dir_name is None:
        # ask user for project name
        # default = repo_path.name.replace("-", "_")
        default = "src"
        try:
            source_dir_name = typer.prompt(
                f"Please provide a source directory name for {repo_path}, will be used to run pre-commit checks (default: {default}): ",
                default=default,
            )
        except:
            source_dir_name = default

    if not source_dir_name:
        # something went wrong
        raise ValueError("No source directory name identified")
    # option 1: user provided full path
    if Path(source_dir_name).exists():
        source_dir_name = Path(source_dir_name).name
    # option 2: user provided name
    # if not (repo_path / source_dir_name).exists():
    #     return None

    x = repo_path / source_dir_name
    if not x.exists():
        y = repo_path / "project_name"
        if y.exists():
            y.rename(repo_path / source_dir_name)
            logger.debug(f"Renamed project_name to {source_dir_name}")
        else:
            x.mkdir()
            logger.debug(f"Created source directory: {source_dir_name}")

    # add it as package to pyproject.toml
    try:
        add_source_package_to_pyproject_toml(repo_path, source_dir_name)
    except NotImplementedError:
        logger.warning(
            "Adding packages to existing list is not implemented yet - skipping"
        )

    return source_dir_name


def _add_vulture(repo_path: Path):
    """Add vulture configuration to the repository

    - find .pre-commit-config.yaml
    - check if vulture is already in it
    - if not, add it.
    """
    source_dir_name = _get_source_dir_name(repo_path)

    content = dedent(
        rf"""
        - repo: https://github.com/jendrikseipp/vulture
          rev: 'v2.10'
          hooks:
            - id: vulture
              args: [
                "--min-confidence", "80",
                "{source_dir_name}"  # project_name - path to scan
              ]
              files: ^.*\.py$
              exclude: ^(.git|.venv|venv|build|dist)/.*$
        """
    )
    _add_precommit_tool_if_missing(repo_path, "vulture", content)


def _add_black(repo_path: Path):
    """Add black configuration to the repository."""
    content = dedent(
        """
          - repo: https://github.com/psf/black
            rev: 24.2.0
            hooks:
              - id: black
                args: [ --line-length=100 ]
                name: black
                description: "Black: The uncompromising Python code formatter (with Jupyter Notebook support)"
                entry: black
                language: python
                minimum_pre_commit_version: 2.9.2
                require_serial: true
                types_or: [python, pyi, jupyter]
                additional_dependencies: [".[jupyter]"]
        """
    )
    _add_precommit_tool_if_missing(repo_path, "black", content)


def _add_flake8(repo_path: Path):
    """Add flake8 configuration to the repository."""
    source_dir_name = _get_source_dir_name(repo_path)
    content = dedent(
        rf"""
        - repo: https://github.com/pycqa/flake8
          rev: '7.0.0'
          hooks:
            - id: flake8
              additional_dependencies: [
                'flake8-docstrings',
                'flake8-bugbear',
                'flake8-comprehensions',
                'flake8-simplify',
              ]
              args: [
                "--max-line-length=100",
                "--exclude=.venv,.git,__pycache__,build,dist",
                "--ignore=E203,W503",  # Ignore some style errors that conflict with other tools
              ]
              files: ^{source_dir_name}/.*\.py$ # project_name - path to scan
        """
    )
    _add_precommit_tool_if_missing(repo_path, "flake8", content)


def _add_isort(repo_path: Path):
    """Add isort configuration to the repository."""
    content = dedent(
        r"""
        - repo: https://github.com/PyCQA/isort
          rev: 5.13.2
          hooks:
            - id: isort
              name: isort (python)
              files: ^.*\.py$
        """
    )
    _add_precommit_tool_if_missing(repo_path, "isort", content)

    content = dedent(
        """
        [tool.isort]
        profile = "black"
        multi_line_output = 3
        line_length = 100
        include_trailing_comma = true
        force_grid_wrap = 0
        use_parentheses = true
        ensure_newline_before_comments = true
        skip = [".git", "venv", ".env", "__pycache__"]
        # known_first_party = ["your_package_name"]  # Replace with your package name
        # known_third_party = [
        #     "aiogram",
        #     "fastapi",
        #     "pydantic",
        #     "pytest",
        #     "tqdm",
        #     "loguru"
        # ]
        # sections = [
        #     "FUTURE",
        #     "STDLIB",
        #     "THIRDPARTY",
        #     "FIRSTPARTY",
        #     "LOCALFOLDER"
        # ]
        """
    )
    _add_pyproject_section_if_missing(repo_path, "[tool.isort]", content)


def _add_pyupgrade(repo_path: Path):
    content = dedent(
        """
          - repo: https://github.com/asottile/pyupgrade
            rev: v3.19.0
            hooks:
              - id: pyupgrade
        """
    )
    _add_precommit_tool_if_missing(repo_path, "pyupgrade", content)


def _add_ruff(repo_path: Path):
    content = dedent(
        """
        - repo: https://github.com/astral-sh/ruff-pre-commit
          # Ruff version.
          rev: v0.7.4
          hooks:
            # Run the linter.
            - id: ruff
              types_or: [ python, pyi ]
              args: [ --fix ]
            # Run the formatter.
            - id: ruff-format
              types_or: [ python, pyi ]
        """
    )
    _add_precommit_tool_if_missing(repo_path, "ruff", content)


def _add_codecov(repo_path: Path):
    source_dir_name = _get_source_dir_name(repo_path)

    # step 1: add to pre-commit
    content = dedent(
        f"""
          - repo: local
            hooks:
              - id: pytest-check
                name: pytest-check
                entry: pytest
                language: system
                pass_filenames: false
                always_run: true
                args: [
                  "--cov={source_dir_name}",  # project_name - path to scan
                  "--cov-report=xml",
                  "--cov-fail-under={settings.codecov_fail_under}",
                ]
        """
    )
    # - repo: https://github.com/codecov/codecov-action
    #   hooks:
    #     - id: codecov
    _add_precommit_tool_if_missing(repo_path, "pytest-check", content)


def _update_pyproject_toml(repo_path: Path):
    """
    - Step 1: check if this is old or new style pyproject.toml
    - Step 2: if old, copy new template to clipboard and open the file with sublime
    """
    pyproject_toml_path = repo_path / "pyproject.toml"
    if not pyproject_toml_path.exists():
        # logger.warning(f"No pyproject.toml found at {pyproject_toml_path}. Skipping.")
        raise ValueError(f"No pyproject.toml found at {pyproject_toml_path}")

    pyproject_toml_content = pyproject_toml_path.read_text()

    template_path = Path(__file__).parent / "poetry_template.txt"
    template = template_path.read_text()

    # check if it's old or new style
    # old style: doesn't have   [tool.poetry.group.test.dependencies]
    keyword = "[tool.poetry.group.test.dependencies]"
    if keyword not in pyproject_toml_content:
        pyperclip.copy(template)
        logger.info(
            f"Copied new template to clipboard. Opening {pyproject_toml_path} with Sublime."
        )
        subprocess.run(["subl", pyproject_toml_path])
    else:
        logger.info(
            "Looks like pyproject.toml is up to the standard of the latest template. (main, dev, extras, test) Skipping."
        )


def _update_dockerfile(repo_path: Path):
    """
    check if old or new style dockerfile
    if old, copy new template to clipboard and open the file with sublime
    """
    # skip for now
    pass


def _update_yaml_tests(repo_path: Path):
    """Update or create the GitHub Actions workflow file for tests."""
    workflow_dir = repo_path / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    workflow_file = workflow_dir / "main.yml"

    template_path = Path(__file__).parent / "tests_workflow_template.txt"

    template_content = template_path.read_text()
    workflow_file.write_text(template_content)
    logger.info(f"Updated GitHub Actions workflow file at {workflow_file}.")


def _install_precommit(repo_path: Path):
    """Install pre-commit hooks in the repository."""
    pre_commit_config_path = repo_path / ".pre-commit-config.yaml"
    if not pre_commit_config_path.exists():
        logger.error(
            f"No .pre-commit-config.yaml found at {pre_commit_config_path}. Cannot install pre-commit."
        )
        return

    try:
        subprocess.run(
            ["poetry", "run", "pre-commit", "install"], cwd=repo_path, check=True
        )
        logger.info("Pre-commit hooks installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install pre-commit hooks: {e}")


def _discover_project(project: str) -> Path:
    if Path(project).exists():
        return Path(project)
    else:
        # check for projects with this name in configured root paths
        for root_path in settings.root_paths:
            project_path = root_path / project
            if project_path.exists():
                return project_path


def _add_nbstripout(repo_path: Path):
    """Add nbstripout configuration to strip output from Jupyter notebooks."""
    content = dedent(
        r"""
        - repo: https://github.com/kynan/nbstripout
          rev: 0.5.0
          hooks:
            - id: nbstripout
              files: \.ipynb$
              stages: [pre-commit]
        """
    )
    _add_precommit_tool_if_missing(repo_path, "nbstripout", content)


def _install_all_test_dependencies(repo_path: Path):
    """Install all test dependencies in a single command."""
    # first - just make sure poetry is installed at all..
    try:
        subprocess.run(["poetry", "install"], check=True, cwd=repo_path)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install poetry: {e}")
        raise

    packages = [
        # "black[jupyter]",
        # flake8 and extensions removed as requested
        # "isort",
        "vulture",
        "pytest-cov",
        "pytest-asyncio",
        "pytest-mock",
        "pyupgrade",
        "pyright",
        "ruff",
    ]
    try:
        cmd = ["poetry", "add", "--group", "test"] + packages
        subprocess.run(cmd, cwd=repo_path, check=True)
        logger.info("Successfully installed all test dependencies")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install test dependencies: {e}")


def _add_pyright(repo_path: Path):
    """Add pyright configuration to the repository."""
    content = dedent(
        """
        - repo: https://github.com/RobertCraigie/pyright-python
          rev: v1.1.399
          hooks:
            - id: pyright
              additional_dependencies: ["pyright==1.1.399"]
              args:
                - "--venvpath=."     # directory that *contains* the venv
        """
    )
    _add_precommit_tool_if_missing(repo_path, "pyright", content)


def _add_precommit(repo_path: Path):
    # First install all test dependencies
    _install_all_test_dependencies(repo_path)

    # Then add configurations
    _add_nbstripout(repo_path)
    _add_vulture(repo_path)
    _add_codecov(repo_path)
    _add_pyupgrade(repo_path)
    _add_pyright(repo_path)
    _add_ruff(repo_path)
    _install_precommit(repo_path)


@app.command()
def fix_repo(
    project: str = typer.Argument(..., help="Project"),
    operation: Operation = typer.Option(Operation.RUN_ALL, help="Operation to perform"),
):
    """Fix repository according to modern standards"""
    repo_path = _discover_project(project)
    if repo_path is None:
        logger.error(
            f"Project {project} not found in any of the root paths: {settings.root_paths}"
        )
        raise typer.Exit(1)

    logger.info(f"Fixing repo at {repo_path} with operation {operation}")

    if not repo_path.is_dir():
        logger.error(f"Path {repo_path} is not a directory")
        raise typer.Exit(1)

    try:
        if operation == Operation.ADD_VULTURE:
            _add_vulture(repo_path)

        elif operation == Operation.ADD_BLACK:
            _add_black(repo_path)

        elif operation == Operation.UPDATE_YAML_TESTS:
            _update_yaml_tests(repo_path)

        elif operation == Operation.ADD_PRECOMMIT:
            # Add all standard tools
            _add_precommit(repo_path)

        elif operation == Operation.UPGRADE_PYPROJECT:
            _update_pyproject_toml(repo_path)

        elif operation == Operation.UPGRADE_DOCKERFILE:
            _update_dockerfile(repo_path)

        elif operation == Operation.RUN_ALL:
            logger.info("Running all operations...")
            _update_pyproject_toml(repo_path)
            _add_precommit(repo_path)
            _update_dockerfile(repo_path)
            _update_yaml_tests(repo_path)

        logger.success(f"Successfully completed operation {operation}")

    except Exception as e:
        logger.error(f"Error during {operation}: {e}")
        import traceback

        traceback.print_exc()
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

import os
from pathlib import Path
from typing import Optional

import typer
from loguru import logger

app = typer.Typer()


def create_softlink(target: Path, link_name: Optional[str] = None):
    # Resolve target to absolute path
    target_path = target.resolve()

    if not target_path.exists():
        logger.error(f"Target path does not exist: {target_path}")
        raise typer.Exit(code=1)

    # If link_name is not provided, use the target's name
    if link_name is None:
        link_name = target_path.name

    # Create the link in the current directory
    link_path = Path.cwd() / link_name

    # Check if the link already exists
    if link_path.exists():
        logger.warning(f"Link already exists: {link_path}")
        if not typer.confirm("Do you want to overwrite it?"):
            logger.info("Operation cancelled.")
            raise typer.Exit()
        link_path.unlink()

    # Create the softlink
    try:
        os.symlink(target_path, link_path)
        logger.success(f"Softlink created: {link_path} -> {target_path}")
    except OSError as e:
        logger.error(f"Failed to create softlink: {e}")
        raise typer.Exit(code=1)


@app.command()
def main(
    target: Path = typer.Argument(..., help="Path to the target file or directory"),
    link_name: Optional[str] = typer.Option(
        None, help="Name of the softlink (default: same as target)"
    ),
):
    """
    Create a softlink to a specified path.
    The softlink is created in the current directory.
    """
    create_softlink(target, link_name)


if __name__ == "__main__":
    app()

import argparse
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from tools.project_arranger.src.main import ProjectArranger

ENABLED = False


def main(
    config_path: str = "config.yaml",
    dry_run: bool = True,
    verbose: bool = False,
    show_all: bool = False,
):
    logger.info(f"Running project arranger with config from {config_path}")

    if dry_run:
        logger.info("Running in dry-run mode")

    try:
        arranger = ProjectArranger(Path(config_path))
        projects = arranger.build_projects_list()
        new_groups = arranger.sort_projects(projects)

        if show_all:
            arranger.print_all_results(new_groups, print_sizes=verbose)
        else:
            # Get current groups based on filesystem structure
            current_groups = arranger.get_current_groups(projects)
            arranger.print_changes(current_groups, new_groups, print_sizes=verbose)

        if not dry_run:
            if not ENABLED:
                raise NotImplementedError("Apply mode forbidden for now!")

    except Exception as e:
        logger.error(f"Error during project arrangement: {e}")
        raise


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description="Project arrangement tool")
    default_config_path = Path(__file__).parent / "pa_config.yaml"
    parser.add_argument(
        "--config", default=default_config_path, help="Path to config file"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode without making changes",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print additional information like project sizes",
    )
    #  todo: Move into a separate tool / typer command
    parser.add_argument(
        "--show-all",
        action="store_true",
        help="Show full project list instead of just changes",
    )

    args = parser.parse_args()
    main(
        config_path=args.config,
        dry_run=args.dry_run,
        verbose=args.verbose,
        show_all=args.show_all,
    )

# TODO: Consider moving this into a separate tool or typer command

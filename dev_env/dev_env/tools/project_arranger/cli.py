from enum import Enum
from pathlib import Path
from typing import Dict, List

import git
import typer
from calmlib.utils import fix_path
from dotenv import load_dotenv
from loguru import logger
from rich.console import Console
from rich.table import Table

from dev_env.tools.project_arranger.src.main import Group, Project, ProjectArranger

# from .old.main import ProjectArranger

app = typer.Typer()
console = Console()

DEFAULT_CONFIG = Path(__file__).parent / "pa_config.yaml"
MISSING_THRESHOLD = 5  # Warn if more than this many projects are missing


class Action(str, Enum):
    SKIP = "skip"  # Same group, no action needed
    CLONE = "clone"  # Not present locally, needs cloning
    REMOVE = "remove"  # Should be moved to to_remove folder
    MOVE = "move"  # Should be moved to a different group


class Destination:
    base = fix_path(Path("~/work"))

    def __init__(self, name, path=None):
        self.name = name
        if path is None:
            self.path = self.base / name
        else:
            self.path = Path(path)

    def get_location(self, name):
        target = self.path / name
        if target.exists():
            raise FileExistsError(
                f"Destination {self.name} already has a project named {name}"
            )
        else:
            return target

    def move(self, project: Project):
        if not self.path.exists():
            self.path.mkdir(parents=True)
        try:
            # Ensure project path exists before attempting move
            if project.path is None:
                logger.error(f"Cannot move project {project.name}: path is None.")
                return
            location = self.get_location(project.name)
            project.path.rename(location)
        except Exception as e:
            logger.error(f"Failed to move {project.name} to {self.name}: {e}")


def get_destinations(config=None):
    destinations = {}
    # step 1 - add default destinations
    for group in Group.__members__.values():
        destinations[group.value] = Destination(group.value)
    # step 2 - add "to_remove" destination
    destinations["to_remove"] = Destination("to_remove")

    # todo: use config
    return destinations


@app.command()
def compare(
    config: Path = typer.Option(
        DEFAULT_CONFIG, "--config", "-c", help="Path to config file"
    ),
    show_ignored: bool = typer.Option(
        False, "--show-ignored", "-i", help="Show ignored projects"
    ),
    # sort_by: str = typer.Option("org", "--sort-by", "-s", help="Sort by: org, edited, created, name"),
):
    """Compare local and GitHub projects lists"""
    arranger = ProjectArranger(config)

    # Get raw project lists
    local_projects = arranger._build_projets_list_local()
    github_projects = arranger._build_projets_list_github()

    if not show_ignored:
        local_projects = [
            p for p in local_projects if arranger._sort_main_manual(p) != "ignore"
        ]

    # Sort function
    # def get_sort_key(project):
    #     if sort_by == "org":
    #         return (project.github_org or "", project.name)
    #     elif sort_by == "edited":
    #         return project.date
    #     elif sort_by == "created":
    #         return project.created_date
    #     return project.name
    #
    # # Sort projects
    # local_projects.sort(key=get_sort_key)
    # github_projects.sort(key=get_sort_key)
    #
    # # Print local projects
    # console.print("\n[blue]Local projects:[/blue]")
    # table = Table(show_header=True)
    # table.add_column("Name")
    # table.add_column("GitHub Info")
    # table.add_column("Last Updated")
    #
    # for proj in local_projects:
    #     github_info = f"{proj.github_org}/{proj.github_name}" if proj.github_org else "-"
    #     table.add_row(
    #         proj.name,
    #         github_info,
    #         proj.date.strftime("%Y-%m-%d"),
    #     )
    # console.print(table)
    #
    # # Print GitHub projects
    # console.print("\n[blue]GitHub projects:[/blue]")
    # table = Table(show_header=True)
    # table.add_column("Name")
    # table.add_column("Owner")
    # table.add_column("Last Updated")
    #
    # for proj in github_projects:
    #     table.add_row(
    #         proj.name,
    #         proj.github_org or "",
    #         proj.date.strftime("%Y-%m-%d"),
    #         )
    # console.print(table)

    # Print stats
    # Get project identifiers
    local_names = {
        (p.github_org, p.github_name) for p in local_projects if p.github_name
    }
    github_names = {(p.github_org, p.github_name) for p in github_projects}

    missing_locally = github_names - local_names
    missing_on_github = {
        (p.github_org, p.name) for p in local_projects if not p.github_name
    }

    # Sort by org, then name
    missing_locally = sorted(missing_locally)
    missing_on_github = sorted(missing_on_github)

    # Print results
    if missing_locally:
        console.print(f"\n[yellow]Missing locally ({len(missing_locally)}):[/yellow]")
        for org, name in missing_locally:
            proj = next(
                p
                for p in github_projects
                if p.github_name == name and p.github_org == org
            )
            console.print(
                f"  {org}/{name:<30} (Last updated: {proj.date.strftime('%Y-%m-%d')})"
            )
        if len(missing_locally) > MISSING_THRESHOLD:
            console.print(
                f"\n[red]Warning: {len(missing_locally)} projects missing locally. "
                "Consider cloning them or improving filters.[/red]"
            )

    if missing_on_github:
        console.print(
            f"\n[yellow]Missing on GitHub ({len(missing_on_github)}):[/yellow]"
        )
        for org, name in missing_on_github:
            proj = next(p for p in local_projects if p.name == name)
            console.print(
                f"  {org or '-'}/{name:<30} (Last edited: {proj.date.strftime('%Y-%m-%d')})"
            )
        if len(missing_on_github) > MISSING_THRESHOLD:
            console.print(
                f"\n[red]Warning: {len(missing_on_github)} projects not on GitHub. "
                "Consider pushing them or improving filters.[/red]"
            )

    if not missing_locally and not missing_on_github:
        console.print("\n[green]All projects are in sync![/green]")


@app.command()
def sort(
    config: Path = typer.Option(
        DEFAULT_CONFIG, "--config", "-c", help="Path to config file"
    ),
    dry_run: bool = typer.Option(
        True, "--execute", help="Actually execute the changes"
    ),
    show_all: bool = typer.Option(
        False, "--all", "-a", help="Show all projects, not just changes"
    ),
):
    load_dotenv()
    """Sort projects into appropriate groups"""
    arranger = ProjectArranger(config)

    # Get all projects
    projects = arranger.build_projects_list()

    # Get current and target groups
    current_groups = arranger.get_current_groups(projects)
    target_groups = arranger.sort_projects(projects)

    # Determine required actions for each project
    actions = _determine_actions(projects, current_groups, target_groups)

    # Print planned actions
    _print_actions(actions, show_all)

    # Execute if not dry run
    if not dry_run:
        console.print(
            "\n[yellow]This is a dry run. Use --execute to actually perform the changes.[/yellow]"
        )
        return

    # Check if there are any actions to execute
    has_actions = any(details["action"] != Action.SKIP for details in actions.values())

    if not has_actions:
        console.print("[green]No actions to execute![/green]")
        return

    if _confirm_actions():
        _execute_actions(actions)


def determine_group(project: Project, groups: Dict[Group, List[Project]]) -> Group:
    for group, projects in groups.items():
        if project in projects:
            return group

    # return Group(project.current_group)
    raise ValueError(f"Project {project.name} not found in groups")


def _determine_actions(
    projects: List[Project], current_groups: Dict, target_groups: Dict
) -> Dict[str, Dict]:
    """Determine required actions for each project"""
    actions = {}

    for project in projects:
        current_group = determine_group(project, current_groups["main"])
        target_group = determine_group(project, target_groups["main"])

        if not target_group:
            logger.warning(f"No target group found for {project.name}")
            continue

        # If target is experiments, replace with projects
        if target_group == Group.experiments:
            target_group = Group.actual  # Group.actual corresponds to 'projects' folder

        # Determine action
        if target_group == current_group:
            action = Action.SKIP
        elif target_group == Group.ignore:
            action = Action.REMOVE
        elif not project.path:
            action = Action.CLONE
        else:
            action = Action.MOVE

        actions[project.name] = {
            "project": project,
            "action": action,
            "current_group": current_group,
            "target_group": target_group,
            "reason": target_groups["main_reason"].get(project.name, "unknown"),
        }

    return actions


def _print_actions(actions: Dict[str, Dict], show_all: bool = False):
    """Print planned actions in a table format"""
    table = Table(show_header=True)
    table.add_column("Project")
    table.add_column("Action")
    table.add_column("From")
    table.add_column("To")
    table.add_column("Reason")

    for name, details in sorted(
        actions.items(), key=lambda x: (x[1]["action"], x[1]["target_group"])
    ):
        if not show_all and details["action"] == Action.SKIP:
            continue

        color = {
            Action.SKIP: "white",
            Action.CLONE: "green",
            Action.REMOVE: "red",
            Action.MOVE: "yellow",
        }[details["action"]]

        table.add_row(
            name,
            f"[{color}]{details['action']}[/{color}]",
            str(details["current_group"]),
            str(details["target_group"]),
            details["reason"],
        )

    console.print("\nPlanned actions:")
    console.print(table)

    # Print summary
    action_counts = {}
    for details in actions.values():
        action_counts[details["action"]] = action_counts.get(details["action"], 0) + 1

    console.print("\nSummary:")
    for action, count in action_counts.items():
        color = {
            Action.SKIP: "white",
            Action.CLONE: "green",
            Action.REMOVE: "red",
            Action.MOVE: "yellow",
        }[action]
        console.print(f"[{color}]{action}:[/{color}] {count}")


def _confirm_actions() -> bool:
    """Ask user to confirm actions"""
    return typer.confirm("\nDo you want to proceed with these changes?")


def _execute_actions(actions: Dict[str, Dict]):
    """Execute the planned actions"""
    destinations = get_destinations()
    with console.status("[bold green]Executing actions...") as status:
        for name, details in actions.items():
            project = details["project"]
            action = details["action"]
            target_group = details["target_group"]

            if action == Action.SKIP:
                continue

            try:
                if action == Action.CLONE:
                    status.update(f"[bold green]Cloning {name}...")
                    destination = destinations[target_group]
                    location = destination.get_location(name)
                    # Use Repository.clone_url directly since project.github_repo is a Repository instance
                    clone_url = project.github_repo.clone_url
                    git.Repo.clone_from(clone_url, location)
                    logger.info(f"Cloned {name} to {target_group}")

                elif action == Action.REMOVE:
                    # --- Protection: Check if project has remote before deletion ---
                    has_remote = False
                    if project.path and project.is_git_repo():
                        try:
                            repo = git.Repo(project.path)
                            has_remote = "origin" in repo.remotes
                        except Exception as git_err:
                            logger.debug(
                                f"Error checking remotes for {name}: {git_err}"
                            )

                    # Also check if project has GitHub repo metadata
                    has_github_repo = project.github_repo is not None

                    if not has_remote and not has_github_repo:
                        logger.warning(
                            f"ABORTING deletion of {name}: No remote repository found. "
                            "This appears to be a local-only project."
                        )
                        console.print(
                            f"[red]⚠️  SKIPPED: {name} - No remote repository found[/red]"
                        )
                        continue
                    # --- End Protection ---

                    status.update(f"[bold red]Moving {name} to to_remove...")
                    destination = destinations["to_remove"]

                    # --- Farewell commit ---
                    if project.path and project.is_git_repo():
                        try:
                            repo = git.Repo(project.path)
                            # Check if repo has origin remote
                            if "origin" in repo.remotes:
                                logger.info(f"Performing farewell commit for {name}...")
                                # Create and checkout new branch
                                farewell_branch = "farewell-commit"
                                try:
                                    # Delete branch if it exists locally
                                    repo.delete_head(farewell_branch, force=True)
                                except git.GitCommandError:
                                    pass  # Branch didn't exist, ignore
                                new_branch = repo.create_head(farewell_branch)
                                new_branch.checkout()

                                # Stage all changes
                                repo.git.add(A=True)

                                # Commit if there are changes
                                if repo.is_dirty(index=True, working_tree=False):
                                    repo.index.commit(
                                        "Final commit before archival by project-arranger"
                                    )
                                    logger.info(
                                        f"Committed changes to {farewell_branch} for {name}"
                                    )

                                    # Push the new branch
                                    try:
                                        repo.git.push(
                                            "origin", farewell_branch, force=True
                                        )  # Use force push in case branch exists remotely
                                        logger.info(
                                            f"Pushed {farewell_branch} to origin for {name}"
                                        )
                                    except git.GitCommandError as push_err:
                                        logger.warning(
                                            f"Failed to push farewell branch for {name}: {push_err}"
                                        )
                                else:
                                    logger.info(
                                        f"No changes to commit for {name} in {farewell_branch}"
                                    )

                                # Optionally switch back to the original branch if needed,
                                # but since we're removing it, it might not matter.
                                # Consider adding repo.heads.main.checkout() or similar if necessary.

                            else:
                                logger.warning(
                                    f"Skipping farewell commit for {name}: No 'origin' remote found."
                                )
                        except Exception as git_err:
                            logger.error(
                                f"Error during farewell git operations for {name}: {git_err}"
                            )
                    # --- End Farewell commit ---

                    destination.move(project)
                    logger.info(f"Moved {name} to to_remove")

                elif action == Action.MOVE:
                    # If current group is experiments, or target group is experiments, use projects instead
                    actual_target_group = (
                        "projects" if target_group == "experiments" else target_group
                    )
                    status.update(
                        f"[bold yellow]Moving {name} to {actual_target_group}..."
                    )
                    destination = destinations[actual_target_group]
                    destination.move(project)
                    logger.info(f"Moved {name} to {actual_target_group}")

            except Exception as e:
                logger.error(f"Failed to process {name}: {e}")

    console.print("[bold green]Done![/bold green]")


if __name__ == "__main__":
    load_dotenv()
    app()

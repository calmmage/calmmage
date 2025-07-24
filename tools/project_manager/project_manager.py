import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

import git
from calmlib.utils.main import is_subsequence
from loguru import logger

from src.lib.pm_utils.destinations import Destination, DestinationsRegistry
from src.lib.pm_utils.project_utils import ProjectDiscovery
from tools.project_manager.pm_config import ProjectManagerConfig


class ProjectManager:
    def __init__(
        self,
        config_path: Optional[Path] = None,
        destinations_config_path: Optional[Path] = None,
    ):
        """Initialize Project Manager with configuration"""
        if config_path is None:
            config_path = Path(__file__).parent / "pm_config.yaml"

        self.config = ProjectManagerConfig.from_yaml(config_path)
        self.discovery = ProjectDiscovery()
        self.destinations = DestinationsRegistry(destinations_config_path)
        self._github_token = None
        self._github_client = None
        self._templates = None

    # ------------------------------------------------------------
    # region GitHub
    # ------------------------------------------------------------

    @property
    def github_token(self) -> str:
        """Get GitHub token from environment variables"""
        if self._github_token is None:
            # Try to load from ~/.env first, then system env vars
            env_path = Path.home() / ".env"
            if env_path.exists():
                from dotenv import load_dotenv

                logger.debug(f"Loading GitHub token from {env_path}")

                load_dotenv(env_path)
            else:
                logger.debug(f"No .env file found at {env_path}")

            token = os.getenv("GITHUB_API_TOKEN")
            if token is None:
                raise ValueError(
                    "Missing GitHub API token. "
                    "Please add it to ~/.env or system environment variables. "
                )
            self._github_token = token
        return self._github_token

    @property
    def github_client(self):
        """Get GitHub client instance"""
        if self._github_client is None:
            from github import Github

            self._github_client = Github(self.github_token)
        return self._github_client

    # todo: cache locally on disk?
    def get_templates(self, reset_cache=False):
        """Get all available GitHub templates"""
        if self._templates is None or reset_cache:
            repos = self.github_client.get_user().get_repos()
            self._templates = {repo.name: repo for repo in repos if repo.is_template}
        return self._templates

    @staticmethod
    def _fuzzy_match_template_name(
        incomplete: str, candidates: list[Tuple[str, str]]
    ) -> list[Tuple[str, str]]:
        """Fuzzy match the template name from candidates."""
        matches = []
        # step 1 - match by exact prefix
        for template, help_text in candidates:
            if template.startswith(incomplete):
                matches.append((template, help_text))
        if len(matches) == 1:
            return matches

        # step 2 - match by any subsequence
        for template, help_text in candidates:
            if is_subsequence(incomplete, template):
                matches.append((template, help_text))

        if len(matches) == 1:
            return matches
        # hack: always add the incomplete string to avoid typer error (broken completion)
        # todo: report the issue to typer
        matches.append((incomplete, ""))
        return matches

    def complete_template_name(self, incomplete: str) -> list[Tuple[str, str]]:
        """Complete template name with fuzzy matching."""
        templates_dict = (
            self.get_templates()
        )  # This returns a dict: {template_name: repo_object}
        # Transform the dict into a list of tuples (template_name, help_text)
        candidates = [
            (name, repo.description or "") for name, repo in templates_dict.items()
        ]
        matches = self._fuzzy_match_template_name(incomplete, candidates)
        return matches

    templates_path = Path(__file__).parent / "templates"

    def complete_mini_template_name(self, incomplete: str) -> list[Tuple[str, str]]:
        """Complete mini-project template name with fuzzy matching."""
        templates = [p for p in self.templates_path.glob("*") if p.is_dir()]
        candidates = [(p.name, str(p)) for p in templates]
        matches = self._fuzzy_match_template_name(incomplete, candidates)
        return matches

    def _create_repo_from_template(
        self, name: str, template_name: str, dry_run: bool = False
    ) -> str:
        """Create a new GitHub repository from template"""
        logger.debug(f"Creating repository {name} from template: {template_name}")

        github_client = self.github_client
        username = github_client.get_user().login

        # Validate template
        templates = self.get_templates()
        if template_name not in templates:
            raise ValueError(
                f"Invalid template: {template_name}. Available: {list(templates.keys())}"
            )

        # Check if repo exists
        if name in [repo.name for repo in github_client.get_user().get_repos()]:
            raise ValueError(
                f"Repository already exists: https://github.com/{username}/{name}"
            )

        # Create repo from template
        params = {
            "verb": "POST",
            "url": f"/repos/{username}/{template_name}/generate",
            "input": {"owner": username, "name": name},
        }
        if not dry_run:
            github_client._Github__requester.requestJsonAndCheck(**params)

            url = f"https://github.com/{username}/{name}"
            logger.debug(f"Repository created: {url}")
            return url
        else:
            logger.info(f"Dry run: would have created repository {params}")
            return f"https://github.com/{username}/{name}"

    def _clone_github_repository(
        self, name: str, project_dir: Path, retries: int = 3, retry_delay: int = 5
    ):
        """Clone GitHub repository to local directory"""
        project_dir = Path(project_dir)
        username = self.github_client.get_user().login
        url = f"https://{self.github_token}@github.com/{username}/{name}.git"

        if project_dir.exists() and list(project_dir.iterdir()):
            raise ValueError(f"Project directory not empty: {project_dir}")

        for i in range(retries):
            try:
                repo = git.Repo.clone_from(url, str(project_dir))
                repo.git.pull()

                # Verify clone success
                if not (project_dir / ".git").exists():
                    raise ValueError(
                        "Repository cloned but .git directory not found where expected"
                    )

                logger.debug(f"Repository cloned successfully to {project_dir}")
                return project_dir

            except Exception as e:
                logger.warning(f"Clone attempt {i+1} failed: {e}")
                if project_dir.exists():
                    try:
                        import shutil

                        shutil.rmtree(project_dir)
                        logger.debug(
                            f"Cleaned up failed clone attempt at {project_dir}"
                        )
                    except Exception as cleanup_error:
                        logger.warning(f"Failed to clean up directory: {cleanup_error}")

                if i < retries - 1:
                    import time

                    time.sleep(retry_delay)
                    continue
                raise

    def _check_github_conflicts(self, name: str) -> bool:
        """Check if name conflicts with existing GitHub repos"""
        try:
            # Try to get repo - if it exists, there's a conflict
            self.github_client.get_user().get_repo(name)
            return True
        except Exception:
            # If repo not found, no conflict
            return False

    def _detect_bot_project(self, name: str) -> bool:
        """Detect if project name indicates a bot project"""
        return (
            "-bot" in name.lower()
            or "_bot" in name.lower()
            or "bot-" in name.lower()
            or "bot_" in name.lower()
        )

    # endregion GitHub

    # ------------------------------------------------------------
    # region New Project
    # ------------------------------------------------------------

    def _get_experiments_destination(self) -> Path:
        """Get experiments destination from config"""
        dest_key = self.config.experiments_destination
        return self.destinations.get(dest_key).path

    def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        template: Optional[str] = None,
        dry_run: bool = False,
    ):
        """Create a new project in experiments destination using GitHub template."""
        # Auto-detect bot projects and set template if none provided
        if template is None:
            if self._detect_bot_project(name):
                template = "botspot-template"
                logger.info(f"Auto-detected bot project, using template: {template}")
            else:
                template = "python-project-template"
        else:
            # Validate provided template name
            matches = self.complete_template_name(template)
            if len(matches) == 1:
                template = matches[0][0]
            else:
                raise ValueError(
                    f"Ambiguous template name: {template}. Matches: {matches}"
                )

        if self.config.always_use_hyphens and ("_" in name):
            name = name.replace("_", "-")
            logger.info(
                f"Auto converted underscores to hyphens in project name: {name}"
            )

        # Check GitHub conflicts
        if self._check_github_conflicts(name):
            raise ValueError(
                f"Project name '{name}' conflicts with existing GitHub repository"
            )

        try:
            # Create repo from template
            self._create_repo_from_template(name, template, dry_run)

            # Add a small delay to ensure GitHub has initialized the repository
            import time

            time.sleep(2)  # Wait 2 seconds before attempting to clone

            # Get destination from config
            destination = self._get_experiments_destination()
            project_dir = destination / name

            if project_dir.exists():
                if list(project_dir.iterdir()):
                    raise ValueError(
                        f"Project directory already exists and is not empty: {project_dir}"
                    )
                else:
                    # remove empty dir
                    project_dir.rmdir()
                    logger.warning(
                        f"Removed pre-existing empty project directory: {project_dir}"
                    )

            if not dry_run:
                self._clone_github_repository(name, project_dir)
            else:
                logger.info(f"Dry run: would have cloned to {project_dir}")

        except Exception as e:
            logger.error(f"Failed to create GitHub project: {e}")
            raise

        logger.info(f"Project '{name}' created successfully at {project_dir}")
        return project_dir

    # endregion New Project

    # ------------------------------------------------------------
    # region Mini Project
    # ------------------------------------------------------------

    def _get_mini_projects_destination(self, private: bool = False) -> Destination:
        """Get mini-projects destination from config"""
        dest_key = (
            self.config.private_mini_projects_destination
            if private
            else self.config.public_mini_projects_destination
        )
        return self.destinations.get(dest_key)

    def _get_latest_seasonal_folder(self, destination: Destination) -> Optional[Path]:
        """Get latest seasonal folder"""
        seasonal_base = destination.path / "experiments"

        # option 1: check all seasonal folders
        existing_seasons = [p for p in seasonal_base.glob("season_*") if p.is_dir()]
        logger.debug(
            f"Found {len(existing_seasons)} seasonal folders: {[s.name for s in existing_seasons]}"
        )

        latest_season = None
        latest_season_num = -1
        for season in existing_seasons:
            season_num = int(season.name.split("_")[1])
            if season_num > latest_season_num:
                latest_season_num = season_num
                latest_season = season

        logger.debug(f"Latest season by number: {latest_season}")

        # option 2: check latest symlink
        latest_link = seasonal_base / "latest"
        if latest_link.exists() and latest_link.is_symlink():
            res = Path(os.readlink(latest_link))
            if res != latest_season:
                logger.warning(
                    f"Latest symlink exists but points to {res}, not {latest_season}"
                )
            logger.debug(f"Latest season by symlink: {res}")

        return latest_season

    def _create_new_seasonal_folder(
        self, destination: Destination, season_num: Optional[int] = None
    ):
        """Create a new seasonal folder"""
        if season_num is None:
            season_num = 1
        logger.debug(f"Creating new seasonal folder with number {season_num}")

        date = datetime.now()
        logger.debug(f"Current date: {date}")
        period = self._get_period_from_date_range(date, date)
        logger.debug(f"Generated period: {period}")

        new_folder = (
            destination.path
            / "experiments"
            / f"season_{season_num}_{period}_{date.year}"
        )
        logger.debug(f"New folder path: {new_folder}")
        new_folder.mkdir(parents=True, exist_ok=True)

        # update latest symlink
        latest_link = destination.path / "experiments" / "latest"
        if latest_link.exists() or latest_link.is_symlink():
            logger.debug(f"Removing existing symlink: {latest_link}")
            latest_link.unlink()
        logger.debug(f"Creating new symlink: {latest_link} -> {new_folder}")
        latest_link.symlink_to(new_folder)

        # create folder structure
        # children = ["draft", "wip", "unsorted", "paused"]
        # for child in children:
        #     (new_folder / child).mkdir(exist_ok=True)
        # logger.debug(f"Created folder structure: {children}")

        return new_folder

    months = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]

    def _get_period_from_date_range(self, start: datetime, end: datetime) -> str:
        """Get season name from date range

        within a month -> this month (1-20 jan - 'jan')
        covering two months -> both
        covering a quarter -> quarter name"""
        logger.debug(f"Getting period for date range: {start} - {end}")

        if start.month == end.month:
            period = self.months[start.month - 1]
            logger.debug(f"Same month period: {period}")
            return period
        elif (start.month + 1) % 12 == end.month:
            # if just 2 months
            period = f"{self.months[start.month - 1]}-{self.months[end.month - 1]}"
            logger.debug(
                f"Two month period: {period} (months {start.month}-{end.month})"
            )
            return period

        # warn if time span is too long
        if (end - start).days > 90:
            logger.warning(f"Season spans multiple quarters: {start} - {end}")

        # winter, spring, summer or fall - based on the end month
        if end.month in [12, 1, 2]:
            logger.debug(f"Winter period (end month: {end.month})")
            return "winter"
        elif end.month in [3, 4, 5]:
            logger.debug(f"Spring period (end month: {end.month})")
            return "spring"
        elif end.month in [6, 7, 8]:
            logger.debug(f"Summer period (end month: {end.month})")
            return "summer"
        else:
            logger.debug(f"Fall period (end month: {end.month})")
            return "fall"

    def _time_to_roll_season(self, season: Path) -> bool:
        """Check if it's time to roll over to a new season"""
        # if already enough projects within season
        num_projects = len(list(season.glob("*/*")))
        threshold = self.config.seasonal_folder_threshold
        if num_projects >= threshold:
            logger.debug(
                f"Enough projects in season: {num_projects=} >= {threshold=}. Rolling over."
            )
            return True

        # or season date range grows too large / awkward
        # i need some kind of metadata for that.. ?
        metadata = self._get_season_metadata(season)
        start = datetime.fromisoformat(metadata["start"])
        end = datetime.now()
        if (end - start).days > 90:
            logger.debug(
                f"Season date range too large: {end - start} days. Rolling over."
            )
            return True
        if (end - start).days > 60:
            # check if we're spanning multiple different quarters
            if start.month in [12, 1, 2] and end.month in [3, 4, 5]:
                logger.debug(
                    "Season spans multiple quarters: winter -> spring. Rolling over."
                )
                return True
            elif start.month in [3, 4, 5] and end.month in [6, 7, 8]:
                logger.debug(
                    "Season spans multiple quarters: spring -> summer. Rolling over."
                )
                return True
            elif start.month in [6, 7, 8] and end.month in [9, 10, 11]:
                logger.debug(
                    "Season spans multiple quarters: summer -> fall. Rolling over."
                )
                return True
            elif start.month in [9, 10, 11] and end.month in [12, 1, 2]:
                logger.debug(
                    "Season spans multiple quarters: fall -> winter. Rolling over."
                )
                return True
        return False

    def _get_season_metadata_file(self, season: Path) -> Path:
        return season / "metadata.json"

    def _parse_name_into_date_range(self, name: str) -> Tuple[datetime, datetime]:
        """Parse season name into start and end date"""
        logger.debug(f"Parsing season name: {name}")
        if name.startswith("season_"):
            name = name.split("_", 2)[2]
        parts = name.split("_")
        if len(parts) == 2:
            year = int(parts[1])
            season = parts[0]
            logger.debug(f"Parsed year: {year}, season: {season}")

            if season == "winter":
                start = datetime(year, 12, 1)
                end = datetime(year + 1, 2, 28)
                logger.debug(f"Winter season: {start} - {end}")
            elif season == "spring":
                start = datetime(year, 3, 1)
                end = datetime(year, 5, 31)
                logger.debug(f"Spring season: {start} - {end}")
            elif season == "summer":
                start = datetime(year, 6, 1)
                end = datetime(year, 8, 31)
                logger.debug(f"Summer season: {start} - {end}")
            elif season == "fall":
                start = datetime(year, 9, 1)
                end = datetime(year, 11, 30)
                logger.debug(f"Fall season: {start} - {end}")
            else:
                if season in self.months:
                    logger.debug(f"Single month: {season}")
                    start_month_index = self.months.index(season) + 1
                    end_month_index = (start_month_index + 1) % 12
                    year_end = year + (start_month_index + 1) // 12
                    start = datetime(year, start_month_index, 1)
                    end = datetime(year_end, end_month_index, 1) - timedelta(days=1)
                    logger.debug(f"Single month dates: {start} - {end}")
                elif "-" in season:
                    start_month, end_month = season.split("-")
                    logger.debug(f"Month range: {start_month}-{end_month}")
                    start_month_index = self.months.index(start_month) + 1
                    end_month_index = self.months.index(end_month) + 1
                    start = datetime(year, start_month_index, 1)

                    if end_month_index <= start_month_index:
                        end = datetime(year + 1, end_month_index + 1, 1) - timedelta(
                            days=1
                        )
                        logger.debug(f"Year boundary crossed: {start} - {end}")
                    else:
                        end = datetime(year, end_month_index + 1, 1) - timedelta(days=1)
                        logger.debug(f"Same year range: {start} - {end}")
                else:
                    raise ValueError(f"Invalid season name: {name}")

        else:
            raise ValueError(f"Invalid season name format: {name}")

        logger.debug(f"Final date range for {name}: {start} - {end}")
        return start, end

    def _init_season_metadata(self, season: Path):
        """Initialize season metadata"""
        metadata_file = self._get_season_metadata_file(season)
        start, end = self._parse_name_into_date_range(season.name)
        metadata = {
            "start": start.isoformat(),
            "end": end.isoformat(),
        }
        metadata_file.write_text(json.dumps(metadata))
        return metadata

    def _get_season_metadata(self, season: Path) -> dict:
        """Get season metadata"""
        metadata_file = self._get_season_metadata_file(season)
        if metadata_file.exists():
            return json.loads(metadata_file.read_text())
        else:
            return self._init_season_metadata(season)

    # def _update_season_dates(
    #     self,
    #     season: Path,
    #     start: Optional[datetime] = None,
    #     end: Optional[datetime] = None,
    # ) -> Path:
    #     """Update season name and folder to the latest date range"""
    #     metadata = self._get_season_metadata(season)
    #     _, num, period, year = season.name.split("_")
    #     if start is None:
    #         start = datetime.fromisoformat(metadata["start"])
    #     if end is None:
    #         end = datetime.fromisoformat(metadata["end"])
    #     period = self._get_period_from_date_range(start, end)
    #
    #     # Calculate new name and path
    #     new_name = f"season_{num}_{period}_{year}"
    #     new_path = season.with_name(new_name)
    #
    #     # Only proceed with rename if needed
    #     # if new_name != season.name:
    #     # disable renaming for now - this is a disaster from git perspective
    #     # if False:
    #     #     logger.info(f"Auto-renaming season folder from {season.name} to {new_name}")
    #     #
    #     #     # Update latest symlink first if it points to this season
    #     #     latest_link = season.parent / "latest"
    #     #     if latest_link.exists() and latest_link.is_symlink():
    #     #         try:
    #     #             if latest_link.resolve() == season.resolve():
    #     #                 latest_link.unlink()
    #     #                 season.rename(new_path)
    #     #                 latest_link.symlink_to(new_path)
    #     #                 # Update metadata in new location
    #     #                 metadata = {"start": start.isoformat(), "end": end.isoformat()}
    #     #                 new_metadata_file = self._get_season_metadata_file(new_path)
    #     #                 new_metadata_file.write_text(json.dumps(metadata))
    #     #                 return new_path
    #     #         except OSError as e:
    #     #             logger.warning(f"Error handling symlink: {e}")
    #     #
    #     #     # If no symlink or it points elsewhere, just rename
    #     #     season.rename(new_path)
    #     #
    #     #     # Update metadata in new location
    #     #     metadata = {"start": start.isoformat(), "end": end.isoformat()}
    #     #     new_metadata_file = self._get_season_metadata_file(new_path)
    #     #     new_metadata_file.write_text(json.dumps(metadata))
    #     # else:
    #     # Just update metadata if no rename needed
    #     metadata = {"start": start.isoformat(), "end": end.isoformat()}
    #     metadata_file = self._get_season_metadata_file(season)
    #     metadata_file.write_text(json.dumps(metadata))
    #
    #     return new_path

    def get_seasonal_folder(self, private: bool = False) -> Path:
        """Get or create appropriate seasonal folder based on count and time thresholds"""
        destination = self._get_mini_projects_destination(private=private)
        # - check if time to roll
        latest_season = self._get_latest_seasonal_folder(destination)
        logger.debug(f"Found latest season: {latest_season}")

        if latest_season is None:
            # create new
            logger.debug("No existing season found, creating new")
            latest_season = self._create_new_seasonal_folder(destination)
        elif self._time_to_roll_season(latest_season):
            # roll over
            logger.info(f"Time to roll season {latest_season}")
            latest_season = self._create_new_seasonal_folder(
                destination, season_num=int(latest_season.name.split("_")[1]) + 1
            )

        # - sanity check name
        # logger.debug(f"Updating season dates for {latest_season}")
        # latest_season = self._update_season_dates(latest_season, end=datetime.now())
        logger.debug(f"Final season folder: {latest_season}")

        return latest_season

    #     return project_dir
    def create_mini_project(
        self,
        name: str,
        idea: Optional[str] = None,
        private: bool = False,
        dry_run: bool = False,
        template: Optional[str] = None,
    ) -> Path:
        """Create a new mini-project in seasonal folder structure

        Args:
            name: Project name
            idea: Project idea/description
            private: Whether to create in private repository
            dry_run: If True, only print what would be done
            template: Template name to use. If None, auto-detects based on name.
        """
        # Auto-detect bot projects and set template if none provided
        if template is None:
            if self._detect_bot_project(name):
                template = "mini-botspot-template"
                logger.info(f"Auto-detected bot project, using template: {template}")
        else:
            # Validate provided template name
            matches = self.complete_mini_template_name(template)
            if len(matches) == 1:
                template = matches[0][0]
            else:
                raise ValueError(
                    f"Ambiguous template name: {template}. Matches: {matches}"
                )

        # - locate seasonal dir
        seasonal_folder = self.get_seasonal_folder(private=private)

        if self.config.always_use_hyphens:
            if "_" in name:
                name = name.replace("_", "-")
                logger.info(
                    f"Auto converted underscores to hyphens in project name: {name}"
                )

        # - create dir
        # draft_dir = seasonal_folder / "draft"
        project_dir = seasonal_folder / name
        # project_dir = draft_dir / name

        if project_dir.exists():
            if list(project_dir.iterdir()):
                raise ValueError(
                    f"Project directory already exists and is not empty: {project_dir}"
                )
            else:
                logger.warning(f"Directory already exists but is empty: {project_dir}")

        if not dry_run:
            # Ensure draft directory exists
            draft_dir.mkdir(exist_ok=True, parents=True)

            if template:
                # Copy template contents
                template_path = self._get_template_path(template)
                if not template_path.exists():
                    raise ValueError(f"Template not found: {template_path}")

                import shutil

                shutil.copytree(template_path, project_dir, dirs_exist_ok=True)

                # Update project name in files if needed
                self._update_template_project_name(project_dir, name)

                logger.info(f"Initialized from template: {template}")
            else:
                # Create empty directory
                project_dir.mkdir(exist_ok=True)

            # - put idea there (append to existing idea.md if it exists)
            idea_file_path = project_dir / "idea.md"
            if idea:
                if idea_file_path.exists():
                    current_content = idea_file_path.read_text()
                    if not current_content.strip():
                        # File is empty, write new content
                        idea_file_path.write_text(f"# {name}\n\n{idea}\n")
                    else:
                        # Append to existing content
                        idea_file_path.write_text(f"{current_content}\n\n{idea}\n")
                else:
                    idea_file_path.write_text(f"# {name}\n\n{idea}\n")
        else:
            logger.info(f"Dry run: Would create directory at {project_dir}")
            if template:
                logger.info(f"Dry run: Would initialize from template: {template}")
            if idea:
                logger.info(
                    f"Dry run: Would create idea.md with content:\n# {name}\n\n{idea}\n"
                )

        return project_dir

    def _update_template_project_name(self, project_dir: Path, name: str):
        """Update project name in template files"""
        # Update _app.py if it exists
        app_file = project_dir / "_app.py"
        if app_file.exists():
            content = app_file.read_text()
            content = content.replace(
                "Mini Botspot Template", name.replace("-", " ").title()
            )
            app_file.write_text(content)
            logger.debug(f"Updated project name in {app_file}")

    def _get_template_path(self, template_name: str) -> Path:
        """Get the path to a template directory"""
        # First check in the tool's templates directory
        template_path = Path(__file__).parent / "templates" / template_name
        if template_path.exists():
            return template_path

        raise ValueError(
            f"Template not found: {template_name}. "
            f"Checked paths:\n"
            f"- {template_path}\n"
        )

    # endregion Mini Project

    # ------------------------------------------------------------
    # region WIP
    # ------------------------------------------------------------

    def _validate_name_with_ai(self, name: str) -> tuple[bool, Optional[str]]:
        """Validate name with AI and optionally get suggestion"""
        # TODO: Implement actual AI validation using query_gpt
        # prompt = f"""Is '{name}' a good project name? Consider:
        # - Clarity and descriptiveness
        # - Length (should be concise)
        # - Standard naming conventions
        #
        # Return format:
        # VALID: true/false
        # SUGGESTION: better-name (only if VALID is false)
        # """
        # Placeholder implementation
        return True, None

    # def create_todo(
    #     self,
    #     name: Optional[str] = None,
    #     project: Optional[str] = None
    # ):
    #     """Create a new todo file"""
    #     if project is None:
    #         project = self.discovery.get_current_project()

    #     if name is None:
    #         name = datetime.now().strftime(self.config.todo_filename_template)

    #     todo_path = Path(project) / self.config.todo_subfolder / name
    #     logger.info(f"Creating todo at {todo_path}")
    #     raise NotImplementedError()

    # def create_feature(
    #     self,
    #     name: str,
    #     description: Optional[str] = None,
    #     project: Optional[str] = None
    # ):
    #     """Create a new feature draft"""
    #     if project is None:
    #         project = self.discovery.get_current_project()

    #     feature_path = Path(project) / self.config.features_subfolder / name
    #     logger.info(f"Creating feature at {feature_path}")
    # raise NotImplementedError()

    # endregion WIP

    def _get_examples_destination(self) -> Path:
        """Get examples destination from config"""
        dest_key = "examples"
        return self.destinations.get(dest_key).path

    def move_to_examples(self, path: Path):
        """Move a file or directory to examples destination"""
        examples_dest = self._get_examples_destination()
        unsorted = examples_dest / "unsorted"
        unsorted.mkdir(exist_ok=True)
        # check if exists
        target = unsorted / path.name
        if target.exists():
            logger.warning(f"Target already exists: {target}. Skipping.")
            if path.is_dir():
                target = target.with_suffix(
                    f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
            else:
                target = target.with_suffix(
                    f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{path.suffix}"
                )

        path.rename(target)
        logger.debug(f"Moved {path} to examples/unsorted at {target}")
        return target

    def open_in_editor(self, path: Path):
        """Open a file in the default editor"""
        cmd = self.config.default_editor
        cmd += f" {path}"
        logger.debug(f"Opening {path} in {cmd}")
        os.system(cmd)

    def rollup_todos(self, project_dir: Optional[Path] = None) -> Optional[Path]:
        """Roll up old todo_{date}.md files into a single todo.md file.
        Excludes today's todo file from the rollup.

        Args:
            project_dir: Project directory to check. If None, uses current project.

        Returns:
            Path to the rolled-up todo.md file if any todos were found, None otherwise.
        """
        if project_dir is None:
            current_project = self.discovery.get_current_project()
            if current_project is None:
                raise ValueError(
                    "No current project found and no project_dir specified"
                )
            project_dir = current_project.path

        # Get todo directory
        todo_dir = project_dir / self.config.todo_subfolder
        if not todo_dir.exists():
            logger.debug(f"No todo directory found at {todo_dir}")
            return None

        # Get today's todo filename to exclude it
        today_filename = datetime.now().strftime(self.config.todo_filename_template)

        # Find all todo files except today's
        todo_files = [f for f in todo_dir.glob("todo_*.md") if f.name != today_filename]

        if not todo_files:
            logger.debug("No old todo files found to roll up")
            return None

        # Sort files by date (newest first)
        todo_files.sort(reverse=True)

        # Create rolled up content
        rolled_content = []
        for todo_file in todo_files:
            # Extract date from filename (assuming format todo_17_Nov.md)
            date_str = todo_file.stem.replace("todo_", "")
            try:
                date = datetime.strptime(date_str, "%d_%b")
                header = f"# Todos from {date.strftime('%d %b')}\n\n"
            except ValueError:
                # If filename doesn't match expected format, use filename as header
                header = f"# {todo_file.stem}\n\n"

            content = todo_file.read_text().strip()
            rolled_content.append(f"{header}{content}\n\n")
        # Write rolled up content
        rolled_up_path = todo_dir / "todo.md"
        if rolled_up_path.exists():
            existing_content = rolled_up_path.read_text()
            rolled_content.append(existing_content)
        rolled_up_path.write_text("".join(rolled_content))
        # Delete old files
        for todo_file in todo_files:
            todo_file.unlink()
        logger.info(f"Rolled up {len(todo_files)} todo files into {rolled_up_path}")

        return rolled_up_path

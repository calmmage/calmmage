from datetime import datetime, timedelta
from pathlib import Path

from dev_env.core.constants import (
    all_projects_dirs,
    archive_dir,
    contexts_dir,
    experiments_dir,
    projects_dir,
    seasonal_dir,
)
from dev_env.core.git_utils import (
    check_repo_allowed,
    check_repo_cloned,
    clone_repo,
    create_and_clone_repo,
    get_all_repos,
)
from dev_env.core.settings import settings
from dev_env.setup.setup_shell_profiles_and_env import git_pull_with_fetch
from git import Repo
from loguru import logger
from pytz import timezone
from tenacity import retry, stop_after_attempt, wait_exponential


# plan:
# idea 1: create all projects dirs
# idea 2: clone all projects - if exists, pull
# idea 3: script to set up seasonal folder
# idea 4 - set up ~/.calmmage dir
# [x] nix - idea 5 - build zshrc file
# idea 6 - set up ~/code dir - softlinks to key locations
# idea 7, essential - daily job

# class MyDevEnv:
#     def __init__(self, **kwargs):
#         self.settings = MySettings(**kwargs)
#         self._github_client = None

#     @property
#     def github_client(self):
#         if self._github_client is None:
#             self._github_client = Github(self.settings.github_api_token)
#         return self._github_client

#     def setup(self):
#         self.create_dirs()
#         self.clone_projects()


# region  idea 1


def create_dirs():
    settings.root_dir.mkdir(parents=True, exist_ok=True)
    settings.symlinks_dir.mkdir(parents=True, exist_ok=True)
    settings.env_dir.mkdir(parents=True, exist_ok=True)

    for dir_path in all_projects_dirs:
        # for dir in settings.structural_dirs:
        # dir_path = settings.root_dir / dir
        if not dir_path.exists():
            dir_path.mkdir()


# endregion

# region idea 2 - clone projects


# todo: move to utils


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def clone_single_repo(repo, target_dir):
    try:
        local_repo_path = check_repo_cloned(repo)
        if local_repo_path:
            if (
                repo.name in settings.main_projects
                and local_repo_path.parent != projects_dir
            ):
                logger.warning(f"Main repo {local_repo_path} is not in {projects_dir}")
                logger.info(f"Moving {local_repo_path} to {projects_dir}")
                local_repo_path.rename(projects_dir / local_repo_path.name)
                local_repo_path = projects_dir / local_repo_path.name

            try:
                local_repo = Repo(local_repo_path)
                git_pull_with_fetch(local_repo)
                logger.info(f"Successfully pulled changes for {local_repo_path}")
            except Exception as e:
                logger.error(f"Failed to pull {local_repo_path}: {e}")
            return

        # clone
        # determine target dir
        # if created in last month -> experiments
        # if in main repos -> projects
        # else -> archive

        moscow_tz = timezone("Europe/Moscow")
        repo_creation_date = repo.created_at.astimezone(moscow_tz)
        if repo_creation_date > datetime.now(moscow_tz) - timedelta(days=30):
            target_dir = experiments_dir
        elif repo.name in settings.main_projects:
            target_dir = projects_dir
        else:
            target_dir = archive_dir

        target_path = target_dir / repo.name
        clone_repo(repo, target_path)
        logger.info(f"Successfully cloned {repo.name} to {target_path}")
    except Exception as e:
        logger.error(f"Failed to clone or update repo {repo.name}: {e}")
        raise


def clone_projects():
    # list all projects in my github
    # select only the ones in the accounts_to_clone_from
    # clone main projects to projects dir
    # clone other projects to archive dir

    # logic 1: what to do if dir exists - pull
    # logic 2: first check if repo is cloned _somewhere_
    # main repos -> move to projects dir
    # others -> don't touch

    repos_list = get_all_repos()
    for repo in repos_list:
        if not check_repo_allowed(repo):
            continue

        try:
            clone_single_repo(
                repo, None
            )  # We'll determine the target_dir inside the function
        except Exception as e:
            logger.error(
                f"Failed to process repo {repo.name} after multiple attempts: {e}"
            )


# endregion idea 2 - clone projects

# region idea 3 - seasonal folder

#
# seasonal/
# ├── yy-mm-mmm
# ├── ── dev-yy-mm (git, poetry)
# ├── ── ── draft [THIS IS MAIN ENTRY POINT]
# ├── ── ── wip
# ├── ── ── paused
# ├── ──p1 (git, poetry)
# ├── ──p2 ...
# ├── yy-mm-mmm
# ├── latest

# a) need a github repo template for dev-seasonal dir - simple: poetry, cursor workspace, draft, wip, paused
# b) softlink seasonal folder to latest
# c)
# d) 'new_project' tool -
# - option 1: draft -> seasonal folder
# - option 2: project -> always a git repo -> seasonal folder AND experiments folder


# todo: move to utils
def get_seasonal_dir(dt: datetime = None) -> Path:
    if dt is None:
        dt = datetime.now()
    seasonal_dir_name = dt.strftime("%Y-%m-%b")
    target_dir = seasonal_dir / seasonal_dir_name
    return target_dir


def get_seasonal_dev_dir(dt: datetime = None) -> Path:
    if dt is None:
        dt = datetime.now()
    seasonal_dir_path = get_seasonal_dir(dt)
    seasonal_dev_dir_name = dt.strftime("dev-%b-%Y".lower())
    return seasonal_dir_path / seasonal_dev_dir_name


def setup_seasonal_folder(dt: datetime = None):
    """
    Create a new seasonal folder and populate it with a dev repo from template.
    Link seasonal folder to latest.
    Args:
        dt (datetime): datetime object for seasonal folder name. If None, use current datetime.
    """
    logger.info("Setting up seasonal folder")
    if dt is None:
        dt = datetime.now()
    seasonal_dir_path = get_seasonal_dir(dt)
    logger.debug(f"Seasonal directory path: {seasonal_dir_path}")

    if not (seasonal_dir_path.exists() and list(seasonal_dir_path.iterdir())):
        logger.info(f"Creating new seasonal directory: {seasonal_dir_path}")
        seasonal_dir_path.mkdir(parents=True, exist_ok=True)

        # populate seasonal dir contents
        seasonal_dev_dir = get_seasonal_dev_dir(dt)
        logger.debug(f"Seasonal dev directory: {seasonal_dev_dir}")
        seasonal_dev_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Creating and cloning repo for {seasonal_dev_dir.name}")
        create_and_clone_repo(
            seasonal_dev_dir.name, seasonal_dev_dir, settings.seasonal_dir_template_repo
        )
    else:
        logger.info(f"Seasonal directory already exists: {seasonal_dir_path}")

    # step 3: check latest softlink
    latest_seasonal_dir = seasonal_dir / "latest"
    if latest_seasonal_dir.exists():
        logger.debug(f"Removing existing symlink: {latest_seasonal_dir}")
        latest_seasonal_dir.unlink()
    logger.info(f"Creating symlink: {latest_seasonal_dir} -> {seasonal_dir_path}")
    latest_seasonal_dir.symlink_to(seasonal_dir_path)

    # todo: link to ~/code dir as well?
    logger.info("Seasonal folder setup complete")
    return seasonal_dir_path


# endregion idea 3 - seasonal folder

# region idea 4
# - set up ~/.calmmage dir
# endregion idea 4

# region idea 5 - build zshrc file
# - [x] safe add line to zshrc file
# - [x] safe add variable to zshrc file
# - safe add variable to ~/.env file

# endregion idea 5 - build zshrc file


# region idea 6 - set up ~/code dir - softlinks to key locations
# - main dirs?
# - seasonal (latest, drafts, vscode workspace?)
# - contexts (libs, dev, etc)


def setup_symlinks_dir():
    links_to_create = {
        # 1) seasonal
        # 2) examples
        # 3) seasonal dev
        # 4) calmlib?
        # 5) dev-env? just main repos?
        # 6) specific contenxt:
        # - templates
        # - libs
        "calmlib": projects_dir / "calmlib",
        "examples": projects_dir / "examples",
        "seasonal": seasonal_dir / "latest",
        "dev": get_seasonal_dev_dir(),
        "dev-env": projects_dir / "dev-env",
        "templates": contexts_dir / "templates",
        "libs": contexts_dir / "libs",
        # "projects": projects_dir,
        # "experiments": experiments_dir,
    }
    for link_name, target_path in links_to_create.items():
        link_path = settings.symlinks_dir / link_name
        if link_path.exists():
            logger.debug(f"Link {link_path} already existed. Re-creating")
            link_path.unlink()
        logger.info(f"Creating symlink: {link_path} -> {target_path}")
        link_path.symlink_to(target_path)


# endregion idea 6 - set up ~/code dir - softlinks to key locations

# region 7 - unsorted, misc


# endregion 7 - unsorted, misc

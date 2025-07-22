from pathlib import Path

from pydantic_settings import BaseSettings


class DevEnvSettings(BaseSettings):
    root_dir: Path = Path("~/work").expanduser()
    app_data_dir: Path = Path("~/.calmmage").expanduser()

    # todo: this should be defined dynamically relative to the root_dir AFTER the root_dir initialized
    # scripts_dir: Path = root_dir / "scripts"
    # seasonal_projects_dir: Path = root_dir / "projects/calmmage-private/seasonal/"
    # new_projects_dir: Path = seasonal_projects_dir / "latest/experiments"
    # project_unsorted_dir: Path = root_dir / "structured/unsorted"
    # all_projects_dir: Path = root_dir / "projects"

    # todo: custom env variable name telegram_notifications_bot_token
    # telegram notifications token

    class Config:
        env_prefix = "CALMMAGE_DEV_ENV"


settings = DevEnvSettings()

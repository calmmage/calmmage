"""Settings for the Telegram downloader."""
from datetime import timedelta
from pathlib import Path
from typing import List, Optional, Union

import yaml
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings


class DownloadSettings(BaseModel):
    """Settings for downloading messages and media."""
    download_media: bool = False
    media_dir: Path = Path("downloads/media")
    logs_dir: Path = Path("downloads/logs")
    save_json: bool = True
    save_text: bool = True

    @validator("media_dir", "logs_dir", pre=True)
    def create_directory(cls, v):
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return path


class ChatLists(BaseModel):
    """Lists of chats to download from."""
    personal: List[str] = Field(default_factory=list)
    groups: List[Union[str, int]] = Field(default_factory=list)
    channels: List[Union[str, int]] = Field(default_factory=list)


class DownloaderConfig(BaseModel):
    """Main configuration for the Telegram downloader."""
    time_window: str = "1d"
    chats: ChatLists = Field(default_factory=ChatLists)
    settings: DownloadSettings = Field(default_factory=DownloadSettings)

    @validator("time_window")
    def parse_time_window(cls, v: str) -> str:
        """Parse time window string into timedelta."""
        unit = v[-1].lower()
        try:
            value = int(v[:-1])
        except ValueError:
            raise ValueError(f"Invalid time window format: {v}")

        if unit == 'd':
            timedelta(days=value)
        elif unit == 'h':
            timedelta(hours=value)
        elif unit == 'm':
            timedelta(minutes=value)
        else:
            raise ValueError(f"Invalid time unit: {unit}. Use 'd' for days, 'h' for hours, or 'm' for minutes")
        return v

    def get_time_delta(self) -> timedelta:
        """Convert time_window string to timedelta."""
        unit = self.time_window[-1].lower()
        value = int(self.time_window[:-1])

        if unit == 'd':
            return timedelta(days=value)
        elif unit == 'h':
            return timedelta(hours=value)
        elif unit == 'm':
            return timedelta(minutes=value)
        else:
            raise ValueError(f"Invalid time unit: {unit}")


def load_config(config_path: Union[str, Path]) -> DownloaderConfig:
    """Load configuration from YAML file."""
    with open(config_path) as f:
        config_dict = yaml.safe_load(f)
    return DownloaderConfig(**config_dict) 
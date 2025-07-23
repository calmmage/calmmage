import asyncio
import yaml
from loguru import logger
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict, Any
from utils import setup_logger


class SizeThresholds(BaseSettings):
    max_members_group: int = 10000  # groups larger than this are considered "big"
    max_members_channel: int = 50000  # channels larger than this are considered "big"


class ChatCategoryConfig(BaseSettings):
    enabled: bool = False
    backdays: Optional[int] = None
    limit: Optional[int] = None
    whitelist: List[str] = Field(default_factory=list)
    blacklist: List[str] = Field(default_factory=list)
    download_attachments: bool = False
    skip_big: bool = True  # whether to skip large groups/channels


class MessageDownloadConfig(BaseSettings):
    # todo: unused for now
    size_thresholds: SizeThresholds = Field(default_factory=SizeThresholds)
    owned_groups: ChatCategoryConfig = Field(default_factory=ChatCategoryConfig)
    owned_channels: ChatCategoryConfig = Field(default_factory=ChatCategoryConfig)
    other_groups: ChatCategoryConfig = Field(default_factory=ChatCategoryConfig)
    other_channels: ChatCategoryConfig = Field(default_factory=ChatCategoryConfig)
    private_chats: ChatCategoryConfig = Field(default_factory=ChatCategoryConfig)
    bots: ChatCategoryConfig = Field(default_factory=ChatCategoryConfig)

    @classmethod
    def from_yaml(cls, path: Path) -> "MessageDownloadConfig":
        with open(path) as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict)

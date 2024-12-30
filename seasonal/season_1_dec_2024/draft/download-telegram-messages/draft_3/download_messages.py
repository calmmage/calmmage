from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field
import yaml
from loguru import logger
from utils import setup_logger
import asyncio
class SizeThresholds(BaseSettings):
    max_members_group: int = 10000    # groups larger than this are considered "big"
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
    size_thresholds: SizeThresholds = Field(default_factory=SizeThresholds)
    owned_groups: ChatCategoryConfig = Field(default_factory=ChatCategoryConfig)
    owned_channels: ChatCategoryConfig = Field(default_factory=ChatCategoryConfig)
    other_groups: ChatCategoryConfig = Field(default_factory=ChatCategoryConfig)
    other_channels: ChatCategoryConfig = Field(default_factory=ChatCategoryConfig)
    private_chats: ChatCategoryConfig = Field(default_factory=ChatCategoryConfig)
    bots: ChatCategoryConfig = Field(default_factory=ChatCategoryConfig)

    @classmethod
    def from_yaml(cls, path: Path) -> "MessageDownloadConfig":
        with open(path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict)


async def load_messages(config: MessageDownloadConfig):
    pass

async def main(debug: bool = False):
    setup_logger(logger, level="DEBUG" if debug else "INFO")
    logger.debug("Starting script")
    config = MessageDownloadConfig.from_yaml(Path("config_debug.yaml"))
    logger.debug(f"Loaded config: {config}")
    data = await load_messages(config)
    


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    
    # Run the async main function
    logger.debug("Starting script")
    # asyncio.run(main(debug=args.debug))
    # asyncio.run(main_linear(debug=args.debug))
    asyncio.run(main(debug=args.debug))
    logger.debug("Script completed")

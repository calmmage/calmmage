"""Main script to run the Telegram downloader."""
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
import sys
sys.path.append("./")
from draft_2_download.download_script.downloader import TelegramDownloader
from draft_2_download.download_script.settings import load_config

# Load environment variables
load_dotenv()



async def code_callback():
    """Callback to get verification code."""
    return input("Enter the verification code: ")


async def main():
    # Load API credentials
    api_id = int(os.getenv("TELEGRAM_API_ID"))
    api_hash = os.getenv("TELEGRAM_API_HASH")
    phone = os.getenv("TELEGRAM_PHONE_NUMBER")
    user_id = os.getenv("TELEGRAM_USER_ID")
    
    if not all([api_id, api_hash, user_id]):
        raise ValueError(
            "Required credentials not found. Please set TELEGRAM_API_ID, TELEGRAM_API_HASH, "
            "and TELEGRAM_USER_ID environment variables."
        )
    
    # Load config
    config_path = Path("config.yaml")
    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found at {config_path}. Please create one using the template."
        )
    
    config = load_config(config_path)
    logger.info(f"Loaded config from {config_path}")
    
    # Initialize and run downloader
    downloader = TelegramDownloader(
        config=config,
        user_id=user_id,
        phone=phone,
        code_callback=code_callback,
    )
    
    # try:
    await downloader.init_client(api_id, api_hash)
    await downloader.run()
    # finally:
    #     await downloader.close()


if __name__ == "__main__":
    asyncio.run(main()) 
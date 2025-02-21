# Plan for this file:

import asyncio
import random
from datetime import datetime, timedelta, timezone
from loguru import logger
from main import get_telethon_client, get_database
from model_chat_data import ChatData
from model_message_donwload_config import MessageDownloadConfig, ChatCategoryConfig
# 1. load list of chats
# 2. load config
# 3. for each chat - pick a config that applies to it
# 4. download messages as per config
# 5. save messages to a database
from pathlib import Path
from telethon import TelegramClient
from tqdm import tqdm
from tqdm.asyncio import tqdm as atqdm
from typing import List
from utils import setup_logger


async def main(debug: bool = False):
    """
    # 1. load list of chats
    # 2. load config
    # 3. for each chat - pick a config that applies to it
    # 4. download messages as per config
    # 5. save messages to a database
    """
    logger.debug("Setting up logger...")
    setup_logger(logger, level="DEBUG" if debug else "INFO")
    logger.debug("Starting script")

    # 1. load list of chats
    logger.debug("Loading chats...")
    chats = await load_chats()
    logger.debug(f"Loaded {len(chats)} chats")

    if debug:
        logger.debug("Debug mode enabled - shuffling and limiting chats")
        random.shuffle(chats)
        chats = chats[:10]
        logger.debug(f"Limited to {len(chats)} chats")

    # 2. load config
    logger.debug("Loading config...")
    # config_file = Path("config_daily.yaml")
    # config_file = Path("config_archive.yaml")
    config_file = Path("config_debug.yaml")
    logger.debug(f"Using config file: {config_file}")

    config = load_config(config_file)
    logger.debug("Config loaded successfully")

    logger.debug("Getting Telethon client")
    client = await get_telethon_client()

    logger.debug("Getting database")
    db = get_database()

    # 3. for each chat - pick a config that applies to it
    logger.debug("Starting chat processing loop...")

    for chat in tqdm(chats, desc="Processing chats"):
        logger.debug(f"Processing chat: {chat.name}")
        chat_config = pick_chat_config(chat, config)
        logger.debug(f"Selected config type: {type(chat_config).__name__}")

        # 4. download messages as per config
        logger.debug(f"Downloading messages for chat: {chat.name}")
        messages = await download_messages(client, chat, chat_config)
        logger.debug(f"Downloaded {len(messages)} messages")

        # 5. save messages to a database
        logger.debug(f"Saving {len(messages)} messages to database")
        if len(messages) > 0:
            save_messages(messages, db)
        logger.debug("Messages saved successfully")


async def load_chats() -> List[ChatData]:
    logger.debug("Starting chat loading process...")
    from get_chat_list import get_chats
    logger.debug("Getting raw chats from get_chats()")
    chats = await get_chats()
    logger.debug(f"Got {len(chats)} raw chats")

    res_chats = []
    logger.debug("Converting raw chats to ChatData objects")
    for chat in chats:
        # logger.debug(f"Converting chat: {chat['entity']}")
        res_chats.append(ChatData(
            entity=chat['entity'],
            last_message_date=chat['last_message_date']
        ))
    logger.debug(f"Converted {len(res_chats)} chats to ChatData objects")
    return res_chats


def load_config(config_path: Path):
    logger.debug(f"Loading config from {config_path}")
    config = MessageDownloadConfig.from_yaml(config_path)
    logger.debug("Config loaded successfully")
    return config


def pick_chat_config(chat: ChatData, config: MessageDownloadConfig):
    logger.debug(f"Picking config for chat: {chat.name}")
    logger.debug(f"Chat category: {chat.entity_category}")

    if chat.entity_category == 'group':
        if chat.is_owned:
            logger.debug("Selected: owned groups config")
            return config.owned_groups
        else:
            logger.debug("Selected: other groups config")
            return config.other_groups
    elif chat.entity_category == 'channel':
        if chat.is_owned:
            logger.debug("Selected: owned channels config")
            return config.owned_channels
        else:
            logger.debug("Selected: other channels config")
            return config.other_channels
    elif chat.entity_category == 'bot':
        logger.debug("Selected: bot config")
        return config.bots
    elif chat.entity_category == 'private chat':
        logger.debug("Selected: private chat config")
        return config.private_chats
    else:
        logger.warning(f"No config found for {chat.entity_category=}")
        return None


async def download_messages(client: TelegramClient, chat: ChatData, chat_config: ChatCategoryConfig):
    logger.debug(f"Starting message download for chat: {chat.name}")

    if not chat_config or not chat_config.enabled:
        logger.debug(f"Skipping chat {chat.name}: config disabled")
        return []

    logger.info(f"Downloading messages from chat: {chat.name}")

    # Initialize parameters for message download
    kwargs = {}
    logger.debug("Initializing download parameters")

    # Apply config parameters
    if chat_config.backdays:
        # Make min_date timezone-aware to match message.date
        min_date = datetime.now(timezone.utc) - timedelta(days=chat_config.backdays)
        logger.debug(f"Set min_date to {min_date}")
    else:
        min_date = None
        logger.debug("No min_date set")

    if chat_config.limit:
        kwargs['limit'] = chat_config.limit
        logger.debug(f"Set message limit to {chat_config.limit}")

    # Skip large groups if configured
    if chat_config.skip_big and chat.is_big:
        logger.warning(f"Skipping large chat {chat.name}")
        return []

    messages = []
    try:
        logger.debug("Starting message iteration")
        async for message in atqdm(client.iter_messages(chat.entity, **kwargs),
                                   desc=f"Downloading messages for chat {chat.name}"):
            # Skip messages older than min_date
            if min_date and message.date < min_date:
                logger.debug(f"Reached message older than min_date ({message.date}), stopping")
                break

            # Use built-in to_json() method
            messages.append(message)
            # logger.debug(f"Added message ID {message.id}")

    except Exception as e:
        logger.error(f"Error downloading messages from {chat.name}: {e}")
        import traceback
        logger.error("Full traceback:\n" + "".join(traceback.format_exc()))

        return []

    logger.info(f"Downloaded {len(messages)} messages from {chat.name}")
    return messages


def save_messages(messages, db):
    """ Save messages to a database """
    logger.debug("Starting message save process")

    # step 1: get a db connection - i already did this somewhere
    logger.debug("Getting database connection")
    collection_name = 'telegram_messages'
    collection = db[collection_name]
    logger.debug(f"Got collection: {collection_name}")

    # make messages to json format
    logger.debug("Converting messages to JSON")
    messages_json = [message.to_dict() for message in messages]
    logger.debug(f"Converted {len(messages_json)} messages to JSON")

    logger.debug("Inserting messages into database")

    collection.insert_many(messages_json)
    logger.debug("Messages inserted successfully")


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
